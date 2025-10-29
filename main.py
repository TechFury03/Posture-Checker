import argparse
from landmark import detectLandmarks
from posture import evaluate_posture
from functools import partial

# Entry point of the program    
def main(
    camera_idx: int = 0, 
    mirror: bool = True, 
    resize_width: int | None = 960, 
    annotate: bool = False,
    headless: bool = False,
):
    callback = partial(
        evaluate_posture, 
        headless=headless, 
        annotate=annotate, 
        mirror=mirror, 
        resize_width=resize_width
    )
    
    # Start detection loop
    detectLandmarks(
        camera_idx=camera_idx, 
        callback=callback
    )

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description="Draw skeleton on webcam using MediaPipe + OpenCV")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default 0)")
    parser.add_argument("--no-mirror", action="store_true", help="Do not mirror the webcam image")
    parser.add_argument("--width", type=int, default=0, help="Resize frame width (helps performance)")
    parser.add_argument("--annotate", action="store_true", help="Annotate landmark indices for debugging")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode (no GUI)")
    args = parser.parse_args()

    width = args.width if args.width > 0 else None
    main(
        camera_idx=args.camera, 
        mirror=(not args.no_mirror), 
        resize_width=width, 
        annotate=args.annotate,
        headless=args.headless    
    )
