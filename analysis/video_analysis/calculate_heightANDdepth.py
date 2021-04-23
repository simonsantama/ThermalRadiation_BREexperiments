import cv2

def heightANDdepth(flame, pixel_to_meters, data, roi):
    """
    This function calculates the flame height and thickness

    Parameters:
    ----------
    flame: contour of the flame
        np.ndarray
        
    pixel_to_meters: ratio of meters per pixel
        float
        
    data: needs to be imported. Dictionary that includes all observed data
          from each experiment
        dict
        
    roi: region of image. 
        np.ndarray

    Returns:
    --------
    flame_height_top: height of the top of the flame in pixels
        float
        
    flame_height_bottom: height of the bottom of the flame in pixels
        float
        
    flame_projection: horizontal projection of the tip of the flame in pixels
        float

    flame_depth_below: depth of flame in pixels 500 mm above the door
        float

    flame_depth_topdoor = depth of flame in pixels at the top of the door
        float
        
    flame_depth_above = depth of flame in pixels 500 mm above the door
        float
    """

    # define variables
    offset = 0.5

    # determine heights at which the depth of the flame will be measured
    height_offset = int(offset / pixel_to_meters)
    height_door = data["top_of_door"][0] - data["min_y_real"]
    height_below = int(height_door - height_offset)
    height_above = int(height_door + height_offset)

    # determine the top and bottom flame heights
    top_point = tuple(flame[flame[:, :, 0].argmax()][0])
    bottom_point = tuple(flame[flame[:, :, 0].argmin()][0])
    height_top = top_point[0]
    height_bottom = bottom_point[0]
    
    # determine the horizontal projection of the flame
    flame_projection = 0
    pt2 = top_point
    pt1 = (top_point[0], data["top_of_door"][1])
    flame_projection = abs(pt2[1] - pt1[1])

    # add a conditional to deal with contours detected on the floor
    if height_top < 300:
        height_top = 0
        height_bottom = 0
        flame_projection = 0
    else:
        # draw on the frame the top and bottom heights as well as the projection
        cv2.circle(roi, top_point, 10, (0, 0, 255), 3)
        cv2.circle(roi, bottom_point, 10, (0, 0, 255), 3)
        cv2.arrowedLine(roi,pt2,pt1,color = (51,153,255),thickness = 3)

    # calculate the flame depth at three different heights
    for i,height in enumerate([height_below, height_door, height_above]):
        
        """
        Initialize pt1 and pt2, otherwise the calculation of depth raises
        an error
        """
        pt1 = (0,0)
        pt2 = (0,0)
        
        for y_coordinate in range(roi.shape[0]):
            # start from the edge of roi and find where the flame ends
            inside_flame = cv2.pointPolygonTest(flame, (height, y_coordinate),
                                                False)
            # if the point is in the flame
            if inside_flame in [0,1]:
                pt1 = (height, y_coordinate)
                break
            
        for y_coordinate in range(roi.shape[0], 0, -1):
            # start from the door and find where the flame starts
            inside_flame = cv2.pointPolygonTest(flame, (height, y_coordinate),
                                                False)
            # if the point is in the flame
            if inside_flame in [0,1]:
                pt2 = (height, y_coordinate)
                break
            
        # draw the lines that indicate the depth that was measured on the image        
        cv2.arrowedLine(roi,pt2,pt1,color = (51,153,255),thickness = 3)
        depth = abs(pt2[1] - pt1[1])
        
        # assign the depth value to the corresponding variable        
        if i == 0:
            depth_below = depth
        if i == 1:
            depth_door = depth
        if i == 2:
            depth_above = depth
    
    return (height_top, height_bottom, flame_projection, depth_below,
            depth_door, depth_above)
    

