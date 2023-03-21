import numpy as np

# START SCRIPT
def clean_data(df):
    # function that cleans the data
    # it replaces Inc(.) with Inc.
    # it removes duplicate whitespaces from the data
    # it replaces empty cells with NaN
    # it removes leading and trailing spaces from column names

    df = df.copy(deep=True)    
    df.replace("(?i)Inc\.?","Inc.",regex=True,inplace=True)
    df.replace('\s+',' ',regex=True,inplace=True)
    df.replace(r'^\s*$',np.nan,regex=True,inplace=True)
    df.columns = df.columns.str.strip()

    # if there first three columns are empty for a row, drop the row
    df.dropna(subset=df.columns[:5], how='all', inplace=True)

    return df 
# END SCRIPT