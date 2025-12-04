import cv2
import mediapipe as mp

drawing = mp.solutions.drawing_utils
POSE_CONNECTIONS = mp.solutions.pose.POSE_CONNECTIONS

def annotate_frame(frame, landmarks):
    if landmarks is None:
        return frame

    h, w = frame.shape[:2]
    for i, lm in enumerate(landmarks.landmark):
        x = int(lm.x * w)
        y = int(lm.y * h)
        cv2.putText(frame, str(i), (x+2, y+2), cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, (255,255,255), 1)
    return frame

def display_frame(frame, landmarks, annotate=False, headless=False):
    if headless:
        return

    if landmarks is not None:
        drawing.draw_landmarks(
            frame,
            landmarks,
            POSE_CONNECTIONS
        )

    if annotate:
        frame = annotate_frame(frame, landmarks)

    cv2.imshow("Posture Checker", frame)