from imports import *

from constants import *

# START SCRIPT
def remove_string_from_column(df, column, string):
    # function that removes a string from a column
    # after removing the string, convert any empty cells to NaN
    logging.debug(list(df[column].unique()))
    df[column] = df[column].str.replace(string, '', regex=True)
    df[column].replace(r'^\s*$',np.nan,regex=True,inplace=True)
    logging.debug(list(df[column].unique()))

    return df
# END SCRIPT