"""
Main video analysis.
Calculates flame height and depth from the videos (converted to one image per frame)

image = np.array(:,:,3) --> image(depth_dimension, height_dimension, RGB)
Saves it in this same folder as un-smoothed data
"""

import cv2
import numpy as np
import os
import pickle
import pandas as pd

# import my own functions
from observed_data import properties
from hsv_convertANDthreshold import convertANDthreshold
from calculate_heightANDdepth import heightANDdepth
from contourplot_createANDsave import createANDsave_plot

# initialize variables
experiments = ["Alpha2", "Beta1", "Beta2", "Gamma"]
threshold_value = [180, 180, 180, 180]
door_height = 2.15

# only analyse one out of every 5 frames to decrease the computational cost
effective_fps = 5

# Create universal dictionary to contain all the data (except for contours)
Flame_Dimensions = {}

for i, experiment in enumerate(experiments):
    print(f"Calculating for experiment ... {experiment}")
    
    # extract the properties for this experiment
    data = properties[experiment]

    # determine ratio of pixels per meter
    pixel_to_meters = door_height / data["door_height_px"]
    
    # initialize the variables for this experiment
    flame_contours = []
    flame_height_top = np.zeros(len(os.listdir(f"{experiment}_frames/")))
    flame_height_bottom = np.zeros_like(flame_height_top)
    flame_projection = np.zeros_like(flame_height_top)
    flame_area = np.zeros_like(flame_height_top)
    
    flame_depth_below = np.zeros_like(flame_height_top)
    flame_depth_above = np.zeros_like(flame_height_top)
    flame_depth_topdoor = np.zeros_like(flame_height_top)
    flame_depth_above = np.zeros_like(flame_height_top)
    flame_characteristic_length = np.zeros_like(flame_height_top)
    flame_perimeter = np.zeros_like(flame_height_top)
    flame_ellipse_length = np.zeros_like(flame_height_top)
    flame_ellipse_angle = np.zeros_like(flame_height_top)
    
    # iterate over every frame
    for frame_name in os.listdir(f"{experiment}_frames/"):
        frame = int(frame_name.split(".")[0].split("-")[1].split("e")[1])
        
        # don't do anything before flashover
        if frame < data["start_externalflaming"] * effective_fps:
            continue
        
        # don't do anything for Beta1 after flameout (it doesn't re-ignite) - 21 minutes
        if experiment == "Beta1" and frame > 6300:
            continue
        
        # show the frame under analysis
        print(frame)
        
        # ---- for debugging
#        if frame < 3000:
#            continue
#        if frame > 5000:
#            break
        # ----
        
        # load image
        image = cv2.imread(f"{experiment}_frames/{frame_name}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # define region of interest
        roi = image[data["min_x_real"]:data["max_x_real"],data["min_y_real"]:data["max_y_real"],:]
        
        # convert to hsv and find contours
        thresh, contours = convertANDthreshold(roi, threshold_value = threshold_value[i])
        
        # try except to handle error if no contour is found
        try:
            # if contours are found, then the flame is the largest contour detected
            flame_area[frame] = cv2.contourArea(contours[0]) * pixel_to_meters**2
            flame_perimeter[frame] = cv2.arcLength(contours[0], True) * pixel_to_meters
            flame_characteristic_length[frame] = flame_area[frame] / flame_perimeter[frame]
            flame = contours[0]
            flame_contours.append(flame)
            
            # retrieve ellipse major axis and angle
            ellipse = cv2.fitEllipse(flame)
            ellipse_majoraxis = ellipse[1][0]
            flame_ellipse_length[frame] = ellipse_majoraxis * pixel_to_meters
            flame_ellipse_angle[frame] = ellipse[2]
            
            # calculate flame height, flame projection and flame depth
            height_top, height_bottom, projection, depth_below, depth_topdoor, depth_above = heightANDdepth(
                    flame, pixel_to_meters, data, roi)
            
            
            # for Alpha2 (angle of the camera) and Gamma (frame) I removed the door from the analysis, so I need to
            # include it into the depth calculation
            if experiment == "Alpha2" or experiment == "Gamma":
                depth_below += data["door_depth"]
                depth_topdoor += data["door_depth"]
                depth_above += data["door_depth"]
                projection -= data["door_depth"]
                
            # convert all to meters (adding the height that hasn't been analysed img -> roi) and removing the height
            # to the bottom of the door
            if height_top == 0:
                flame_height_top[frame] = 0
                flame_height_bottom[frame] = 0
            else:
                flame_height_top[frame] = (height_top + data["min_y_real"] - data["door_origin"])* pixel_to_meters
                flame_height_bottom[frame] = (height_bottom + data["min_y_real"] - data["door_origin"]) * pixel_to_meters
                flame_projection[frame] = (projection)*pixel_to_meters

            flame_depth_below[frame] = depth_below * pixel_to_meters
            flame_depth_topdoor[frame] = depth_topdoor * pixel_to_meters
            flame_depth_above[frame] =  depth_above * pixel_to_meters
            
        except Exception as e:
            # if no contours are found or an error is raised
            print(frame, e)
            pass
        
        # save every 50th contour as well as flame height and depth (mostly for evaluating the code's performance)
        if frame % 50 == 0: 
            createANDsave_plot(flame,roi,experiment,frame, image,
                               (flame_height_top[frame], flame_height_bottom[frame]),
                               flame_projection[frame],
                               (flame_depth_below[frame], flame_depth_topdoor[frame], flame_depth_above[frame]))
        
        
    # save the contours separately for each test
    with open(f'{experiment}_flame_contours.pickle', 'wb') as handle:
        pickle.dump(flame_contours, handle)
        
    # create data frames with the data calculated
    df = pd.DataFrame(columns = ["testing_time","flame_height_top", "flame_height_bottom", "flame_projection",
                                 "flame_depth_below","flame_depth_topdoor","flame_depth_above", 
                                 "flame_area", "flame_perimeter",
                                 "flame_characteristic_length", "flame_ellipse_length", "flame_ellipse_angle"])
    
    # populate the data frame
    df["testing_time"] = np.linspace(0, data["total_video_duration"], len(flame_height_top))

    for j,column in enumerate(df.columns[1:]):
        df[column] = [flame_height_top, flame_height_bottom, flame_projection,
          flame_depth_below, flame_depth_topdoor, flame_depth_above,
          flame_area, flame_perimeter, 
          flame_characteristic_length, flame_ellipse_length, flame_ellipse_angle][j]

    # add the data frame to the central dictionary
    Flame_Dimensions[experiment] = df
        
        
file_address_save = "Flame_Dimensions_unsmoothed.pkl"
with open(file_address_save, 'wb') as handle:
    pickle.dump(Flame_Dimensions, handle)
    
