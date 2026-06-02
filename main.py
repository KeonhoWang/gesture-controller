import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import pyautogui
import subprocess
import time
import numpy as np
import os

# Setup
pyautogui.FAILSAFE = False
base_options = mp.tasks.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
cam_w, cam_h = 640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cam_w)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_h)
screen_w, screen_h = pyautogui.size()

print("Gesture Controller running! Press Q to quit. Press S to screenshot.")

# Gesture Map
GESTURE_MAP = {
    (0, 1, 0, 0, 0): "VOLUME UP",
    (0, 0, 0, 0, 1): "VOLUME DOWN",
    (1, 1, 1, 1, 1): "PLAY PAUSE",
    (0, 1, 1, 0, 0): "NEXT TAB",
    (1, 0, 0, 0, 0): "PREV TAB",
    (0, 1, 1, 1, 0): "BRIGHTNESS UP",
    (0, 0, 0, 0, 0): "BRIGHTNESS DOWN",
    (0, 1, 0, 0, 1): "SCREENSHOT",
    (1, 1, 0, 0, 0): "AIR MOUSE",
}

GESTURE_LABELS = {
    "VOLUME UP":       "VOL UP",
    "VOLUME DOWN":     "VOL DOWN",
    "PLAY PAUSE":      "PLAY / PAUSE",
    "NEXT TAB":        "NEXT TAB",
    "PREV TAB":        "PREV TAB",
    "BRIGHTNESS UP":   "BRIGHTNESS UP",
    "BRIGHTNESS DOWN": "BRIGHTNESS DOWN",
    "SCREENSHOT":      "SCREENSHOT!",
    "AIR MOUSE":       "AIR MOUSE ON",
}

# Actions
def volume_up():
    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])

def volume_down():
    subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])

def play_pause():
    pyautogui.press('playpause')

def next_tab():
    pyautogui.hotkey('command', 'tab')

def prev_tab():
    pyautogui.hotkey('command', 'shift', 'tab')

def brightness_up():
    subprocess.run(["osascript", "-e", "tell application \"System Events\" to key code 144"])

def brightness_down():
    subprocess.run(["osascript", "-e", "tell application \"System Events\" to key code 145"])

def take_screenshot():
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        desktop = os.path.expanduser("~/Desktop")
        path = os.path.join(desktop, f"gesture_screenshot_{timestamp}.png")
        result = subprocess.run(["screencapture", "-x", path], capture_output=True, text=True)
        if os.path.exists(path):
            print(f"Screenshot saved: {path}")
            return True
        else:
            print(f"Screenshot failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Screenshot error: {e}")
        return False

# Finger Detection
def fingers_up(landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    fingers.append(1 if landmarks[4].x < landmarks[3].x else 0)
    for tip in tips[1:]:
        fingers.append(1 if landmarks[tip].y < landmarks[tip - 2].y else 0)
    return tuple(fingers)

# Draw Hand Landmarks
def draw_landmarks(frame, hand_landmarks):
    proto = landmark_pb2.NormalizedLandmarkList()
    proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=l.x, y=l.y, z=l.z)
        for l in hand_landmarks
    ])
    solutions.drawing_utils.draw_landmarks(
        frame, proto,
        solutions.hands.HAND_CONNECTIONS,
        solutions.drawing_styles.get_default_hand_landmarks_style(),
        solutions.drawing_styles.get_default_hand_connections_style()
    )

