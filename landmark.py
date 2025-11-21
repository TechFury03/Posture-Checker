import cv2
import spinepose
from torch import cuda
from mp_wrapper import MPLandmarks

DEVICE = 'auto' if cuda.is_available() else 'cpu'
BACKEND = 'onnxruntime' #openvino (spinepose default) gave issues during testing
MODE = 'large' if cuda.is_available() else 'small'

# Detect pose landmarks from the camera feed and invoke a callback with the results.
def detectLandmarks(
    camera_idx: int = 0,
    callback = None
):
    # Initialize estimator (downloads ONNX model if not found locally)
    # check https://github.com/dfki-av/spinepose/blob/main/src/spinepose/tools/base_solution.py for baseclass of Estimator (most functionality found here)
    # TODO #4: look into estimator vs tracker for our application
    # Determines device and backend itself (device=auto), mode size needs to be set by us (else it uses large)
    estimator = spinepose.SpinePoseEstimator(
        mode=MODE,
        backend=BACKEND,
        device=DEVICE)

    cap = cv2.VideoCapture(camera_idx)
    if not cap.isOpened():
        print(f"Unable to open camera {camera_idx}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        keypoints, scores = estimator(rgb_img)

        # Wrap keypoints so old code keeps working
        # landmarks = MPLandmarks(keypoints, frame.shape)

        # if callback is not None:
        #     callback(landmarks, frame)

        # OPTIONAL: show visualized output
        vis = estimator.visualize(rgb_img, keypoints, scores)
        cv2.imshow("Raw SpinePose Output", cv2.cvtColor(vis, cv2.COLOR_RGB2BGR))

        if cv2.waitKey(1) & 0xFF in (ord('q'), 27):
            break
    cap.release()
    cv2.destroyAllWindows()
