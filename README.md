# 🖱️ AI Virtual Mouse Pro

> Control your computer using hand gestures through a webcam — no physical mouse required.

An AI-powered virtual mouse built with **Python, OpenCV, MediaPipe, and PyAutoGUI**.  
The project uses real-time hand tracking and computer vision to recognize hand gestures and translate them into mouse and system-control actions.

This project is developed incrementally through different versions, starting from basic cursor control in **V1** and evolving into a more feature-rich gesture-based interface in **V2**.

---

## ✨ Highlights

- 🖐️ Real-time hand tracking through webcam
- 🖱️ Touch-free cursor control
- 👆 Gesture-based mouse actions
- 📜 Automatic smooth scrolling
- 🔊 Gesture-based volume control
- 🔆 Gesture-based brightness control
- 🤏 Right click and double click gestures
- 🖱️ Drag & drop using hand gestures
- ⚡ Smooth cursor movement
- 🎯 Gesture cooldowns for more stable interaction
- 📊 Real-time FPS monitoring
- 💻 Designed for Windows desktop control

---

## 🚀 Features

### 🖱️ Mouse Control

The index finger can be used as a virtual mouse pointer.

- ☝️ **Index finger only** → Move cursor
- 🤏 **Thumb + Middle finger** → Single click
- 🤏 **Thumb + Index finger** → Double click
- 🤏 **Thumb + Ring finger** → Right click
- 🤏 **Thumb + Pinky + Index finger** → Drag & Drop

### 📜 Automatic Scrolling

- ✌️ **Index + Middle fingers** → Automatic smooth scrolling
- No continuous hand movement is required once the gesture is detected.
- Designed for browsing and reading long pages hands-free.

### 🔆 Brightness Control

Use **four fingers open** to control screen brightness.

- 🖐️ Move hand **upward** → Increase brightness
- 🖐️ Move hand **downward** → Decrease brightness

### 🔊 Volume Control

Use **three fingers open** to control system volume.

- 🤟 Move hand **upward** → Increase volume
- 🤟 Move hand **downward** → Decrease volume

### 🎯 Stability & Performance

V2 includes several improvements to make interaction more reliable:

- Cursor smoothing
- Gesture cooldowns
- Movement dead zones
- Control update intervals
- Gesture separation
- Automatic scroll timing
- FPS monitoring
- Lightweight MediaPipe hand tracking configuration

---

## ✋ Gesture Controls

| Hand Gesture | Action |
|---|---|
| ☝️ Index finger only | Move cursor |
| 🤏 Thumb + Middle | Single click |
| 🤏 Thumb + Index | Double click |
| 🤏 Thumb + Ring | Right click |
| 🤏 Thumb + Pinky + Index | Drag & Drop |
| ✌️ Index + Middle | Automatic scrolling |
| 🖐️ Four fingers open | Brightness control |
| 🤟 Three fingers open | Volume control |

---

## 🧠 How It Works

The system follows a simple real-time computer vision pipeline:

```text
Webcam
   ↓
OpenCV Frame Capture
   ↓
MediaPipe Hand Detection
   ↓
Hand Landmark Extraction
   ↓
Finger/Gesture Detection
   ↓
Gesture Classification
   ↓
Mouse / Scroll / System Control
```

### 1. Webcam Input

OpenCV captures frames from the computer's webcam in real time.

### 2. Hand Tracking

MediaPipe detects the hand and provides landmark coordinates for the fingers and joints.

### 3. Gesture Detection

The program analyzes the relative positions of the finger landmarks to determine which fingers are open or closed.

### 4. Gesture Mapping

Detected gestures are mapped to specific computer actions such as:

- Cursor movement
- Mouse clicks
- Double click
- Right click
- Drag & drop
- Scrolling
- Brightness adjustment
- Volume adjustment

### 5. System Interaction

