from get_data_from_local import get_data_from_local
from get_data_from_domo import get_data_from_domo

# START SCRIPT
def get_data_from_either(dataset_id, file_name, header=0):
    # This function gets the data from either Domo or the local file
    # and returns a data frame
    if RUNNING_LOCALLY:
        df = get_data_from_local(file_name, header)
    else:
        df = get_data_from_domo(dataset_id)
    
    if PRINT_LEVEL > 1: 
        complete_data_import(df)
    return df
# END SCRIPT