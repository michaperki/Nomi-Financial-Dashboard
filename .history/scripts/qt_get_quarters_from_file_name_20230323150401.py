from constants import *
import logging


# START SCRIPT
def get_quarters_from_file_name(df):
    # Find the letter "Q" (case insensitive) followed by a number in the _FILE_NAME_ column and
    # make a new column called Q-budget (standard format is YYYYQ# ex: 2023Q1)
    df["Q-budget"] = df["_FILE_NAME_"].str.extract(r"(?i)Q(\d)", expand=False)
    df["Y-budget"] = df["_FILE_NAME_"].str.extract(r"(?i)Q\d(\d{4})", expand=False)

    # If the Q-budget column has NaN values
    if df["Q-budget"].isnull().values.any():
        print("some file names did not include a quarter value, assigning 1")
        # replace the NaN values with 1
        df["Q-budget"] = df["Q-budget"].fillna(1)

    # If the Y-budget column has NaN values
    if df["Y-budget"].isnull().values.any():
        logging.debug("some file names did not include a year value, assigning 2023")
        # replace the NaN values with 2023
        df["Y-budget"] = df["Y-budget"].fillna(2023)

    # convert the Q-budget column to an int
    df["Q-budget"] = df["Q-budget"].astype(int)

    # convert the Y-budget column to an int
    df["Y-budget"] = df["Y-budget"].astype(int)

    return df
# END SCRIPT