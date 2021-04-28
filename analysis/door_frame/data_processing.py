"""
Functions used to calculate velocity and mass flow at the door from the
doorway pressure probe and temperature data
"""

from scipy.signal import savgol_filter
import numpy as np
from scipy import interpolate

def calculation_area(number_of_heights=9, delta_height=0.2, door_width=0.8):
    """
    Returns a list with the equivalent area fraction of the door for each
    probe
    The list provides a number of areas equal to the number of heights
    measured. Some heights (0.4 m and 1.6 m) have three pressure probes.
    
    Parameters:
    ----------
    number_of_heights: number of heights at which pressure probes were located
        int

    delta_height: fraction of the door corresponding to a single pressure probe
        float
        
    door_width: width of the door
        float
        
    Returns:
    -------
    areas = list with the corresponding door area for each pressure probe height
        list
    """
    areas = [delta_height * door_width] * number_of_heights
    
    return areas


def calculation_velocity(df, test_name, gamma=0.94, omega_factor=2.49,
                         gems_factor=10, window_length=31, polyorder=2):
    """
    Calculates gas flow velocity from the pressure probe readings
    
    Parameters:
    ----------
    df: pandas DataFrame with the raw test data
        pd.DataFrame

    gamma: calibration constant for the pressure probe
        float

    omega_factor: conversion factor for the omega pressure transducers
        float

    gems_factor: conversion factor for the gems pressure transducers
        int

    window_length: the length of the filter window for the Savitsky-Golay
                   filter
        int
        
    polyorder: the order of the polynomial used to fit the samples with the
               Savitsky-Golay filter
        int

    test_name: name of the test. Required to perform individualized cleaning
               of the data
        str
        
    Returns:
    -------
    df: pandas DataFrame with the formatted and calculated data
        pd.DataFrame
    """
    # create a mask to access values before start test
    mask_prestart = df.loc[:, "testing_time"] < 0
    
    # fix temperature TDD.40 for Beta2 by interpolating from the other TCs
    if test_name == "Beta2":
        
        # extrapolate to obtain temperature at 0.4 meters
        df.loc[:, "TDD.40"] = df.loc[:, ["TDD.60", "TDD.80", "TDD.100",
                                         "TDD.120", "TDD.140", "TDD.160",
                                         "TDD.180"]].apply(
                                             lambda row: extrapolate(
                                                 [60, 80, 100, 120, 140, 160,
                                                  180], row.values, 40),
                                             axis=1)
    
    # ambient temperature is mean value before start and assing to h = 20 cm.
    temperature_columns = []
    for column in df:
        if "TDD" in column:
            temperature_columns.append(column)
    temperature_ambient = df.loc[
        mask_prestart, temperature_columns].mean().mean()
    df["TDD.20"] = temperature_ambient

    # calculate mean value reported by the pressure probes before start test
    pressure_columns = [x for x in df.columns if "P" in x]
    pressure_prestart_mean = df.loc[mask_prestart, pressure_columns].mean()
    
    # calculate the zeroed values for the pressure channels
    for column in pressure_prestart_mean.index:
        df.loc[:, f"{column}_zeroed"] = df.loc[:, column] - pressure_prestart_mean[column]
    
    # determine which pressure transducers were used for each sensor
    omega = ["P1.20", "P2.40", "P3.40", "P4.40", "P5.60", "P6.80"]
    gems = ["P7.100", "P8.120", "P9.140", "P10.160", "P11.160", "P12.160",
            "P13.180"]

    # calculate the pressure difference from the zeroed values
    for column in df:
        if "zeroed" not in column:
            pass
        else:
            probe = column.split("_")[0]
            if probe in omega:
                df.loc[:, f"{probe}_DeltaP"] = df.loc[:, column] * omega_factor
            elif probe in gems:
                df.loc[:, f"{probe}_DeltaP"] = df.loc[:, column] * gems_factor

    # drop all nan values before continuing with smoothing
    df.dropna(axis = 0, inplace = True)

    # smooth the pressure readings using a savitsky-golay filter
    for column in df:
        if "DeltaP" in column:
            df.loc[:, f"{column}_smooth"] = savgol_filter(df.loc[:, column],
                                                          window_length, polyorder)

    # average probes 0.4 from the ground
    if test_name in ["Alpha1","Alpha2", "Beta2", "Gamma"]:
        df.loc[:, "PP_40"] = df.loc[:, ["P2.40_DeltaP_smooth",
                                        "P3.40_DeltaP_smooth",
                                        "P4.40_DeltaP_smooth"]].mean(axis = 1)
    elif test_name in ["Beta1"]:
        df.loc[:, "PP_40"] = df.loc[:, ["P2.40_DeltaP_smooth",
                                        "P4.40_DeltaP_smooth"]].mean(axis = 1)

    # average probes 1.6 meters from the ground
    if test_name in ["Alpha1","Alpha2"]:
        df.loc[:, "PP_160"] = df.loc[
            :, ["P12.160_DeltaP_smooth"]].mean(axis = 1)
    elif test_name in ["Beta1"]:
        df.loc[:, "PP_160"] = df.loc[
            :, ["P10.160_DeltaP_smooth"]].mean(axis = 1)
    elif test_name in ["Beta2"]:
        df.loc[:, "PP_160"] = df.loc[
            :, ["P10.160_DeltaP_smooth",
                "P12.160_DeltaP_smooth"]].mean(axis = 1)
    elif test_name in ["Gamma"]:
        df.loc[:, "PP_160"] = df.loc[
            :, ["P10.160_DeltaP_smooth", "P11.160_DeltaP_smooth",
                "P12.160_DeltaP_smooth"]].mean(axis = 1)
        
    # assing new columns with useful data to their respective heights. 
    # I do this instead of renaming to preserve all data
    column_new_name = ["PP_20", "PP_60", "PP_80", "PP_100", "PP_120", "PP_140",
                       "PP_180"]
    for i, column_old_name in enumerate(
            ["P1.20_DeltaP_smooth", "P5.60_DeltaP_smooth",
             "P6.80_DeltaP_smooth", "P7.100_DeltaP_smooth",
             "P8.120_DeltaP_smooth", "P9.140_DeltaP_smooth",
             "P13.180_DeltaP_smooth"]):
            df.loc[:, column_new_name[i]] = df.loc[:, column_old_name]

    """
    Clean up the data for each test by interpolating and extrapolating to
    substitute damaged data
    """
    if test_name == "Alpha2":
        # between 5 min and 15 min, interpolate PP120 and PP140
        mask_interpolation = (df.loc[:, "testing_time"]/60 > 5) & (
            df.loc[:, "testing_time"]/60 < 15)
        df.loc[mask_interpolation, "PP_120"] = df.loc[
            mask_interpolation, ["PP_100", "PP_160"]].apply(
                lambda row: np.interp(120,[100,160], row.values), axis = 1)
        df.loc[mask_interpolation, "PP_140"] = df.loc[
            mask_interpolation, ["PP_100", "PP_160"]].apply(
                lambda row: np.interp(140,[100,160], row.values), axis = 1)

        # between 0 and 5 min, then between 12 and 20 and after 40 minutes
        # extrapolate for PP180
        mask_extrapolation = (((df.loc[:, "testing_time"]/60 > 0) &
                               (df.loc[:, "testing_time"]/60 < 6)) |
                              ((df.loc[:, "testing_time"]/60 > 12) &
                               (df.loc[:, "testing_time"]/60 < 21))|
                              (df.loc[:, "testing_time"]/60 > 40))
        df.loc[mask_extrapolation, "PP_180"] = df.loc[
            mask_extrapolation, ["PP_100", "PP_120", "PP_140","PP_160"]].apply(
                lambda row: extrapolate([100,120,140,160], row.values, 180),
                axis = 1)

    if test_name == "Beta1":

        # between 10 min and 20 min extrapolate PP_120 and PP_140
        mask_extrapolation = (df.loc[:, "testing_time"]/60 > 10) & (
            df.loc[:, "testing_time"]/60 < 20)
        df.loc[mask_extrapolation, "PP_20"] = df.loc[mask_extrapolation,
                                                     ["PP_60", "PP_80"]].apply(
                lambda row: extrapolate([60,80], row.values, 20), axis = 1)
        df.loc[mask_extrapolation, "PP_40"] = df.loc[mask_extrapolation,
                                                     ["PP_60", "PP_80"]].apply(
                lambda row: extrapolate([60,80], row.values, 40), axis = 1)

        # between 7 min and 11 min interpolate PP_100
        mask_interpolation = (df.loc[:, "testing_time"]/60 > 7) & (
            df.loc[:, "testing_time"]/60 < 11)
        df.loc[mask_interpolation, "PP_100"] = df.loc[
            mask_interpolation, ["PP_80", "PP_120"]].apply(
                lambda row: np.interp(100,[80,120], row.values), axis = 1)

        # between 6 min and 20 min extrapolate PP_160 and PP_180
        mask_extrapolation = (df.loc[:, "testing_time"]/60 > 6) & (
            df.loc[:, "testing_time"] / 60 < 60)
        df.loc[mask_extrapolation, "PP_160"] = df.loc[
            mask_extrapolation, ["PP_20", "PP_40","PP_60", "PP_80", "PP_100",
                                 "PP_120", "PP_140"]].apply(
                lambda row: extrapolate([20,40,60,80,100,120,140], row.values,
                                        160), axis = 1)
        df.loc[mask_extrapolation, "PP_180"] = df.loc[
            mask_extrapolation, ["PP_20", "PP_40","PP_60", "PP_80", "PP_100",
                                 "PP_120", "PP_140", "PP_160"]].apply(
                lambda row: extrapolate([20,40,60,80,100,120,140, 160],
                                        row.values, 180), axis = 1)

    if test_name == "Beta2":
        
        # between 0 min and 15 min extrapolate PP_180
        mask_extrapolation = (df.loc[:, "testing_time"]/60 > 0) & (
            df.loc[:, "testing_time"]/60 < 15)
        df.loc[mask_extrapolation, "PP_180"] = df.loc[
            mask_extrapolation, ["PP_20", "PP_40","PP_60", "PP_80", "PP_100",
                                 "PP_120", "PP_140", "PP_160"]].apply(
                lambda row: extrapolate([20,40,60,80,100,120,140, 160],
                                        row.values, 180), axis = 1)
            
        # between 8 min and 10 min interpolate PP_100
        mask_interpolation = (df.loc[:, "testing_time"]/60 > 8) & (
            df.loc[:, "testing_time"]/60 < 10)
        df.loc[mask_interpolation, "PP_100"] = df.loc[
            mask_interpolation, ["PP_80", "PP_120"]].apply(
                lambda row: np.interp(100,[80,120], row.values), axis = 1)

    if test_name == "Gamma":

        # between 7 min and 16 min interpolate PP_120 and PP_140
        mask_interpolation = (df.loc[:, "testing_time"]/60 > 7) & (
            df.loc[:, "testing_time"]/60 < 16)
        df.loc[mask_interpolation, "PP_120"] = df.loc[
            mask_interpolation, ["PP_100", "PP_160"]].apply(
                lambda row: np.interp(120,[100,160],row.values), axis = 1)
        df.loc[mask_interpolation, "PP_140"] = df.loc[
            mask_interpolation, ["PP_100", "PP_160"]].apply(
                lambda row: np.interp(140,[100,160],row.values), axis = 1)

    # If delta p is positive then temperature equals ambient temperature
    df.loc[:, "TC_20"] = df.loc[:, "TDD.20"]
    for column in df:
        if "PP" in column:
            mask_positives = df.loc[:, column] > 0
            height = column.split("_")[1]
            df.loc[:, f"TC_{height}"] = df.loc[:, f"TDD.{height}"]
            df.loc[mask_positives, f"TC_{height}"] = temperature_ambient

    # calculate density
    for column in df:
        if "TC" in column:
            height = column.split("_")[1]
            df.loc[:, f"Rho_{height}"] = 353 / (df.loc[:,column] + 273)

    # calculate velocities
    for height in range(20,200,20):
        df.loc[:,f"V_{height}"] = gamma * (2 * np.abs(df.loc[:, f"PP_{height}"]) / 
               df.loc[:, f"Rho_{height}"])**0.5

        """
        np.abs used for calculation but negative delta P should give a
        negative (outward) velocity
        """
        mask_negatives = df.loc[:, f"PP_{height}"] < 0
        df.loc[mask_negatives,f"V_{height}"] = df.loc[
            mask_negatives,f"V_{height}"] * -1

    # calculate neutral plane by interpolating the velocity values
    columns_velocity = []
    for column in df:
        if "V_" in column:
            columns_velocity.append(column)
    heights = np.linspace(0.2,1.8,9)

    df.loc[:, "Neutral_Plane"] = df.loc[:, columns_velocity].apply(
        lambda row: find_neutral_plane(row, heights), axis = 1)
    df.loc[:, "Neutral_Plane_Smooth"] = df.loc[
        :,"Neutral_Plane"].rolling(30).mean()
    
    return


