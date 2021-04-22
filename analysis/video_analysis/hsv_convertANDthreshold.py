import cv2

def convertANDthreshold(roi, threshold_value = 230):
    """
    This function takes an RGB image (roi), converts the image to HSV, applies threshold and determines contours
    
    The threshold is hard-coded to optimize the identification of a flame in the BRE experiments videos.

    Parameters:
    ----------
    img: skimage array. RGB  image.
        np.ndarray
        
    threshold_value: threshold to be applied to the value channel after conversion to the HSV color space
        int
        
    Returns:
	--------
	img: binary image (roi) threhsolded
        np.ndarray
    flame: all identified contours
        list
    """
    
    # convert to hsv and extract value channel
    hsv_image = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    _,_,value_channel = cv2.split(hsv_image)
    
    # apply filters and threshold
    blurred = cv2.GaussianBlur(value_channel, (11, 11), 0)
    _, thresh = cv2.threshold(blurred, threshold_value, 255, cv2.THRESH_BINARY)
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)
    
    # find contours
    _,contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    
    return thresh, contours
