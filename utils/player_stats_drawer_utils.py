import cv2


def draw_player_stats(output_video_frames, player_stats):
    """
    Draw player statistics on every frame of the output video.

    This function creates a statistics panel in the
    bottom-right area of each frame and displays:

    - Current shot speed of both players
    - Current movement speed of both players
    - Average shot speed of both players
    - Average movement speed of both players

    Parameters
    ----------
    output_video_frames : list
        List containing all video frames as NumPy arrays.

    player_stats : pandas.DataFrame
        DataFrame containing frame-by-frame statistics.

        Expected columns:

        - player_1_last_shot_speed
        - player_2_last_shot_speed
        - player_1_last_player_speed
        - player_2_last_player_speed
        - player_1_average_shot_speed
        - player_2_average_shot_speed
        - player_1_average_player_speed
        - player_2_average_player_speed

    Returns
    -------
    list
        List of frames with the statistics overlay drawn on them.
    """

    # Iterate through every row in the statistics DataFrame.
    # Each row corresponds to a video frame.
    for index, row in player_stats.iterrows():

        # Current frame statistics

        # Speed of the most recent shot hit by each player
        player_1_shot_speed = row["player_1_last_shot_speed"]
        player_2_shot_speed = row["player_2_last_shot_speed"]

        # Current running speed of each player
        player_1_speed = row["player_1_last_player_speed"]
        player_2_speed = row["player_2_last_player_speed"]

        # Average statistics

        # Average shot speed over the entire match so far
        avg_player_1_shot_speed = row["player_1_average_shot_speed"]
        avg_player_2_shot_speed = row["player_2_average_shot_speed"]

        # Average player movement speed
        avg_player_1_speed = row["player_1_average_player_speed"]
        avg_player_2_speed = row["player_2_average_player_speed"]

        # Get the current frame
        frame = output_video_frames[index]

        # Statistics panel dimensions

        # Width and height of the stats box
        width = 350
        height = 230

        # Position the box near the bottom-right corner
        start_x = frame.shape[1] - 400
        start_y = frame.shape[0] - 500

        end_x = start_x + width
        end_y = start_y + height

        # Create a semi-transparent background

        # Create a copy of the frame for overlay blending
        overlay = frame.copy()

        # Draw a filled black rectangle
        cv2.rectangle(overlay, (start_x, start_y), (end_x, end_y), (0, 0, 0), -1)

        # Transparency factor
        # 0.0 -> invisible
        # 1.0 -> fully opaque
        alpha = 0.5

        # Blend overlay and original frame
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        output_video_frames[index] = frame

        # Draw table header

        text = "     Player 1     Player 2"

        output_video_frames[index] = cv2.putText(
            output_video_frames[index],
            text,
            (start_x + 80, start_y + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

        # Current shot speed

        text = "Shot Speed"

        output_video_frames[index] = cv2.putText(
            output_video_frames[index],
            text,
            (start_x + 10, start_y + 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
        )

        text = f"{player_1_shot_speed:.1f} km/h    " f"{player_2_shot_speed:.1f} km/h"

        output_video_frames[index] = cv2.putText(
            output_video_frames[index],
            text,
            (start_x + 130, start_y + 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2,
        )

        # Current player movement speed

        text = "Player Speed"

        output_video_frames[index] = cv2.putText(
            output_video_frames[index],
            text,
            (start_x + 10, start_y + 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
        )

        text = f"{player_1_speed:.1f} km/h    " f"{player_2_speed:.1f} km/h"

        output_video_frames[index] = cv2.putText(
            output_video_frames[index],
            text,
            (start_x + 130, start_y + 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2,
        )

        # Average shot speed

        text = "avg. S. Speed"

        output_video_frames[index] = cv2.putText(
            output_video_frames[index],
            text,
            (start_x + 10, start_y + 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
        )

        text = (
            f"{avg_player_1_shot_speed:.1f} km/h    "
            f"{avg_player_2_shot_speed:.1f} km/h"
        )

        output_video_frames[index] = cv2.putText(
            output_video_frames[index],
            text,
            (start_x + 130, start_y + 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2,
        )

        # Average movement speed

        text = "avg. P. Speed"

        output_video_frames[index] = cv2.putText(
            output_video_frames[index],
            text,
            (start_x + 10, start_y + 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1,
        )

        text = f"{avg_player_1_speed:.1f} km/h    " f"{avg_player_2_speed:.1f} km/h"

        output_video_frames[index] = cv2.putText(
            output_video_frames[index],
            text,
            (start_x + 130, start_y + 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2,
        )

    # Return all processed frames
    return output_video_frames
