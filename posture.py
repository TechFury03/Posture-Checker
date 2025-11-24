from display import display_frame

def evaluate_posture(
    frame,
    poses,
    scores,
    estimator,
    headless=False,
    annotate=False,
    mirror=True,
    resize_width=None
):
    if poses is not None: # This check is not correct (will never be none), but there is also not logic here so ¯\_(ツ)_/¯
        pass
    # TODO: Add posture evaluation logic here
    if not headless:
        display_frame(
            frame,
            poses,
            scores,
            estimator,
            annotate=annotate,
            mirror=mirror,
            resize_width=resize_width,
        )