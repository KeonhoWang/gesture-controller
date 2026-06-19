# ✋ Hand Gesture Controller

A computer vision application that allows users to control their computer using hand gestures and a webcam. Built with Python, MediaPipe, and OpenCV, the system recognizes hand movements in real time and maps them to actions such as volume control, brightness adjustment, media playback, browser navigation, screenshots, and cursor movement.

---

## 🚀 Features

- 🔊 Volume Up / Down Control
- 💡 Screen Brightness Adjustment
- ⏯️ Play / Pause Media
- 🌐 Browser Tab Navigation
- 📸 Screenshot Capture
- 🖱️ Air Mouse Mode
- ✋ Real-Time Hand Gesture Recognition
- 🛡️ Hold-to-Trigger Protection
- 🎥 Live Camera Overlay Interface

---

## 🛠️ Tech Stack

- Python
- MediaPipe
- OpenCV
- PyAutoGUI
- NumPy

---

## 📖 How It Works

The application captures webcam input and uses MediaPipe's hand landmark detection model to track finger positions in real time.

Detected finger patterns are translated into predefined gestures, which trigger system actions through PyAutoGUI and system-level commands. To improve usability, the application includes gesture stabilization, cursor smoothing, and hold-to-trigger protection to reduce accidental activations.

---

## 🎯 Supported Gestures

| Gesture Action | Function |
|---------------|----------|
| Volume Control | Increase or decrease system volume |
| Brightness Control | Adjust screen brightness |
| Play / Pause | Control media playback |
| Tab Navigation | Switch browser tabs |
| Screenshot | Capture and save screenshots |
| Air Mouse | Move and control the cursor |

---

## 🧩 Challenges & Solutions

### Gesture Misfires

Implemented a hold-to-trigger mechanism that requires a gesture to remain stable for a short duration before activation, reducing accidental commands.

### Cursor Jitter

Applied cursor smoothing algorithms to create more precise and natural Air Mouse movement.

### Performance Optimization

Implemented frame-skipping and optimized gesture detection logic to maintain smooth real-time performance on Apple Silicon devices.

---

## 💡 Skills Demonstrated

- Computer Vision
- Real-Time Image Processing
- Human-Computer Interaction (HCI)
- Python Development
- Event-Driven Programming
- State Management
- Performance Optimization
- Gesture Recognition Systems

---

## 📈 Future Improvements

- Custom Gesture Creation
- Multi-Hand Support
- Windows & Linux Compatibility
- User-Configurable Gesture Mapping
- Machine Learning-Based Gesture Training
- Gesture Profiles for Different Applications

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Keonho Wang**

Software Engineering Student passionate about Computer Vision, Artificial Intelligence, and Productivity Tools.


