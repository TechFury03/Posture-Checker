import argparse
import cv2
import mediapipe as mp
from posture import evaluate_posture, evaluate_posture_side_view
from notification import notify_user

def main(camera_idx=0, mirror=True, resize_width=960, annotate=False, headless=False, initial_view="front"):
    current_view = initial_view.lower()
    view_functions = {
        "front": evaluate_posture,
        "side": evaluate_posture_side_view
    }

    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(camera_idx)
    if not cap.isOpened():
        print(f"Unable to open camera {camera_idx}")
        return

    print("Press 'v' to toggle view between front and side. Press 'q' or ESC to quit.")

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

            # Convert to RGB for MediaPipe
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)

            landmarks = results.pose_landmarks

            # Call the correct posture evaluation function
            callback_func = view_functions[current_view]
            callback_func(
                landmarks, 
                frame, 
                annotate=annotate, 
                headless=headless, 
                mirror=mirror, 
                resize_width=resize_width
            )

            if not headless:
                # Display current view on the frame
                cv2.putText(frame, f"View: {current_view.capitalize()}",
                            (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.imshow("Posture Checker", frame)

            # Handle key inputs
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
            elif key == ord('v'):
                current_view = "side" if current_view == "front" else "front"
                print(f"Switched view to: {current_view.capitalize()}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Posture Checker with view toggle")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default 0)")
    parser.add_argument("--no-mirror", action="store_true", help="Disable mirroring")
    parser.add_argument("--width", type=int, default=960, help="Resize width")
    parser.add_argument("--annotate", action="store_true", help="Show landmark indices")
    parser.add_argument("--headless", action="store_true", help="Run without GUI window")
    parser.add_argument("--view", choices=["front", "side"], default="front", help="Initial camera view")

    args = parser.parse_args()

    notify_user("Posture Checker", f"Starting in {args.view} view...", duration=5)

    main(
        camera_idx=args.camera,
        mirror=(not args.no_mirror),
        resize_width=args.width,
        annotate=args.annotate,
        headless=args.headless,
        initial_view=args.view
    )
