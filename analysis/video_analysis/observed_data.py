"""
This script contains the data observed from the videos. 
Structured as a dictionary

For the min and maximmum dimensions (used for defining roi),
x and y are defined based on real video NOT rotated frame
"""

properties_Alpha2 = {"door_height_px": 840,
                     "top_of_door": (990, 950), # (y_real, x_real) coordinates
                     "door_origin": 188,
                     "min_x_real": 200,
                     "max_x_real": 860,
                     "min_y_real": 250,
                     "max_y_real": 1920, # 1750
                     "start_externalflaming": 300,
                     "door_depth": 100,
                     "total_video_duration": 3900}
properties_Beta1 = {"door_height_px": 830,
                    "door_origin": 110,
                    "top_of_door": (940, 900), # (y_real, x_real) coordinates
                    "min_x_real": 400,
                    "max_x_real": 900,
                    "min_y_real": 300,
                    "max_y_real": 1920,
                    "start_externalflaming": 509,
                    "total_video_duration": 2559}
properties_Beta2 = {"door_height_px": 800,
                    "door_origin": 210,
                    "top_of_door": (915, 700), # (y_real, x_real) coordinates
                    "min_x_real": 200,
                    "max_x_real": 740,
                    "min_y_real": 350,
                    "max_y_real": 1920, # 1750
                    "start_externalflaming": 240,
                    "total_video_duration": 3750}
properties_Gamma = {"door_height_px": 805,
                    "door_origin": 360,
                    "top_of_door": (1130, 1020), # (y_real, x_real) coordinates
                    "min_x_real": 500,
                    "max_x_real": 970,
                    "min_y_real": 450,
                    "max_y_real": 1920,
                    "start_externalflaming": 319,
                    "door_depth": 60,
                    "total_video_duration": 4677}

properties = {"Alpha2": properties_Alpha2,
              "Beta1": properties_Beta1,
              "Beta2": properties_Beta2, 
              "Gamma": properties_Gamma}