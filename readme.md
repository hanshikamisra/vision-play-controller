# 🎮 VisionPlay: AI Gesture Game Controller

![Project Banner or Demo GIF](insert_your_gif_link_here)
> *Control games with your bare hands using Computer Vision.*

**VisionPlay** is a real-time AI application that converts hand gestures into keyboard inputs. It allows users to play platformer games (like the famous Chrome Dino Run) completely touch-free.

Built with **Python**, **OpenCV**, and **Google MediaPipe**, this project demonstrates how to integrate pre-trained deep learning models into practical, interactive applications with low latency.

---

## 🚀 Features

* **👆 Vertical Jump Control:** Tracks the y-coordinate of the index finger. Breaking the "virtual threshold" triggers a Jump (Spacebar).
* **✊ Crouching Logic (Fist Detection):** Uses geometric landmarks to detect if fingers are curled into a fist, triggering a Crouch (Down Arrow).
* **⚡ High Performance:** Optimized to run at 30+ FPS on standard CPU hardware (no GPU required).
* **🎮 Universal Support:** Can be mapped to control any game that accepts keyboard inputs.

---

## 🛠️ Tech Stack

* **Language:** Python 3.11
* **Computer Vision:** OpenCV (`cv2`)
* **AI/ML Model:** MediaPipe Hands (Google)
* **Automation:** PyAutoGUI (for keyboard simulation)

---

## ⚙️ Installation & Setup

This project requires **Python 3.9 - 3.11**.
*(Note: MediaPipe does not yet support Python 3.13).*

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/hanshikamisra/vision-play-controller.git](https://github.com/hanshikamisra/vision-play-controller.git)
    cd vision-play
    ```

2.  **Create a Virtual Environment** (Recommended)
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🕹️ How to Run

1.  Connect your webcam.
2.  Run the script:
    ```bash
    python main.py
    ```
3.  Open your game (Recommended: `chrome://dino` or [Dino Runner Online](https://chromedino.com/)).
4.  **The Controls:**
    * **Neutral:** Keep hand open and low.
    * **JUMP:** Raise hand quickly above the green line.
    * **DUCK:** Close hand into a fist.
5.  Press `q` in the camera window to quit.

---

## 🧠 How It Works

The system uses a pipeline approach:

1.  **Capture:** OpenCV reads a frame from the webcam.
2.  **Process:** MediaPipe Hands analyzes the frame and returns 21 3D hand landmarks (x, y, z coordinates).
3.  **Logic:**
    * **Jump:** The system checks the Y-coordinate of the **Index Finger Tip (Landmark 8)**. If `y < threshold`, a jump is triggered.
    * **Duck:** The system compares the Y-coordinates of the finger tips vs. the knuckles (PIPs). If tips are below knuckles, it registers a "Fist."
4.  **Act:** `PyAutoGUI` simulates the corresponding key press event.

---

## 🔮 Future Improvements

* Add support for **Multithreading** to separate frame processing from game logic (further reducing latency).
* Implement **Dynamic Calibration** so the "Jump Line" adjusts to the user's height automatically.
* Add support for "Left/Right" movement gestures to play more complex games like Super Mario Bros.
 
