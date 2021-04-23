"""
This code uploads the already pickled TSC data, operates on it, parses the
data that is needed and then saves it as a dictionary in the processed data
folder

"""

import pickle

TSC = {}

# iterate over the four tests to be analysed
for test_name in ["Alpha2", "Beta2", "Gamma"]:
    
    # upload the pickled files from the unprocessed data folder
    file_address = (r"C:/Users/s1475174/Documents/Python_Projects/T"
                    r"hermalRadiation_BREexperiments/unprocessed_data/t"
                    f"sc_data/{test_name}_TSC.pkl")
    
    """
    data already processed by me previously (see the jupyter notebook in
                                             the unprocesseded data folder)
    """
    with open(file_address, "rb") as handle:
        TSC[test_name] = pickle.load(handle)
        
    # only retain the columns of interest
    TSC[test_name].drop(columns = TSC[test_name].columns[1:-8],
                        inplace=True)
    TSC[test_name].rename(columns = {"Elapsed_time": "testing_time"},
                          inplace=True)
    TSC[test_name].loc[:, "testing_time"] = TSC[test_name].loc[
        :, "testing_time"] * 60

# save all the external HRR data as a pickle in processed data
file_address_save = (r"C:/Users/s1475174/Documents/Python_Projects/T"
                     r"hermalRadiation_BREexperiments/processed_data/TSC.pkl")
with open(file_address_save, 'wb') as handle:
    pickle.dump(TSC, handle)
