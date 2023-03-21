import os

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

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def main():
    RUNNING_LOCALLY = detect_environment()
    logging.info(f"Running locally: {RUNNING_LOCALLY}")