def extrapolate(x, y, x_ext):
    """
    Function to implement extrapolation in the data frame
    
    Parameters:
    ----------
    row: pandas DataFrame containing all the time dependant data
        np.array
    
    x: value at which the extrapolating function should be evaluated
        float
    
    Returns:
    -------
    y_ext: f(x). Interpolate value
        float
    
    """

    extrapolating_function = interpolate.interp1d(x = x,
                                              y = y,
                                              kind = 'linear',
                                              fill_value = 'extrapolate')
    
    y_ext = extrapolating_function(x_ext)
    
    return y_ext


def find_neutral_plane(x,y):
    """
    Interpolates the velocity profile to find the neutral plane
    
    Parameters:
    ----------
    x: velocities
        np.array
        
    y: heights
        np.array
        
    Returns:
    -------
    neutral_plane: height of the neutral plane
        float
    """
    
    # create set of tuples containing the velocity and their respective height
    pos = (0,0)
    neg = (0,0)

    # determine the height of the last positive velocity and the first negative velocity
    for i,vel in enumerate(x.values):
        if vel < 0:
            if i != 0:
                neg = (vel, y[i])
                pos = (x.values[i-1], y[i-1])
                break

    # interpolate 
    f = interpolate.interp1d(x = [pos[0], neg[0]], y = [pos[1], neg[1]],
                             kind="linear", fill_value = 'extrapolate')

    # evaluate the interpolating function to find the velocity
    neutral_plane = f(0)

    return neutral_plane