# Draw UI
def draw_ui(frame, gesture_label, air_mouse_on, smoothed_pos, hold_progress, hold_gesture):
    h, w = frame.shape[:2]

    # Top bar
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 60), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

    # Title
    cv2.putText(frame, "GESTURE CONTROLLER", (10, 22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

    # Status dot
    dot_color = (0, 255, 100) if gesture_label else (80, 80, 80)
    cv2.circle(frame, (w - 20, 20), 8, dot_color, -1)

    # Air mouse label
    if air_mouse_on:
        cv2.putText(frame, "AIR MOUSE ON", (10, 48),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)

    # Hold progress bar
    if hold_gesture and hold_progress > 0:
        bar_w = int((hold_progress / 12) * (w - 20))
        cv2.rectangle(frame, (10, h - 75), (10 + bar_w, h - 62), (0, 200, 255), -1)
        cv2.rectangle(frame, (10, h - 75), (w - 10, h - 62), (80, 80, 80), 2)
        cv2.putText(frame, f"Hold: {GESTURE_LABELS.get(hold_gesture, str(hold_gesture))}", (10, h - 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 200, 255), 1)

    # Gesture label bottom bar
    if gesture_label:
        overlay2 = frame.copy()
        cv2.rectangle(overlay2, (0, h - 55), (w, h), (20, 20, 20), -1)
        cv2.addWeighted(overlay2, 0.75, frame, 0.25, 0, frame)
        cv2.putText(frame, gesture_label, (10, h - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 100), 2)

    # Air mouse cursor dot
    if air_mouse_on and smoothed_pos:
        cx, cy = smoothed_pos
        cv2.circle(frame, (cx, cy), 12, (0, 200, 255), -1)
        cv2.circle(frame, (cx, cy), 18, (0, 200, 255), 2)
        cv2.putText(frame, "CURSOR", (cx + 20, cy),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 200, 255), 1)

    # Guide top right
    guide = [
        "Index up  = Vol Up",
        "Pinky up  = Vol Down",
        "Open hand = Play/Pause",
        "Peace     = Next Tab",
        "Thumb     = Prev Tab",
        "3 fingers = Bright Up",
        "Fist      = Bright Down",
        "Idx+Pnky  = Screenshot",
        "Thm+Idx   = Air Mouse",
    ]
    for i, line in enumerate(guide):
        cv2.putText(frame, line, (w - 210, 30 + i * 17),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (180, 180, 180), 1)

    return frame

# Smooth cursor
prev_x, prev_y = 0, 0
SMOOTH = 5

def smooth_cursor(x, y):
    global prev_x, prev_y
    prev_x = prev_x + (x - prev_x) / SMOOTH
    prev_y = prev_y + (y - prev_y) / SMOOTH
    return int(prev_x), int(prev_y)

# Main Loop
last_action_time = 0
COOLDOWN         = 1.5
gesture_label    = ""
label_timer      = 0
air_mouse_on     = False
smoothed_pos     = None
HOLD_FRAMES      = 12
hold_counter     = 0
last_gesture     = None
frame_count      = 0
PROCESS_EVERY    = 2

while True:
    success, frame = cap.read()
    if not success:
        break

    frame       = cv2.flip(frame, 1)
    frame_count += 1

    if frame_count % PROCESS_EVERY == 0:
        rgb      = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result   = detector.detect(mp_image)

        if result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                draw_landmarks(frame, hand_landmarks)
                fingers = fingers_up(hand_landmarks)
                gesture = GESTURE_MAP.get(fingers)

                # Air Mouse mode
                if air_mouse_on:
                    index_tip = hand_landmarks[8]
                    cx = int(index_tip.x * cam_w)
                    cy = int(index_tip.y * cam_h)
                    smoothed_pos = (cx, cy)

                    mouse_x = int(np.interp(index_tip.x, [0.1, 0.9], [0, screen_w]))
                    mouse_y = int(np.interp(index_tip.y, [0.1, 0.9], [0, screen_h]))
                    sx, sy  = smooth_cursor(mouse_x, mouse_y)
                    pyautogui.moveTo(sx, sy)

                    if fingers == (0, 0, 0, 0, 0):
                        if last_gesture == (0, 0, 0, 0, 0):
                            hold_counter += 1
                        else:
                            hold_counter = 0
                        last_gesture = (0, 0, 0, 0, 0)

                        if hold_counter >= HOLD_FRAMES:
                            air_mouse_on  = False
                            gesture_label = "AIR MOUSE OFF"
                            label_timer   = time.time()
                            hold_counter  = 0
                    else:
                        hold_counter = 0
                        last_gesture = fingers

                else:
                    smoothed_pos = None
                    now = time.time()

                    if gesture:
                        if gesture == last_gesture:
                            hold_counter += 1
                        else:
                            hold_counter = 0
                            last_gesture = gesture
                    else:
                        hold_counter = 0
                        last_gesture = None

                    if hold_counter >= HOLD_FRAMES and (now - last_action_time) > COOLDOWN:
                        last_action_time = now
                        gesture_label    = GESTURE_LABELS.get(gesture, gesture)
                        label_timer      = time.time()
                        hold_counter     = 0

                        if gesture == "VOLUME UP":         volume_up()
                        elif gesture == "VOLUME DOWN":     volume_down()
                        elif gesture == "PLAY PAUSE":      play_pause()
                        elif gesture == "NEXT TAB":        next_tab()
                        elif gesture == "PREV TAB":        prev_tab()
                        elif gesture == "BRIGHTNESS UP":   brightness_up()
                        elif gesture == "BRIGHTNESS DOWN": brightness_down()
                        elif gesture == "SCREENSHOT":
                            success = take_screenshot()
                            if not success:
                                gesture_label = "SCREENSHOT FAILED"
                        elif gesture == "AIR MOUSE":
                            air_mouse_on  = True
                            gesture_label = "AIR MOUSE ON"

                        print(f">> {gesture_label}")

        else:
            hold_counter = 0
            last_gesture = None

    # Clear label after 2 seconds
    if gesture_label and (time.time() - label_timer) > 2:
        gesture_label = ""

    # Keyboard shortcuts
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        take_screenshot()
        gesture_label = "SCREENSHOT!"
        label_timer   = time.time()
        print(">> Screenshot taken with S key!")

    hold_progress = hold_counter if last_gesture else 0
    frame = draw_ui(frame, gesture_label, air_mouse_on, smoothed_pos, hold_progress, last_gesture)
    cv2.imshow("Gesture Controller", frame)

cap.release()
cv2.destroyAllWindows()