import cv2
import spinepose
from torch import cuda
from keypoints_enum import keypoints_enum

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

        poses, scores = estimator(rgb_img)

        if callback is not None:
            callback(
                frame=frame,
                poses=poses[:1], # only the first person, TODO figure out to determine this is the "subject"
                scores=scores,
                estimator=estimator)

        if cv2.waitKey(1) & 0xFF in (ord('q'), 27):
            break
    cap.release()
    cv2.destroyAllWindows()

def print_dbg_info(keypoints, scores, i=-1):
    """
    Prints the coordinates and score of every joint (name, not index)
    """
    assert len(keypoints.shape) == 2 # make sure this is of just 1 person
    if (i >= 0):
      print(f"Frame {i}: ", end='')
    print(f"Detected {len(keypoints)} people")
    if (len(keypoints) > 0):
        print(f"  Found {len(keypoints[0])} joints in person 1: {keypoints[0]}")
        print(f"  Example joint (nose) 0 (x,y): {keypoints[0][0]}, score: {scores[0][0]}")
        print(f"  Left ankle (joint 15) (x,y): {keypoints[0][15]}, score: {scores[0][15]}")
        # all joints for person 1
        for j, kp in enumerate(keypoints[0]):
            print(f"    Joint {keypoints_enum[j]:<20} (x,y): {kp}, score: {scores[0][j]}")

def cap_and_hold_one_img(cap, estimator):
    # capture just 1 img (and keep that alive until esc is pressed):
    ret, frame = cap.read()
    if ret:
        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        keypoints, scores = estimator(rgb_img)
        print_dbg_info(keypoints, scores)
        vis = estimator.visualize(rgb_img, keypoints, scores)
        cv2.imshow("Raw SpinePose Output", cv2.cvtColor(vis, cv2.COLOR_RGB2BGR))
    while (True):
        k = cv2.waitKey(1)
        if k%256 == 27:
            break