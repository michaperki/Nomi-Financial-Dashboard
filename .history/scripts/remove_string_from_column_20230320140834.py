from constants import *
import logging
from clean_data import clean_data
import pandas as pd

# START SCRIPT
def remove_string_from_column(df, column, string):
    # function that removes a string from a column
    # after removing the string, convert any empty cells to NaN

    # create a string of unique values in the column
    unique_values = ', '.join(list(df[column].unique()))
    # log the unique values in the column
    logging.debug("...unique values in " + column +  " are " + unique_values)

    
    df[column] = df[column].str.replace(string, '', regex=True)
    df[column].replace(r'^\s*$',np.nan,regex=True,inplace=True)

    # create a string of unique values in the column
    unique_values = ', '.join(list(df[column].unique()))
    # log the unique values in the column
    logging.debug("...after removing the pattern, unique values in " + column +  " are " + unique_values)


    return df
# END SCRIPT