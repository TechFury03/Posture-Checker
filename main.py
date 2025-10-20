import argparse
import cv2
import mediapipe as mp

def main(
    camera_idx: int = 0, 
    mirror: bool = True, 
    resize_width: int | None = 960, 
    annotate: bool = False
):
    # MediaPipe pose setup
    mp_pose = mp.solutions.pose
    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(camera_idx)
    if not cap.isOpened():
        print(f"Unable to open camera {camera_idx}")
        return

    # Use default Pose with a good balance: model_complexity=1, enable smoothing
    with mp_pose.Pose(static_image_mode=False,
                      model_complexity=1,
                      enable_segmentation=False,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame from camera")
                break

            if mirror:
                frame = cv2.flip(frame, 1)

            orig_h, orig_w = frame.shape[:2]
            if resize_width is not None and orig_w != resize_width:
                scale = resize_width / orig_w
                frame = cv2.resize(frame, (resize_width, int(orig_h * scale)), interpolation=cv2.INTER_AREA)

            # Convert the BGR frame to RGB for MediaPipe
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Process
            results = pose.process(rgb)

            # Draw skeleton if pose landmarks detected
            if results.pose_landmarks:
                # Draw connections (skeleton lines) and landmarks (points)
                mp_draw.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                )

                # Draw small id labels (landmark index) for debugging
                # https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker
                if annotate:
                    for i, lm in enumerate(results.pose_landmarks.landmark):
                        x = int(lm.x * frame.shape[1])
                        y = int(lm.y * frame.shape[0])
                        cv2.putText(frame, str(i), (x+2, y+2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)

            # Show
            cv2.imshow("Posture Checker", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Draw skeleton on webcam using MediaPipe + OpenCV")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default 0)")
    parser.add_argument("--no-mirror", action="store_true", help="Do not mirror the webcam image")
    parser.add_argument("--width", type=int, default=0, help="Resize frame width (helps performance)")
    parser.add_argument("--annotate", action="store_true", help="Annotate landmark indices for debugging")
    args = parser.parse_args()

    width = args.width if args.width > 0 else None
    main(camera_idx=args.camera, mirror=(not args.no_mirror), resize_width=width, annotate=args.annotate)
