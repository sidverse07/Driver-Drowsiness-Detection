
import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
import pygame
import os

from streamlit_webrtc import (
    webrtc_streamer,
    VideoProcessorBase,
    RTCConfiguration
)

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="DriveGuard AI",
    page_icon="🚗",
    layout="wide"
)

# --------------------------------
# BABY PINK THEME
# --------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #FFF1F7, #FCE7F3);
    color: #831843;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #9D174D !important;
}

p, label {
    color: #831843;
}

[data-testid="stSidebar"] {
    background: #FBCFE8;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 18px;
    border-radius: 15px;
    border: 1px solid #F9A8D4;
    box-shadow: 0 4px 12px rgba(190, 24, 93, 0.08);
}

[data-testid="stMetricValue"] {
    color: #BE185D;
    font-weight: bold;
}

div.stButton > button {
    background: #EC4899;
    color: white !important;
    border: none;
    border-radius: 12px;
    height: 45px;
    font-weight: bold;
}

div.stButton > button:hover {
    background: #BE185D;
    color: white !important;
}

[data-testid="stImage"] img {
    border-radius: 15px;
    border: 2px solid #F9A8D4;
}

hr {
    border-color: #F9A8D4;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# PROJECT HEADER
# --------------------------------

st.title("🚗 DRIVEGUARD AI")

st.markdown(
    "### Driver Drowsiness Detection System"
)

st.write(
    "Real-Time AI Powered Driver Monitoring "
    "using Computer Vision and Machine Learning."
)

st.divider()


# --------------------------------
# SIDEBAR SETTINGS
# --------------------------------

st.sidebar.title("⚙️ Control Panel")

st.sidebar.write("Driver Monitoring Settings")

threshold = st.sidebar.slider(
    "EAR Threshold",
    0.15, 0.40, 0.25, 0.01
)

closed_time = st.sidebar.slider(
    "Closed Eye Duration (seconds)",
    1, 5, 2
)

st.sidebar.info(
    "Keep your face visible to the camera."
)

st.sidebar.markdown("---")

st.sidebar.write("Technologies Used")

st.sidebar.write("• Python")
st.sidebar.write("• OpenCV")
st.sidebar.write("• MediaPipe")
st.sidebar.write("• NumPy")
st.sidebar.write("• Streamlit")


# --------------------------------
# ALARM INITIALIZATION
# --------------------------------

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

ALARM_PATH = os.path.join(
    BASE_DIR,
    "alarm.wav"
)

try:
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    if os.path.exists(ALARM_PATH):
        pygame.mixer.music.load(ALARM_PATH)
        ALARM_AVAILABLE = True
    else:
        ALARM_AVAILABLE = False

except Exception as e:
    ALARM_AVAILABLE = False
    st.warning(f"Alarm initialization issue: {e}")


# --------------------------------
# EYE LANDMARKS
# --------------------------------

LEFT_EYE = [33, 160, 158, 133, 153, 144]

RIGHT_EYE = [362, 385, 387, 263, 373, 380]

mp_face_mesh = mp.solutions.face_mesh


# --------------------------------
# EAR CALCULATION
# --------------------------------

def calculate_ear(points):

    A = np.linalg.norm(points[1] - points[5])

    B = np.linalg.norm(points[2] - points[4])

    C = np.linalg.norm(points[0] - points[3])

    if C == 0:
        return 0

    return (A + B) / (2.0 * C)


# --------------------------------
# VIDEO PROCESSOR
# --------------------------------

class DrowsinessProcessor(VideoProcessorBase):

    def __init__(self):

        self.face_mesh = mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.eye_closed_start = None

    def recv(self, frame):

        image = frame.to_ndarray(format="bgr24")

        h, w, _ = image.shape

        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        results = self.face_mesh.process(rgb)

        status = "NO FACE"

        ear = 0

        color = (0, 0, 255)

        if results.multi_face_landmarks:

            for face in results.multi_face_landmarks:

                landmarks = face.landmark

                left_points = np.array([
                    [landmarks[i].x * w,
                     landmarks[i].y * h]
                    for i in LEFT_EYE
                ])

                right_points = np.array([
                    [landmarks[i].x * w,
                     landmarks[i].y * h]
                    for i in RIGHT_EYE
                ])

                left_ear = calculate_ear(left_points)

                right_ear = calculate_ear(right_points)

                ear = (left_ear + right_ear) / 2.0

                # Draw eye landmarks

                for point in list(left_points) + list(right_points):

                    cv2.circle(
                        image,
                        tuple(point.astype(int)),
                        2,
                        (0, 255, 0),
                        -1
                    )

                # Drowsiness detection

                if ear < threshold:

                    if self.eye_closed_start is None:

                        self.eye_closed_start = time.time()

                    duration = (
                        time.time() - self.eye_closed_start
                    )

                    if duration >= closed_time:

                        status = "DROWSINESS ALERT!"

                        color = (0, 0, 255)

                        if ALARM_AVAILABLE:

                            if not pygame.mixer.music.get_busy():

                                pygame.mixer.music.play(-1)

                    else:

                        status = "EYES CLOSED"

                        color = (0, 255, 255)

                else:

                    self.eye_closed_start = None

                    status = "ALERT"

                    color = (0, 255, 0)

                    if ALARM_AVAILABLE:

                        if pygame.mixer.music.get_busy():

                            pygame.mixer.music.stop()

        else:

            self.eye_closed_start = None

            if ALARM_AVAILABLE:

                if pygame.mixer.music.get_busy():

                    pygame.mixer.music.stop()

        # Display EAR

        cv2.putText(
            image,
            f"EAR: {ear:.2f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        # Display Status

        cv2.putText(
            image,
            status,
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        return frame.from_ndarray(
            image,
            format="bgr24"
        )


# --------------------------------
# DASHBOARD METRICS
# --------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "EAR Threshold",
        f"{threshold:.2f}"
    )

with col2:
    st.metric(
        "Closed Eye Duration",
        f"{closed_time} sec"
    )

with col3:
    st.metric(
        "Alarm System",
        "Ready" if ALARM_AVAILABLE else "Not Available"
    )


st.divider()


# --------------------------------
# LIVE CAMERA MONITORING
# --------------------------------

st.subheader("📹 Live Camera Monitoring")

st.write(
    "Click START to activate live driver monitoring."
)

webrtc_ctx = webrtc_streamer(
    key="driveguard-camera",
    video_processor_factory=DrowsinessProcessor,
    rtc_configuration=RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    ),
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    async_processing=True
)


# --------------------------------
# MONITORING STATUS
# --------------------------------

if webrtc_ctx.state.playing:

    st.success("🟢 Camera Monitoring Active")

else:

    st.info("⚪ Camera Monitoring Stopped")


# --------------------------------
# ALARM INFORMATION
# --------------------------------

st.divider()

st.subheader("🔔 Alarm Information")

if ALARM_AVAILABLE:

    st.success("Alarm sound loaded successfully.")

else:

    st.warning(
        "alarm.wav not found. Please check your project folder."
    )


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.markdown(
    "<center>💗 DRIVEGUARD AI | "
    "Computer Vision Based Driver Monitoring System</center>",
    unsafe_allow_html=True
)
