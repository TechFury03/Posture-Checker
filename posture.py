import math
import cv2
from display import display_frame
from notification import notify_user
from messages import get_random_bad_posture_message, get_random_good_posture_message

# EMA smoothing storage
smoothed_scores = {
    "total": None
}
ALPHA = 0.3  # smoothing factor for EMA

def get_xy(lm, w, h):
    return (lm.x * w, lm.y * h)

def smooth_score(prev, current):
    if prev is None:
        return current
    return ALPHA * current + (1 - ALPHA) * prev

bad_posture_notified = False
def overlay_score(frame, score):
    global bad_posture_notified
    h, w, _ = frame.shape
    bar_height = int(h * score / 100)

    # Color: red <50, yellow 50–75, green >75
    if score < 50:
        color = (0, 0, 255)
        if not bad_posture_notified:
            notify_user(
                title="Posture Checker", 
                message=get_random_bad_posture_message(), 
                duration=5
            )
            bad_posture_notified = True
    elif score < 75:
        color = (0, 255, 255)
    else:
        if bad_posture_notified:
            notify_user(
                title="Posture Checker", 
                message=get_random_good_posture_message(),
                duration=5
            )
            bad_posture_notified = False
        color = (0, 255, 0)

    cv2.rectangle(frame, (w-50, h-bar_height), (w-20, h), color, -1)
    cv2.putText(frame, f"{int(score)}", (w-70, h-bar_height-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

# Front-view
def evaluate_posture(landmarks, frame, annotate=False, mirror=True, resize_width=None, headless=False):
    """
    Front view posture based on nose-to-shoulder distance with dynamic scaling
    """
    
    if not landmarks:
        return
    
    h, w = frame.shape[:2]
    lm = landmarks.landmark

    # Nose and shoulders
    nose = get_xy(lm[0], w, h)
    left_shoulder = get_xy(lm[11], w, h)
    right_shoulder = get_xy(lm[12], w, h)

    # Midpoint between shoulders
    mid_shoulder = ((left_shoulder[0] + right_shoulder[0]) / 2,
                    (left_shoulder[1] + right_shoulder[1]) / 2)

    # Shoulder width as reference distance
    shoulder_width = math.sqrt((left_shoulder[0]-right_shoulder[0])**2 +
                                (left_shoulder[1]-right_shoulder[1])**2)

    # Distance from nose to shoulder midpoint
    dx = nose[0] - mid_shoulder[0]
    dy = nose[1] - mid_shoulder[1]
    distance = math.sqrt(dx**2 + dy**2)

    # Dynamic scaling factor
    max_good_distance = shoulder_width * 0.8

    # Compute score: smaller distance = better posture
    score = max(0, 100 * (distance / max_good_distance))
    score = min(score, 100)

    # Smooth score
    smoothed_scores["total"] = smooth_score(smoothed_scores.get("total"), score)

    # Overlay score only
    overlay_score(frame, smoothed_scores["total"])
    display_frame(frame, landmarks, annotate=annotate, headless=headless)

# Side-view
def evaluate_posture_side_view(landmarks, frame, annotate=False, mirror=True, resize_width=None, headless=False):
    """
    Side view posture evaluation for left side of the body
    """
    if not landmarks:
        return
    
    h, w = frame.shape[:2]
    lm = landmarks.landmark

    # Side view landmarks
    ear = get_xy(lm[7], w, h)
    shoulder = get_xy(lm[11], w, h)
    hip = get_xy(lm[23], w, h)
    knee = get_xy(lm[25], w, h)

    # Angle calculations
    def angle(a, b, c):
        ax, ay = a
        bx, by = b
        cx, cy = c
        ab = (ax - bx, ay - by)
        cb = (cx - bx, cy - by)
        dot = ab[0]*cb[0] + ab[1]*cb[1]
        mag_ab = math.sqrt(ab[0]**2 + ab[1]**2)
        mag_cb = math.sqrt(cb[0]**2 + cb[1]**2)
        if mag_ab * mag_cb == 0:
            return 0
        cos_angle = dot / (mag_ab * mag_cb)
        cos_angle = max(-1, min(1, cos_angle))
        return math.degrees(math.acos(cos_angle))

    neck_angle = angle(ear, shoulder, hip)
    back_angle = angle(shoulder, hip, knee)

    # Convert to score
    neck_score = max(0, 100 - abs(neck_angle - 180))
    back_score = max(0, 100 - abs(back_angle - 180))
    total_score = 0.5 * neck_score + 0.5 * back_score

    # Smooth score
    smoothed_scores["total"] = smooth_score(smoothed_scores.get("total"), total_score)

    # Overlay score only
    overlay_score(frame, smoothed_scores["total"])
    display_frame(frame, landmarks, annotate=annotate, headless=headless)