def calculation_massflow(df, areas, Cd=0.68):
    """
    Calculates the mass flow from the velocities and areas already determined.
    
    Also determines the total inflow and outflow of gases to and from the compartment
    
    Parameters:
    ----------
    df: pandas DataFrame containing all the time dependant data
        pd.DataFrame
    
    areas: fraction of the door area to which each pressure probe corresponds
        list
        
    Cd: discharge coefficient (0.68 according to SFPE and 0.7 according to Prahl and Emmons, 1975)
    
    Returns:
    -------
    df: pandas DataFrame containing all the data.
    """
    
    for i, height in enumerate(list(range(20,200,20))):
        df.loc[:, f"M_{height}"] = Cd * df.loc[
            :, f"Rho_{height}"] * df.loc[:,f"V_{height}"] * areas[i]

    mass_columns = [x for x in df.columns if "M_" in x]

    # sum positives and negatives to obtain mass_in and mass_out (slow and dirty implementation)
    for index, row in df.loc[:, mass_columns].iterrows():
        positives = 0
        negatives = 0
        for item in row:
            if item > 0:
                positives += item
            else:
                negatives += np.abs(item)
        df.loc[index, "mass_in"] = positives
        df.loc[index, "mass_out"] = negatives
    df.loc[:, "mass_average"] = df.loc[:, ["mass_in", "mass_out"]].mean(axis = 1)

    """
    Calculate HRR assuming all O2 in gets oxydised
    (I later use the juanalyser as well to run a different HRR calc)
    """
    df.loc[:, "hrr_internal_allmassin"] = 0.233 * df.loc[:, "mass_in"] * 13100
            
    return


