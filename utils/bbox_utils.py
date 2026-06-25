def get_center_of_bbox(bbox):
    """
    Calculate the center point of a bounding box.

    A bounding box is represented as:
        [x1, y1, x2, y2]

    where:
        x1, y1 -> coordinates of the top-left corner
        x2, y2 -> coordinates of the bottom-right corner

    Parameters:
        bbox (list or tuple): Bounding box coordinates in the format
                              [x1, y1, x2, y2].

    Returns:
        tuple:
            (center_x, center_y) coordinates of the center point.

    Example:
        bbox = [100, 50, 200, 250]

        center_x = (100 + 200) / 2 = 150
        center_y = (50 + 250) / 2 = 150

        Returns:
            (150, 150)
    """

    # Extract coordinates from bounding box
    x1, y1, x2, y2 = bbox

    # Compute horizontal center
    center_x = int((x1 + x2) / 2)

    # Compute vertical center
    center_y = int((y1 + y2) / 2)

    return (center_x, center_y)


def measure_distance(p1, p2):
    """
    Calculate the Euclidean distance between two points.

    Uses the distance formula:

        distance = sqrt((x2 - x1)^2 + (y2 - y1)^2)

    Parameters:
        p1 (tuple): First point as (x, y)
        p2 (tuple): Second point as (x, y)

    Returns:
        float:
            Distance between the two points in pixels.

    Example:
        p1 = (10, 20)
        p2 = (13, 24)

        distance = sqrt((13-10)^2 + (24-20)^2)
                 = sqrt(9 + 16)
                 = sqrt(25)
                 = 5
    """

    return ((p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2) ** 0.5


def get_foot_position(bbox):
    """
    Estimate the foot position of a detected person.

    The foot position is assumed to be the center of the bottom edge
    of the bounding box.

    This is commonly used in sports analytics because the player's
    feet represent their actual location on the court.

    Parameters:
        bbox (list or tuple): Bounding box coordinates
                              [x1, y1, x2, y2].

    Returns:
        tuple:
            (x, y) coordinates of the foot position.

    Example:
        bbox = [100, 50, 200, 250]

        foot_x = (100 + 200) / 2 = 150
        foot_y = 250

        Returns:
            (150, 250)
    """

    x1, y1, x2, y2 = bbox

    # Horizontal center of the box
    foot_x = int((x1 + x2) / 2)

    # Bottom of the box represents the player's feet
    foot_y = y2

    return (foot_x, foot_y)


def get_closest_keypoint_index(point, keypoints, keypoint_indices):
    """
    Find the court keypoint that is vertically closest to a given point.

    The comparison uses only the Y coordinate difference because
    in many sports applications (such as tennis), we care more about
    which horizontal court line the player is nearest to.

    Parameters:
        point (tuple):
            Target point as (x, y).

        keypoints (list):
            Flattened list of keypoint coordinates:

                [x1, y1, x2, y2, x3, y3, ...]

        keypoint_indices (list):
            List of indices of candidate keypoints to search.

    Returns:
        int:
            Index of the closest keypoint.

    Example:
        keypoints = [
            100, 50,    # keypoint 0
            100, 200,   # keypoint 1
            100, 350    # keypoint 2
        ]

        point = (120, 180)

        Vertical distances:
            keypoint 0 -> |180 - 50|  = 130
            keypoint 1 -> |180 - 200| = 20
            keypoint 2 -> |180 - 350| = 170

        Returns:
            1
    """

    # Start with infinity so that any real distance is smaller
    closest_distance = float('inf')

    # Assume first candidate is the closest initially
    closest_keypoint_index = keypoint_indices[0]

    for keypoint_index in keypoint_indices:

        # Extract x and y coordinates of current keypoint
        keypoint = (
            keypoints[keypoint_index * 2],
            keypoints[keypoint_index * 2 + 1]
        )

        # Compare only vertical distance
        distance = abs(point[1] - keypoint[1])

        # Update if this keypoint is closer
        if distance < closest_distance:
            closest_distance = distance
            closest_keypoint_index = keypoint_index

    return closest_keypoint_index


def get_height_of_bbox(bbox):
    """
    Calculate the height of a bounding box.

    Parameters:
        bbox (list or tuple):
            Bounding box coordinates [x1, y1, x2, y2].

    Returns:
        int or float:
            Height of the bounding box in pixels.

    Example:
        bbox = [100, 50, 200, 250]

        height = 250 - 50 = 200 pixels
    """

    return bbox[3] - bbox[1]


def measure_xy_distance(p1, p2):
    """
    Calculate horizontal and vertical distances separately.

    Unlike measure_distance(), this function does not calculate
    the diagonal distance.

    Parameters:
        p1 (tuple): First point as (x, y)
        p2 (tuple): Second point as (x, y)

    Returns:
        tuple:
            (x_distance, y_distance)

    Example:
        p1 = (100, 50)
        p2 = (150, 120)

        x_distance = |150 - 100| = 50
        y_distance = |120 - 50| = 70

        Returns:
            (50, 70)
    """

    x_distance = abs(p1[0] - p2[0])
    y_distance = abs(p1[1] - p2[1])

    return (x_distance, y_distance)
