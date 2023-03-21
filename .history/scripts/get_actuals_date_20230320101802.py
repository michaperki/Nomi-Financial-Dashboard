from get_date_from_string import get_date_from_string

def get_actuals_date(df_actuals):
    # function that returns the actuals file date
    
    ACTUAL_FILE_NAME = df_actuals['_FILE_NAME_'].iat[0].lower()
    ACTUAL_FILE_DATE = get_date_from_string(ACTUAL_FILE_NAME)
    return ACTUAL_FILE_DATE