import cv2
import mediapipe as mp

# Detect pose landmarks from the camera feed and invoke a callback with the results.
def detectLandmarks(
    camera_idx: int = 0, 
    callback = None
):
    # MediaPipe pose setup
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(camera_idx)
    if not cap.isOpened():
        print(f"Unable to open camera {camera_idx}")
        return

    # Use default Pose with a good balance: model_complexity=1, enable smoothing
    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame from camera")
                break

            # Convert the BGR frame to RGB for MediaPipe
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            if callback is not None:
                callback(results.pose_landmarks, frame)
            
            # Exit loop when pressing 'q' or 'ESC' or closing the window
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27 or cv2.getWindowProperty("Posture Checker", cv2.WND_PROP_VISIBLE) < 1:
                break
                
    cap.release()
    cv2.destroyAllWindows()
