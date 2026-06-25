def convert_pixel_distance_to_meters(pixel_distance, refrence_height_in_meters, refrence_height_in_pixels):
    """
    This function converts a distance in pixels to meters using a reference 
    height in meters and its corresponding height in pixels.

    Parameters
    ----------
    pixel_distance : float
        The distance in pixels to be converted.
    refrence_height_in_meters : float
        The reference height in meters.
    refrence_height_in_pixels : float
        The reference height in pixels.

    Returns
    -------
    float
        The distance in meters.
    """
    return (pixel_distance * refrence_height_in_meters) / refrence_height_in_pixels

def convert_meters_to_pixel_distance(meters, refrence_height_in_meters, refrence_height_in_pixels):
    """
    This function converts a distance in meters to pixels using a reference
    height in meters and its corresponding height in pixels.

    Parameters
    ----------
    meters : float
        The distance in meters to be converted.
    refrence_height_in_meters : float
        The reference height in meters.
    refrence_height_in_pixels : float
        The reference height in pixels.

    Returns
    -------
    float
        The distance in pixels.
    """
    return (meters * refrence_height_in_pixels) / refrence_height_in_meters
