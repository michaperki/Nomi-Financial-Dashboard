from constants import *
import logging
from clean_data import clean_data
import pandas as pd

# START SCRIPT
def remove_string_from_column(df, column, string):
    # function that removes a string from a column
    # after removing the string, convert any empty cells to NaN

    logging.debug("...removing " + string + " from " + column)
    logging.debug("...unique values in " + column + " are " + list(df[column].unique()))

    df[column] = df[column].str.replace(string, '', regex=True)
    df[column].replace(r'^\s*$',np.nan,regex=True,inplace=True)

    logging.debug("...after removing, unique values in " + column +  " are " + list(df[column].unique()))

    return df
# END SCRIPT