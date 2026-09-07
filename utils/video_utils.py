import cv2

def read_video(video_path):
    """Read video frames from *video_path* safely, limiting memory usage.
    Returns a list of frames (numpy arrays). If the video cannot be opened,
    raises a ``ValueError`` with a descriptive message.
    """
    # Attempt to open video using FFMPEG backend if available for better codec support
    if hasattr(cv2, "CAP_FFMPEG"):
        cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    else:
        cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Unable to open video file: {video_path}")
    frames = []
    MAX_FRAMES = 300  # safety cap to keep memory consumption reasonable
    while True:
        try:
            # Read the next frame; ret indicates success, frame may be None on failure
            ret, frame = cap.read()
            if not ret or frame is None:
                break
        except Exception as e:
            # Log and break out if OpenCV raises an unexpected error
            print(f"Error reading frame: {e}")
            break
        frames.append(frame)
        if len(frames) >= MAX_FRAMES:
            print(f"Warning: video contains more than {MAX_FRAMES} frames; processing only the first {MAX_FRAMES} to avoid OOM.")
            break
    cap.release()
    if not frames:
        raise ValueError("Video file contains no frames or could not be decoded.")
    return frames

def save_video(ouput_video_frames,output_video_path):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, 24, (ouput_video_frames[0].shape[1], ouput_video_frames[0].shape[0]))
    for frame in ouput_video_frames:
        out.write(frame)
    out.release()


def save_video_mp4(output_video_frames, output_video_path, fps=24):
    """Save frames as an H.264-compatible MP4 that Streamlit's st.video() can play."""
    if not output_video_frames:
        return
    try:
        import imageio
        # imageio expects RGB format (OpenCV frames are BGR)
        rgb_frames = [cv2.cvtColor(f, cv2.COLOR_BGR2RGB) for f in output_video_frames]
        imageio.mimwrite(output_video_path, rgb_frames, fps=fps, codec='libx264', quality=8)
        return
    except Exception as e:
        print(f"imageio save notice ({e}); falling back to OpenCV VideoWriter")

    h, w = output_video_frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (w, h))
    for frame in output_video_frames:
        out.write(frame)
    out.release()


def downscale_frame(frame, width: int, height: int):
    """Resize a frame to the given width and height using a memory‑efficient interpolation.
    Returns a new frame. The original ``frame`` is not modified; callers should release it after use.
    This function also ensures the resulting frame does not exceed a safe pixel count
    (default 800 000 pixels) to prevent OpenCV memory‑allocation failures.
    """
    # Define a safe upper bound for total pixels (e.g., 800,000 ≈ 1280×625)
    MAX_PIXELS = 800_000
    # If the requested size exceeds the limit, scale it down proportionally
    if width * height > MAX_PIXELS:
        scale_factor = (MAX_PIXELS / (width * height)) ** 0.5
        width = max(1, int(width * scale_factor))
        height = max(1, int(height * scale_factor))
    # Use INTER_AREA for downscaling which reduces aliasing and memory overhead
    resized = cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)
    return resized

def should_process_frame(frame_idx: int, skip_interval: int) -> bool:
    """Return True if the frame at frame_idx should be processed based on skip_interval.
    skip_interval of 1 processes every frame.
    """
    return (frame_idx % skip_interval) == 0
