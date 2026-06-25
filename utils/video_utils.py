import cv2


def read_video(video_path):
    """
    Read a video file and return all frames as a list.

    This function opens a video file using OpenCV and reads each frame
    sequentially until the end of the video is reached.

    Parameters
    ----------
    video_path : str
        Path to the input video file.

    Returns
    -------
    list
        A list containing all video frames as NumPy arrays.

    Notes
    -----
    Each frame is represented as a NumPy array with shape:

        (height, width, channels)

    where:
        height  -> number of pixels vertically
        width   -> number of pixels horizontally
        channels -> usually 3 (Blue, Green, Red)

    Example
    -------
    frames = read_video("input_videos/input_video.mp4")

    print(len(frames))
    # Output: 750

    print(frames[0].shape)
    # Output: (720, 1280, 3)
    """

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Store all frames here
    frames = []

    # Continue reading until there are no frames left
    while True:

        # Read one frame from the video
        ret, frame = cap.read()

        # ret is False when the video ends or reading fails
        if not ret:
            break

        # Store frame in memory
        frames.append(frame)

    # Release the video resource
    cap.release()

    return frames


def save_video(output_video_frames, output_video_path):
    """
    Save a list of frames as a video file.

    This function takes processed frames and writes them into
    a video file using OpenCV's VideoWriter.

    Parameters
    ----------
    output_video_frames : list
        List of video frames to save.

    output_video_path : str
        Path where the output video should be written.

    Returns
    -------
    None

    Notes
    -----
    The video is saved using the MJPG codec at 24 FPS.

    FPS (Frames Per Second):
        24 FPS means 24 images are displayed every second.

    Video dimensions are automatically obtained from the
    first frame in the list.

    Example
    -------
    save_video(
        processed_frames,
        "output_videos/output_video.avi"
    )
    """

    # Create the codec identifier.
    # MJPG = Motion JPEG compression format
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")

    # Create video writer object
    out = cv2.VideoWriter(
        output_video_path,                 # Output file location
        fourcc,                            # Video codec
        24,                                # Frames per second
        (
            output_video_frames[0].shape[1],  # Width
            output_video_frames[0].shape[0],  # Height
        ),
    )

    # Write every frame into the video file
    for frame in output_video_frames:
        out.write(frame)

    # Finalize and close the video file
    out.release()
