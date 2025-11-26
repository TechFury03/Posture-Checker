import cv2

#TODO we should probably just grab the visualization function chain from the package (for annotate there is already custom code added...)

# Display the frame with optional mirroring, resizing, and annotation.
def display_frame(
    frame,
    poses,
    scores,
    estimator, # has nice visualize() method
    annotate=False,
    mirror=True,
    resize_width=None,
):
    keypoints = poses[0]
    orig_h, orig_w = frame.shape[:2]
    if mirror:
        frame = cv2.flip(frame, 1)
        for keypoint in keypoints:
            keypoint[0] = orig_w - keypoint[0]

    if resize_width is not None and orig_w != resize_width:
        scale = resize_width / orig_w
        frame = cv2.resize(frame, (resize_width, int(orig_h * scale)), interpolation=cv2.INTER_AREA)
        for keypoint in keypoints:
            keypoint[0] = scale * keypoint[0]
            keypoint[1] = scale * keypoint[1]

    vis = estimator.visualize(frame, poses, scores, annotate=annotate)
    cv2.imshow("Posture Checker", vis)