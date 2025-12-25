# 🐍 Python Snake Gesture Game

A gesture-controlled Snake Game built using **Python, Pygame, OpenCV, and MediaPipe**.  
Control the snake using **hand movements only** — no keyboard required.

---

## 📌 Overview

This project combines **Computer Vision** with classic game development.  
Using a webcam and real-time **hand tracking**, the snake is controlled by the movement of the **index finger**, creating a touch-free gaming experience.

---

## ✨ Features

- Classic Snake Game mechanics  
- Hand gesture-based control  
- Live webcam feed integration  
- Real-time hand landmark detection  
- Food generation and score tracking  
- Wall and self-collision detection  
- Restart and quit options after game over  

---

## 🛠️ Technologies Used

- Python  
- Pygame  
- OpenCV  
- MediaPipe  
- NumPy  

---

## 🎯 How It Works

1. Webcam captures live video input  
2. MediaPipe detects hand landmarks  
3. Index finger movement is tracked  
4. Gesture direction is calculated  
5. Snake moves accordingly in the game arena  

---

## ▶️ How to Run

### Prerequisites

- Python 3.8 or higher
- Webcam

Install dependencies:
```bash
pip install pygame opencv-python mediapipe
```
Run the Game:
```bash
python snake_gesture_game.py
```

---

## 🎮 Gesture Controls

| Hand Movement     | Snake Direction |
|------------------|-----------------|
| Move finger up    | Up              |
| Move finger down  | Down            |
| Move finger left  | Left            |
| Move finger right | Right           |


### - Make sure your hand is clearly visible to the camera for best results.

---

## 🖥️ Game Layout

- Left Side: Live camera feed with hand tracking

- Right Side: Snake game area

---

## 📄 License

- This project is created for educational purposes and free to use.
