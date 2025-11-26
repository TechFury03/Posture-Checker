import cv2
import mediapipe as mp

# Annotate landmarks in a frame with their corresponding index numbers.
# For more information on MediaPipe Pose Landmarker, visit:
# https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
def annotate_frame(
    frame, 
    landmarks,
):
    for i, lm in enumerate(landmarks.landmark):
        x = int(lm.x * frame.shape[1])
        y = int(lm.y * frame.shape[0])
        cv2.putText(frame, str(i), (x+2, y+2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
    return frame

# Display the frame with optional mirroring, resizing, and annotation.    
def display_frame(
    frame, 
    landmarks,
    annotate=False,
    mirror=True,
    resize_width=None,
):
    if mirror:
        frame = cv2.flip(frame, 1)
        if landmarks is not None:
            for lm in landmarks.landmark:
                lm.x = 1 - lm.x  # flip horizontally

    orig_h, orig_w = frame.shape[:2]
    if resize_width is not None and orig_w != resize_width:
        scale = resize_width / orig_w
        frame = cv2.resize(frame, (resize_width, int(orig_h * scale)), interpolation=cv2.INTER_AREA)
    
    # Draw connections (skeleton lines) and landmarks (points)
    mp.solutions.drawing_utils.draw_landmarks(
        frame,
        landmarks,
        mp.solutions.pose.POSE_CONNECTIONS,
    )
    
    if annotate and landmarks is not None:
        frame = annotate_frame(frame, landmarks)
        
    cv2.imshow("Posture Checker", frame)