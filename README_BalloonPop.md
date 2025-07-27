# 🎈 Balloon Pop Game – Interactive Wall Projection Using Hand Gestures

This project is an **interactive balloon popping game** designed for **wall projection** where users can pop balloons by **touching the projection**. It uses a **webcam or phone camera** (IP camera) to track hand gestures and simulate touch on a wall. Designed using **Python, OpenCV, Pygame, and MediaPipe (via cvzone)**.

---

## 🚀 Features

- Real-time **hand gesture tracking** using external phone camera or webcam
- Touchless interaction: **pop balloons by pointing or touching the projected wall**
- **Colorful balloons**: red, yellow, green with different points
- **Combo system** for fast pops
- Background image and Game Over screen with theme
- Projector-friendly full-screen mode
- **Phone camera support** via IP webcam stream

---

## 📂 Folder Structure

```
BalloonPopProject/
│
├── assets/                        # Images and fonts
│   ├── BalloonRed.png
│   ├── BalloonGreen.png
│   ├── BalloonYellow.png
│   ├── BackgroundBlue.jpg
│   ├── a937cd27...gameover.png
│   └── Marcellus-Regular.ttf
│
├── snapshots/                    # (Auto-created) Screenshots of final score
│
├── utils.py                      # Helper functions: coordinate mapping, collision detection
├── BalloonPop.py                 # Main game logic
├── leaderboard.txt               # Score history
├── install.bat                   # Script to install all dependencies
├── requirements.txt              # Python packages
└── README.md                     # You are here
```

---

## 🧰 Requirements

- Python 3.10.x (Recommended)
- `opencv-python`
- `pygame`
- `cvzone`
- `mediapipe`
- `numpy`

---

## ⚙️ Setup Instructions

1. Open terminal or CMD in the project folder
2. Run the installer:
   ```bash
   install.bat
   ```
   Or manually:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📱 Use Your Phone as a Webcam (for wall projection)

1. Install **IP Webcam** (Android) or **DroidCam**
2. Make sure phone and PC are on the **same Wi-Fi**
3. Start camera server on phone — note the stream URL like:
   ```
   http://192.168.29.26:4747/video
   ```
4. In `BalloonPop.py`, update:
   ```python
   cap = cv2.VideoCapture("http://192.168.29.26:4747/video")
   ```

---

## 🕹️ How to Play

- Project the game on a **flat wall**
- Place your **phone camera** facing the wall to track hands
- Use your **index finger** to "touch" the projected balloons
- Balloons pop when finger overlaps them!
- Game lasts **30 seconds**, score is displayed with animations
- Press `Q` to Quit or `R` to Restart after game over

---

## 🛠️ Main Code Overview

### `BalloonPop.py`
- Fullscreen Pygame display with webcam input
- Uses `cvzone.HandTrackingModule.HandDetector` to track finger
- Balloons move upwards and pop on collision with finger
- Points:  
  - Red 🎈 = 1 point  
  - Yellow 🎈 = 2 points  
  - Green 🎈 = 3 points  
- Combo logic: 3 pops in 3 sec = `x2 bonus`

### `utils.py`
- `map_coordinates`: maps OpenCV finger coordinates to screen
- `check_collision`: returns `True` if finger overlaps balloon

---

## 🔧 Easily Customizable

| Feature            | File          | What to change                        |
|-------------------|---------------|---------------------------------------|
| Background image  | `assets/`     | Replace `BackgroundBlue.jpg`          |
| Game Over screen  | `assets/`     | Replace `a937cd27-...gameover.png`    |
| Fonts             | `assets/`     | Replace `Marcellus-Regular.ttf`       |
| Balloon images    | `assets/`     | Replace `BalloonRed.png`, etc.        |
| Game duration     | `BalloonPop.py` | `game_time = 30` (change seconds)   |
| Balloon types     | `Balloon` class | Modify color/point logic             |

---

## 📸 Wall Projection Setup

1. Connect laptop to **projector**
2. Use `pygame.FULLSCREEN` mode (already done)
3. Place phone camera at a fixed angle facing wall
4. Run the game – touch the projected balloons!

---

## 🧠 Credits

Built using:
- Python + OpenCV
- MediaPipe via [cvzone](https://github.com/cvzone/cvzone)
- Pygame
- Inspired by human-computer interaction & AR-based projection touch

---