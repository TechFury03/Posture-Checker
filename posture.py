from display import display_frame
import cv2
import math
from mediapipe.python.solutions.pose import PoseLandmark

def evaluate_posture(
    landmarks,
    frame,
    headless=False,
    annotate=False,
    mirror=False,
    resize_width=None
):
    if landmarks is not None:
        lm = landmarks.landmark

        # Extract key 2D points
        ear = lm[PoseLandmark.LEFT_EAR]
        shoulder = lm[PoseLandmark.LEFT_SHOULDER]
        hip = lm[PoseLandmark.LEFT_HIP]
        knee = lm[PoseLandmark.LEFT_KNEE]

        # Convert to normalized 2D coordinates
        def pt(lm): return (lm.x, lm.y)

        def angle(a, b, c):
            ab = (a[0]-b[0], a[1]-b[1])
            cb = (c[0]-b[0], c[1]-b[1])
            dot = ab[0]*cb[0] + ab[1]*cb[1]
            mag_ab = math.sqrt(ab[0]**2 + ab[1]**2)
            mag_cb = math.sqrt(cb[0]**2 + cb[1]**2)
            return math.degrees(math.acos(dot / (mag_ab * mag_cb)))

        # 1 Head alignment (horizontal distance)
        head_offset = abs(ear.x - shoulder.x)
        head_score = max(0, 100 - head_offset * 1000)  # tune scaling

        # 2 Torso angle (shoulder–hip–knee)
        torso_angle = angle(pt(shoulder), pt(hip), pt(knee))
        torso_score = max(0, 100 - abs(180 - torso_angle))

        # 3 Shoulder slouch (shoulder too far forward)
        shoulder_offset = abs(shoulder.x - hip.x)
        shoulder_score = max(0, 100 - shoulder_offset * 500)

        # Weighted posture score
        posture_score = 0.4 * head_score + 0.4 * torso_score + 0.2 * shoulder_score
        posture_score = int(max(0, min(100, posture_score)))

        # Draw result on frame
        cv2.putText(frame, f"Score: {posture_score}", (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Optionally show metrics
        cv2.putText(frame, f"Head: {int(head_score)}  Torso: {int(torso_score)}  Shoulder: {int(shoulder_score)}",
                    (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3) # outline
        cv2.putText(frame, f"Head: {int(head_score)}  Torso: {int(torso_score)}  Shoulder: {int(shoulder_score)}",
                    (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    if not headless:
        display_frame(
            frame,
            landmarks,
            annotate=annotate,
            mirror=mirror,
            resize_width=resize_width,
        )