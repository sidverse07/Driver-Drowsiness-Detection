# 🚗 Driver Drowsiness Detection System

## 📌 About the Project
The Driver Drowsiness Detection System is a real-time project that detects whether a driver is feeling sleepy or not using a webcam.

If the driver's eyes remain closed for more than 2 seconds, the system detects drowsiness and plays an alarm to alert the driver.

## 🎯 Objectives
- Detect the driver's face and eyes.
- Monitor eye movements in real time.
- Detect drowsiness using Eye Aspect Ratio (EAR).
- Generate an alarm when drowsiness is detected.

## 🛠️ Technologies Used
- Python
- OpenCV
- MediaPipe
- NumPy
- Pygame
- Streamlit

## 🧠 Algorithms and Techniques
- MediaPipe Face Mesh
- Eye Aspect Ratio (EAR)
- Euclidean Distance
- Threshold-based Classification
- Time-based Drowsiness Detection

## ⚙️ How It Works
1. Webcam captures the driver's face.
2. MediaPipe detects facial landmarks.
3. Eye Aspect Ratio (EAR) is calculated.
4. EAR is compared with the threshold value (0.25).
5. If eyes remain closed for more than 2 seconds, an alarm is triggered.

## ▶️ How to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/sidverse07/Driver-Drowsiness-Detection.git
```

### 2. Open Project Folder
```bash
cd Driver-Drowsiness-Detection
```

### 3. Create Virtual Environment
```bash
python -m venv venv
```

### 4. Activate Environment (Windows)
```bash
venv\Scripts\activate
```

### 5. Install Requirements
```bash
pip install -r requirements.txt
```

### 6. Run Dashboard
```bash
streamlit run app.py
```

## ✨ Features
- Real-time face and eye detection.
- Drowsiness detection.
- Audio alarm alert.
- Web-based dashboard.

## 🔮 Future Scope
- GPS location tracking.
- Mobile application integration.
- Emergency notifications.
- Improved low-light detection.

## 📌 GitHub Repository
https://github.com/sidverse07/Driver-Drowsiness-Detection