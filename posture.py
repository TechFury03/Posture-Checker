from display import display_frame

def evaluate_posture(
    landmarks, 
    frame, 
    headless=False, 
    annotate=False, 
    mirror=True, 
    resize_width=None
):
    if landmarks is not None:
        pass
    # TODO: Add posture evaluation logic here
    
    if not headless:
        display_frame(
            frame, 
            landmarks,
            annotate=annotate,
            mirror=mirror,
            resize_width=resize_width,
        )