import math
import cv2
from display import display_frame
from notification import notify_user
from messages import get_random_bad_posture_message, get_random_good_posture_message
import time

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

# State
current_zone = None
zone_enter_time = None
NOTIFY_DELAY = 3  # seconds
bad_posture_notified = False
good_posture_notified = False

def overlay_score(frame, score):
    global current_zone, zone_enter_time
    global bad_posture_notified, good_posture_notified

    h, w, _ = frame.shape
    bar_height = int(h * score / 100)

    # Determine zone
    if score < 50:
        zone = "bad"
        color = (0, 0, 255)
    elif score < 75:
        zone = "yellow"
        color = (0, 255, 255)
    else:
        zone = "good"
        color = (0, 255, 0)

    # Zone changed → reset timer
    now = time.time()
    if zone != current_zone:
        current_zone = zone
        zone_enter_time = now
        # Reset zone-specific flags
        bad_posture_notified = False
        good_posture_notified = False

    # Stay duration
    stayed = now - zone_enter_time

    # Trigger notifications **only after 3 seconds**
    if stayed >= NOTIFY_DELAY:
        if zone == "bad" and not bad_posture_notified:
            notify_user(
                title="Posture Checker",
                message=get_random_bad_posture_message(),
                duration=30
            )
            bad_posture_notified = True

        elif zone == "good" and not good_posture_notified:
            notify_user(
                title="Posture Checker",
                message=get_random_good_posture_message(),
                duration=30
            )
            good_posture_notified = True

    # Draw UI
    cv2.rectangle(frame, (w - 50, h - bar_height), (w - 20, h), color, -1)
    cv2.putText(frame, f"{int(score)}", (w - 70, h - bar_height - 10),
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
    max_good_distance = shoulder_width * 0.72

    # Compute score: smaller distance = better posture
    score = max(0, 100 * (distance / max_good_distance))
    score = min(score, 100)

    # Smooth score
    smoothed_scores["total"] = smooth_score(smoothed_scores.get("total"), score)

    # Overlay score only
    overlay_score(frame, smoothed_scores["total"])
    display_frame(frame, landmarks, annotate=annotate, headless=headless)

def smooth_plateau_score(angle, ideal_min, ideal_max, soft_limit=5, hard_drop=15):
    """
    Smooth scoring curve:
        - Full score inside [ideal_min, ideal_max]
        - Smooth sigmoid falloff outside
        - Steeper sigmoid falloff after soft_limit
    """

    # Inside plateau = full score
    if ideal_min <= angle <= ideal_max:
        return 100

    # Distance from nearest plateau edge
    if angle > ideal_max:
        diff = angle - ideal_max
    else:
        diff = ideal_min - angle

    # Soft falloff → smooth sigmoid (no jumps)
    hard_region = soft_limit + hard_drop

    # Normalized x in [0, 1]
    x = diff / hard_region
    x = max(0, min(x, 1))

    # Smooth logistic falloff curve
    k_soft = 10
    k_hard = 25

    if diff <= soft_limit:
        # Gentle slope
        score = 100 / (1 + math.exp(k_soft * (x - (soft_limit / hard_region))))
    else:
        # Steeper slope
        score = 100 / (1 + math.exp(k_hard * (x - (soft_limit / hard_region))))

    return max(0, min(100, score))



# Side-view
def evaluate_posture_side_view(landmarks, frame, annotate=False, mirror=True, resize_width=None, headless=False):
    if not landmarks:
        return

    h, w = frame.shape[:2]
    lm = landmarks.landmark

    ear = get_xy(lm[7], w, h)
    shoulder = get_xy(lm[11], w, h)
    hip = get_xy(lm[23], w, h)
    knee = get_xy(lm[25], w, h)

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
        cos_angle = max(-1, min(1, dot / (mag_ab * mag_cb)))
        return math.degrees(math.acos(cos_angle))

    neck_angle = angle(ear, shoulder, hip)
    back_angle = angle(shoulder, hip, knee)

    # Debug overlay
    cv2.putText(frame, f"Neck Angle: {int(neck_angle)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, f"Back Angle: {int(back_angle)}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Ideal ranges
    NECK_MIN = 135
    NECK_MAX = 150
    BACK_MIN = 90
    BACK_MAX = 115

    # New smooth scoring
    neck_score = smooth_plateau_score(neck_angle, NECK_MIN, NECK_MAX, soft_limit=5, hard_drop=15)
    back_score = smooth_plateau_score(back_angle, BACK_MIN, BACK_MAX, soft_limit=5, hard_drop=20)

    total_score = 0.5 * neck_score + 0.5 * back_score

    # Smooth using EMA
    smoothed_scores["total"] = smooth_score(smoothed_scores.get("total"), total_score)

    overlay_score(frame, smoothed_scores["total"])
    display_frame(frame, landmarks, annotate=annotate, headless=headless)

