import matplotlib.pyplot as plt
import numpy as np
import cv2

def createANDsave_plot(flame,roi,experiment, frame, image, heights, projection,
                       depths):
    """
    Creates a plot that includes the flame, its contour, height and depth and
    saves it.
    This is used for evaluating the performance of the algorithm.
    
    Parameters:
    ----------
    flame: contour of the flame
        np.ndarray
        
    roi: region of the image
        np.ndarray    
    
    experiment: name of the experiment
        str
    
    frame: number of the frame currently being analysed
        int
        
    image: image currently being analysed
        np.ndarray
        
    (height_top, height_bottom): tupple with top and bottom flame heights in pixels
        tuple
    
    projection: projection of the top of the flame outwards
        float
    
    (depth_below, depth_topdoor, depth_above): tupple with flame depths in pixels
        tuple
    
    Returns:
    -------
    None
    """
    
    height_top, height_bottom = np.round(heights, 2)
    projection = np.round(projection, 2)
    depth_below, depth_topdoor, depth_above = np.round(depths, 2)

    fig, ax = plt.subplots(1, 1, figsize=(16,9))
    fig.tight_layout()
    
    # add note that includes flame heights, projection and depths on each frame
    ax.text(200, 400, 
            (f"Top flame height = {height_top} m \nBottom flame heigh"
             f"t = {height_bottom} m \nTop flame projection = {projection}"
             f" m\nDepth 0.5 m below = {depth_below} m \nDepth top of doo"
             f"r = {depth_topdoor} m \nDepth 0.5 m above = {depth_above} m"), 
            fontsize=18, bbox=dict(facecolor="red", alpha=0.5), ma="left",
            ha="left")
    
    # draw flame contour
    if cv2.contourArea(flame) > 4500:
        cv2.drawContours(roi,[flame],0, (51,255,51),4)

        ellipse = cv2.fitEllipse(flame)
        cv2.ellipse(roi, ellipse, (0,255,0),3)

    ax.imshow(image)

    plt.savefig(f"{experiment}_frames_processed/{frame}.png")
    plt.close(fig)
    
    return None