PyAutoGUI performs mouse and scrolling actions, while Windows-specific libraries handle brightness and audio controls.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 Python | Core programming language |
| 👁️ OpenCV | Webcam capture and computer vision |
| 🖐️ MediaPipe | Real-time hand landmark detection |
| 🖱️ PyAutoGUI | Mouse and keyboard automation |
| 🔆 Screen Brightness Control | Windows brightness control |
| 🔊 Pycaw | Windows system volume control |
| ⚙️ Comtypes | Windows COM interface support |

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/anshvashisht08-alt/AI-Virtual-Mouse.git
```

### 2. Open the project directory

```bash
cd AI-Virtual-Mouse
```

### 3. Install dependencies

```bash
pip install opencv-python mediapipe pyautogui screen-brightness-control pycaw comtypes
```

---

## ▶️ Running the Project

### Run V1

```bash
python virtual_mouse.py
```

### Run V2

```bash
python virtual_mouse_v2.py
```

Make sure:

- Your webcam is connected.
- Camera access is enabled.
- You are using Windows for brightness and volume controls.
- The required Python packages are installed.

Press:

```text
ESC
```

to exit the application.

---

## 📁 Project Structure

```text
AI-Virtual-Mouse/
│
├── virtual_mouse.py
├── virtual_mouse_v2.py
└── README.md
```

### `virtual_mouse.py`

The original V1 implementation containing the basic virtual mouse functionality.

### `virtual_mouse_v2.py`

The improved V2 implementation with smoother movement, additional gestures, scrolling, brightness control, volume control, and better interaction stability.

---

## 🔄 Version History

### 🟢 V1 — Foundation

V1 established the core virtual mouse concept.

#### Included

- Real-time webcam hand tracking
- Index-finger cursor control
- Basic mouse gestures
- Click functionality
- Drag & drop
- Basic brightness control

V1 focused primarily on building the foundation of the system.

---

### 🔵 V2 — AI Virtual Mouse Pro

V2 builds on the V1 foundation and introduces improved usability and additional system controls.

#### Improvements

- ⚡ Smoother cursor movement
- 🎯 More stable gesture detection
- 🖱️ Single click gesture
- 🖱️ Double click gesture
- 🖱️ Right click gesture
- 🖱️ Drag & drop gesture
- 📜 Automatic smooth scrolling
- 🔆 Brightness control
- 🔊 Volume control
- 📊 FPS monitoring
- ⏱️ Gesture cooldowns
- 🎯 Movement dead zones
- ⚙️ Improved responsiveness

---

## 💡 Design Goals

The main goals of this project are:

- Build a practical computer-vision application.
- Explore real-time hand tracking.
- Understand gesture recognition.
- Control a computer without traditional input hardware.
- Improve stability and responsiveness through iterative development.
- Gradually evolve the project instead of jumping directly into a highly complex system.

---

## 🎯 Future Improvements

The project will continue to evolve beyond V2.

Planned improvements include:

- 🤖 Advanced gesture recognition
- ✋ Multi-hand support
- ⚙️ Custom gesture mapping
- 🧠 Personalized gesture profiles
- 🎮 More system-level controls
- 🪟 Better application/window control
- 📈 Improved gesture classification
- ⚡ Further performance optimization
- 🧩 Modular gesture configuration
- 🎥 Better demo and visualization system

---

## 🧪 Development Approach

This project follows an iterative development approach.

```text
V1
↓
Basic Hand Tracking
↓
Basic Mouse Control
↓
V2
↓
Improved Stability
↓
More Gestures
↓
System Controls
↓
Future Versions
↓
Smarter & More Adaptive Interaction
```

Each version is maintained separately so that the development progress can be tracked and compared over time.

---

## ⚠️ Notes

- This project is primarily designed and tested for **Windows**.
- Brightness and volume functionality depend on Windows system support and the installed hardware/drivers.
- Good lighting and a clearly visible hand generally improve hand-tracking performance.
- Camera position and distance can affect gesture recognition.
- The project is intended as an experimental computer-vision and human-computer-interaction project.

---

## 🌟 Why This Project?

Traditional mouse and touch interfaces are not always the only way to interact with a computer.

This project explores how **computer vision + hand tracking + gesture recognition** can create an alternative human-computer interaction system using hardware that is already available on most laptops and desktops: a webcam.

The project also demonstrates how a simple idea can be developed incrementally from a basic prototype into a more capable application.

---

## 👨‍💻 Author

**Ansh Sharma**

B.Tech AI & ML Student

Interested in:

- Artificial Intelligence
- Machine Learning
- Computer Vision
- Human-Computer Interaction
- AI-based Applications

---

## ⭐ Support the Project

If you find this project interesting or useful:

- ⭐ Star the repository
- 🍴 Fork the project
- 💡 Suggest improvements
- 🐛 Report issues
- 🚀 Follow the project's future versions

---

## 📌 Project Status

**Current Version: V2 — AI Virtual Mouse Pro**

```text
V1 ✅ Completed
V2 ✅ Completed
V3 🚧 Future Development
```

---

### 🖱️ Built with Python + Computer Vision + Hand Gestures

**From a simple webcam to a touch-free computer interface. 🚀**
