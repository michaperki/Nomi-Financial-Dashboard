import os

import pandas as pd
import warnings



import logging


def detect_environment():
    try:
        return os.environ['HOME'] == r"/home/domo"
    except KeyError:
        return False

def get_data_from_domo(dataset_id):
    # This function gets the data from Domo
    # and returns a data frame
    df = read_dataframe(dataset_id)
    return df

def get_data_from_local(file_name, header=0):
    # This function gets the data from the local file from a csv
    # and returns a data frame
    warnings.simplefilter(action='ignore', category=UserWarning)
    df = pd.read_csv(file_name, header=header)
    return df

def get_data_from_either(dataset_id, file_name, header=0, RUNNING_IN_DOMO=False):
    # This function gets the data from either Domo or the local file
    # and returns a data frame
    if RUNNING_IN_DOMO:
        df = get_data_from_domo(dataset_id)
    else:
        df = get_data_from_local(file_name, header)
        
    complete_data_import(df)
    return df

def print_columns(df):
    # This function prints the columns of the data frame
    # This is useful for debugging

    # are there more than 10 columns?
    if len(df.columns) > 10:
        print("the column names are...")
        # split the columns into groups of 10
        for i in range(0, len(df.columns), 10):
            # print the columns in each group as a string, separated by a comma
            print("..." + ", ".join(df.columns[i:i+10]))
    else:
        print(",".join(df.columns))
    print()

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

    return get_data_from_either(DOMO_NAME, FILE_PATH, HEADER, RUNNING_LOCALLY)

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def main():
    RUNNING_IN_DOMO = detect_environment()
    logging.info(f"Running in Domo: {RUNNING_IN_DOMO}")
    PATH = "data/"
    FTE_DICT = {
    'DOMO_FILE': "FTE Projections",
    'FILE_PATH': PATH + "FTE Projections.csv"
    }
    get_data(FTE_DICT, RUNNING_IN_DOMO)

