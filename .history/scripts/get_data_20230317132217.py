from get_data_from_either import get_data_from_either

# START SCRIPT
def get_data(DICT, RUNNING_LOCALLY):
    # This function reads the data using the information from a dictionary and
    # returns a data frame
    DOMO_NAME = DICT['DOMO_FILE']
    FILE_PATH = DICT['FILE_PATH']

    # If the header is not specified, then use the default value of 0
    try:
        HEADER = DICT['HEADER']
    except KeyError:
        HEADER = 0

    return get_data_from_either(DOMO_NAME, FILE_PATH, HEADER)
# END SCRIPT