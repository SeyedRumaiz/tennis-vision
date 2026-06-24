"""
Creates a player tracker using YOLOv8 to detect and track tennis players across video frames.

Video -> YOLOv8 Tracking -> Player IDs assigned -> Choose 2 players closest to court -> Remove spectators/referee

-> Track same players across frames -> Draw bounding boxes -> Return processed frames
"""

from ultralytics import YOLO 
import cv2
import pickle
import sys
sys.path.append('../')
from utils import measure_distance, get_center_of_bbox

class PlayerTracker:
    """
    Encapsulates all player tracking functionalities, including detection, 
    filtering, and drawing bounding boxes on video frames.
    """
    def __init__(self,model_path):
        self.model = YOLO(model_path)

    def choose_and_filter_players(self, court_keypoints, player_detections):
        """
        Only picks the tennis players.
        """
        player_detections_first_frame = player_detections[0]

        # Find the two actual players
        chosen_player = self.choose_players(court_keypoints, player_detections_first_frame)

        # Keep only those IDs
        filtered_player_detections = []
        for player_dict in player_detections:
            filtered_player_dict = {track_id: bbox for track_id, bbox in player_dict.items() if track_id in chosen_player}
            filtered_player_detections.append(filtered_player_dict)
        return filtered_player_detections

    def choose_players(self, court_keypoints, player_dict):
        """
        Determines which tracked people are actually on the tennis court.
        """
        distances = []
        for track_id, bbox in player_dict.items():

            # Get player center
            player_center = get_center_of_bbox(bbox)

            min_distance = float('inf')

            # Check distance to each court keypoint
            for i in range(0,len(court_keypoints),2):
                court_keypoint = (court_keypoints[i], court_keypoints[i+1])
                distance = measure_distance(player_center, court_keypoint)

                # Keep smallest distance.
                if distance < min_distance:
                    min_distance = distance
            distances.append((track_id, min_distance))
        
        # Sort the distances in ascending order
        distances.sort(key = lambda x: x[1])
        # Choose the first 2 tracks or the closest two.
        chosen_players = [distances[0][0], distances[1][0]]
        return chosen_players


    def detect_frames(self,frames, read_from_stub=False, stub_path=None):
        """
        Processes an entire video.
        """
        player_detections = []      # Stores the player detections for each frame.

        if read_from_stub and stub_path is not None:
            with open(stub_path, 'rb') as f:
                player_detections = pickle.load(f)
            return player_detections

        # Process each frame to detect players
        for frame in frames:

            # detect players in the current frame
            player_dict = self.detect_frame(frame)
            player_detections.append(player_dict)
        
        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                # Future becomes faster
                pickle.dump(player_detections, f)
        
        return player_detections

    def detect_frame(self,frame):
        """
        Processes one frame to detect players.
        """

        # Run tracker and persist to keep IDs consistent across frames
        results = self.model.track(frame, persist=True)[0]

        # Class names.
        id_name_dict = results.names

        player_dict = {}

        # Loop through detections
        for box in results.boxes:
            track_id = int(box.id.tolist()[0])

            # Bounding box
            result = box.xyxy.tolist()[0]
            object_cls_id = box.cls.tolist()[0]
            object_cls_name = id_name_dict[object_cls_id]
            if object_cls_name == "person":
                player_dict[track_id] = result
        
        # eg: {
        # 5:[100,200,250,600],
        # 8:[800,200,950,620]
        # }
        return player_dict

    def draw_bboxes(self,video_frames, player_detections):
        """
        Draws bounding boxes on the video frames for the detected players."""
        output_video_frames = []

        # Loop through frames.
        for frame, player_dict in zip(video_frames, player_detections):

            # Draw Bounding Boxes and loop through each player in the frame.
            for track_id, bbox in player_dict.items():
                x1, y1, x2, y2 = bbox

                # Text and rectangle above player
                cv2.putText(frame, f"Player ID: {track_id}",(int(bbox[0]),int(bbox[1] -10 )),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
            output_video_frames.append(frame)
        
        return output_video_frames
