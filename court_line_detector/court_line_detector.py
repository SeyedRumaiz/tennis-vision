"""
This module contains the CourtLineDetector class which is responsible for:

1. Loading a trained court keypoint detection model.
2. Predicting tennis court keypoints from an image.
3. Drawing the detected keypoints on images or videos.

The model is based on ResNet50 and predicts 14 court keypoints.
Each keypoint contains an (x, y) coordinate.

14 keypoints × 2 coordinates = 28 output values.
"""

import torch
import torchvision.transforms as transforms
import cv2
from torchvision import models


class CourtLineDetector:
    """
    Detects tennis court keypoints using a trained ResNet50 model.

    Example:
        detector = CourtLineDetector("models/keypoints_model.pth")
        keypoints = detector.predict(frame)

    Output format:
        [
            x0, y0,
            x1, y1,
            x2, y2,
            ...
            x13, y13
        ]
    """

    def __init__(self, model_path):
        """
        Constructor.

        Parameters
        ----------
        model_path : str
            Path to the trained model weights file.
        """

        self.model = models.resnet50(pretrained=True)
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, 14*2) 
        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def predict(self, image):
        """
        Predicts court keypoints from the given image.

        Parameters
        ----------
        image : np.ndarray
            Input image in BGR format (as read by OpenCV).

        Returns
        -------
        numpy.ndarray
            Array containing 28 values:

            [
                x0, y0,
                x1, y1,
                ...
                x13, y13
            ]
        """
    
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Apply preprocessing transformations and add a batch dimension
        image_tensor = self.transform(image_rgb).unsqueeze(0)

        # Performance inference without tracking gradients since no training is involved.
        with torch.no_grad():
            outputs = self.model(image_tensor)
        keypoints = outputs.squeeze().cpu().numpy()

        # Original frame dimensions
        original_h, original_w = image.shape[:2]

        # Even indices are x-coordinates, odd indices are y-coordinates
        keypoints[::2] *= original_w / 224.0
        keypoints[1::2] *= original_h / 224.0

        return keypoints

    def draw_keypoints(self, image, keypoints):
        """
        Draw keypoints on an image.

        Parameters
        ----------
        image : numpy.ndarray
            Input image.

        keypoints : numpy.ndarray
            Predicted court keypoints.

        Returns
        -------
        numpy.ndarray
            Image with keypoints drawn.
        """
        
        # Loop through the keypoints and draw them on the image
        for i in range(0, len(keypoints), 2):
            x = int(keypoints[i])
            y = int(keypoints[i+1])

            # Draw point number above keypoint
            cv2.putText(image, str(i//2), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Red circle for keypoint
            cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

        return image
    
    def draw_keypoints_on_video(self, video_frames, keypoints):
        """
        Draw court keypoints on every frame in a video.

        Parameters
        ----------
        video_frames : list
            List containing all video frames.

        keypoints : numpy.ndarray
            Predicted court keypoints.

        Returns
        -------
        list
            Video frames with keypoints drawn.
        """

        output_video_frames = []

        # Proces every frame
        for frame in video_frames:
            frame = self.draw_keypoints(frame, keypoints)
            output_video_frames.append(frame)

        return output_video_frames
