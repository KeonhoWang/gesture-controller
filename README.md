# Hand Gesture Controller

A computer vision application that allows users to control their Mac using hand gestures and a webcam. Built with Python, MediaPipe, and OpenCV, the system recognizes hand gestures in real time and maps them to actions such as volume control, brightness adjustment, media playback, tab navigation, screenshots, and cursor movement.

## Features

- Volume Up / Down Control
- Brightness Adjustment
- Play / Pause Media
- Browser Tab Navigation
- Screenshot Capture
- Air Mouse Mode
- Real-Time Gesture Recognition
- Hold-to-Trigger Protection
- Live Camera Overlay UI

## Tech Stack

- Python
- MediaPipe
- OpenCV
- PyAutoGUI
- NumPy

## How It Works

The application captures webcam input and uses MediaPipe's hand landmark detection model to track finger positions. Detected finger patterns are translated into predefined gestures, which trigger system actions through PyAutoGUI and macOS system commands. A hold-to-trigger mechanism is implemented to reduce accidental activations, and cursor smoothing is used for stable Air Mouse functionality.

## Challenges & Solutions

### Gesture Misfires
Implemented a hold-to-trigger system that requires gestures to remain stable before activation.

### Cursor Jitter
Applied smoothing algorithms to reduce shaking and improve Air Mouse precision.

### Performance Optimization
Implemented frame skipping to maintain smooth real-time performance on Apple Silicon devices.

## Skills Demonstrated

- Computer Vision
- Real-Time Processing
- Human-Computer Interaction (HCI)
- Python Development
- Performance Optimization
- Event-Driven Programming
- State Management

## Future Improvements

- Custom Gesture Creation
- Multi-Hand Support
- Windows and Linux Compatibility
- User-Configurable Gesture Mapping

## License

MIT License
