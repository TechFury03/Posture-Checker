def detectLandmarks(camera_idx=0, callback=None, resize_width=None, mirror=True, return_capture=False):
    import cv2
    import mediapipe as mp

    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(camera_idx)
    if not cap.isOpened():
        print(f"Unable to open camera {camera_idx}")
        return None

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

            if mirror:
                frame = cv2.flip(frame, 1)

            if resize_width is not None and frame.shape[1] != resize_width:
                scale = resize_width / frame.shape[1]
                frame = cv2.resize(frame, (resize_width, int(frame.shape[0] * scale)))

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            if callback:
                callback(results.pose_landmarks, frame)

            if return_capture:
                return cap  # Return capture object to main loop for keyboard control
