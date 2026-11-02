
import cv2
import mediapipe as mp
import numpy as np
import time
import pygame
import os

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh

# Eye landmark points
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# Settings
EAR_THRESHOLD = 0.25
CLOSED_EYE_TIME = 2

# Initialize Pygame Alarm
pygame.mixer.init()

if os.path.exists("alarm.wav"):
    pygame.mixer.music.load("alarm.wav")
else:
    print("Warning: alarm.wav file not found!")

# Calculate Eye Aspect Ratio
def calculate_ear(points):

    A = np.linalg.norm(points[1] - points[5])
    B = np.linalg.norm(points[2] - points[4])
    C = np.linalg.norm(points[0] - points[3])

    if C == 0:
        return 0

    ear = (A + B) / (2.0 * C)

    return ear


# Start Webcam
cap = cv2.VideoCapture(0)

eye_closed_start = None

try:
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        while True:

            ret, frame = cap.read()

            if not ret:
                print("Camera not detected!")
                break

            h, w, _ = frame.shape

            # Convert BGR to RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect face and eyes
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:

                for face in results.multi_face_landmarks:

                    landmarks = face.landmark

                    # Get left eye points
                    left_points = np.array([
                        [landmarks[i].x * w, landmarks[i].y * h]
                        for i in LEFT_EYE
                    ])

                    # Get right eye points
                    right_points = np.array([
                        [landmarks[i].x * w, landmarks[i].y * h]
                        for i in RIGHT_EYE
                    ])

                    # Calculate EAR
                    left_ear = calculate_ear(left_points)
                    right_ear = calculate_ear(right_points)

                    ear = (left_ear + right_ear) / 2.0

                    # Display eye landmarks
                    for point in left_points:
                        cv2.circle(
                            frame, tuple(point.astype(int)),
                            2, (0, 255, 0), -1
                        )

                    for point in right_points:
                        cv2.circle(
                            frame, tuple(point.astype(int)),
                            2, (0, 255, 0), -1
                        )

                    # Drowsiness Detection
                    if ear < EAR_THRESHOLD:

                        if eye_closed_start is None:
                            eye_closed_start = time.time()

                        closed_duration = time.time() - eye_closed_start

                        if closed_duration >= CLOSED_EYE_TIME:

                            status = "DROWSINESS ALERT!"
                            color = (0, 0, 255)

                            # Play alarm
                            if not pygame.mixer.music.get_busy():
                                pygame.mixer.music.play(-1)

                        else:
                            status = "Eyes Closed"
                            color = (0, 255, 255)

                    else:

                        eye_closed_start = None
                        status = "ALERT"
                        color = (0, 255, 0)

                        # Stop alarm
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.stop()

                    # Display EAR
                    cv2.putText(
                        frame,
                        f"EAR: {ear:.2f}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        2
                    )

                    # Display Status
                    cv2.putText(
                        frame,
                        status,
                        (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        2
                    )

            else:

                eye_closed_start = None

                # Stop alarm if face is not detected
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()

                cv2.putText(
                    frame,
                    "No Face Detected",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            # Display output
            cv2.imshow("Driver Drowsiness Detection", frame)

            # Press Q to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    print("Program Closed!")

import cv2
import mediapipe as mp
import numpy as np
import time
import pygame
import os

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh

# Eye landmark points
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# Settings
EAR_THRESHOLD = 0.25
CLOSED_EYE_TIME = 2

# Initialize Pygame Alarm
pygame.mixer.init()

if os.path.exists("alarm.wav"):
    pygame.mixer.music.load("alarm.wav")
else:
    print("Warning: alarm.wav file not found!")

# Calculate Eye Aspect Ratio
def calculate_ear(points):

    A = np.linalg.norm(points[1] - points[5])
    B = np.linalg.norm(points[2] - points[4])
    C = np.linalg.norm(points[0] - points[3])

    if C == 0:
        return 0

    ear = (A + B) / (2.0 * C)

    return ear


# Start Webcam
cap = cv2.VideoCapture(0)

eye_closed_start = None

try:
    with mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as face_mesh:

        while True:

            ret, frame = cap.read()

            if not ret:
                print("Camera not detected!")
                break

            h, w, _ = frame.shape

            # Convert BGR to RGB
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect face and eyes
            results = face_mesh.process(rgb)

            if results.multi_face_landmarks:

                for face in results.multi_face_landmarks:

                    landmarks = face.landmark

                    # Get left eye points
                    left_points = np.array([
                        [landmarks[i].x * w, landmarks[i].y * h]
                        for i in LEFT_EYE
                    ])

                    # Get right eye points
                    right_points = np.array([
                        [landmarks[i].x * w, landmarks[i].y * h]
                        for i in RIGHT_EYE
                    ])

                    # Calculate EAR
                    left_ear = calculate_ear(left_points)
                    right_ear = calculate_ear(right_points)

                    ear = (left_ear + right_ear) / 2.0

                    # Display eye landmarks
                    for point in left_points:
                        cv2.circle(
                            frame, tuple(point.astype(int)),
                            2, (0, 255, 0), -1
                        )

                    for point in right_points:
                        cv2.circle(
                            frame, tuple(point.astype(int)),
                            2, (0, 255, 0), -1
                        )

                    # Drowsiness Detection
                    if ear < EAR_THRESHOLD:

                        if eye_closed_start is None:
                            eye_closed_start = time.time()

                        closed_duration = time.time() - eye_closed_start

                        if closed_duration >= CLOSED_EYE_TIME:

                            status = "DROWSINESS ALERT!"
                            color = (0, 0, 255)

                            # Play alarm
                            if not pygame.mixer.music.get_busy():
                                pygame.mixer.music.play(-1)

                        else:
                            status = "Eyes Closed"
                            color = (0, 255, 255)

                    else:

                        eye_closed_start = None
                        status = "ALERT"
                        color = (0, 255, 0)

                        # Stop alarm
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.stop()

                    # Display EAR
                    cv2.putText(
                        frame,
                        f"EAR: {ear:.2f}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        2
                    )

                    # Display Status
                    cv2.putText(
                        frame,
                        status,
                        (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        color,
                        2
                    )

            else:

                eye_closed_start = None

                # Stop alarm if face is not detected
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()

                cv2.putText(
                    frame,
                    "No Face Detected",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            # Display output
            cv2.imshow("Driver Drowsiness Detection", frame)

            # Press Q to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    print("Program Closed!")