def calculation_HRR(df, df_mass, alpha = 1.105, 
                    XO2_0 = 0.2095, XCO2_0 = 0.0004 ,E_02 = 13100, ECO_CO2 = 17600,
                    M_a = 29, M_O2 = 32, M_CO2 = 44, M_CO = 28,
                    window_length = 31, polyorder = 2):
    """
    Calculates the HRR from Oxygen Calorimetry using the mass flow calculated
    above and the gas analysis results from the Juanalyser
    
    Parameters:
    ----------
    
    
    Returns:
    -------
    df: pandas DataFrame containing all the data.
    """
    """
    interpolate the data from df_massloss to calculate the HRR.
    This is because this was logged with a different
    datalogger and so it has a different time stamp
    """
    mass_interpolating_function = interpolate.interp1d(
        x=df_mass.loc[:, "testing_time"],
        y=df_mass.loc[:, "mass_average"],
        kind='linear',
        fill_value='extrapolate')

    df.loc[:, "mass_average"] = mass_interpolating_function(
        df.loc[:, "testing_time"])
    
    # first, smoothe O2, CO and CO2 values
    for column_name in ["CO2", "CO", "O2"]:
        df.loc[:, f"{column_name}_smooth"] = savgol_filter(
            df.loc[:,column_name], window_length, polyorder)
        
    # convert from % volume to mole (assumes ideal gas so % volume == % mol)
    for column_name in ["CO2_smooth", "CO_smooth", "O2_smooth"]:
        df.loc[:, f"{column_name}_mol"] = df.loc[:, column_name]/100
        
    # calculate oxygen depletion factor
    XO2 = df.loc[:, "O2_smooth_mol"]
    XCO = df.loc[:, "CO_smooth_mol"]
    XCO2 = df.loc[:, "CO2_smooth_mol"]
    
    df.loc[:, "oxygen_depletion_factor"] = (
        XO2_0 * (1 - XCO2 - XCO) - XO2 * (1 - XCO2_0)) / (
            XO2_0 * (1 - XO2 - XCO2 - XCO))

    # calculate the HRR
    O2_dep_fac = df.loc[:, "oxygen_depletion_factor"]
    me = df.loc[:, "mass_average"]
    
    df.loc[:, "hrr_internal"] = (E_02 * O2_dep_fac - (
        (ECO_CO2 - E_02)*((1 - O2_dep_fac)/2) * (XCO/XO2))) * (
            (me/(1 + O2_dep_fac*(alpha - 1)))*(M_O2/M_a)*XO2_0)

    return
