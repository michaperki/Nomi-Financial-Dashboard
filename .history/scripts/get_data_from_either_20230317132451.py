from get_data_from_local import get_data_from_local
from get_data_from_domo import get_data_from_domo
from complete_data_import import complete_data_import

# START SCRIPT
def get_data_from_either(dataset_id, file_name, header=0, RUNNING_IN_DOMO=False):
    # This function gets the data from either Domo or the local file
    # and returns a data frame
    if RUNNING_IN_DOMO:
        df = get_data_from_domo(dataset_id)
    else:
        df = get_data_from_local(file_name, header)
        
    complete_data_import(df)
    return df
# END SCRIPT