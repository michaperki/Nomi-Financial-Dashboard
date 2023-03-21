# this is another test script

# import detect environment
from detect_environment import detect_environment
from get_data import get_data
from write_data import write_data

# START SCRIPT
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def main():
    RUNNING_IN_DOMO = detect_environment()
    logging.info(f"Running in Domo: {RUNNING_IN_DOMO}")
    PATH = "data/"
    FTE_DICT = {
    'DOMO_FILE': "FTE Projections",
    'FILE_PATH': PATH + "FTE Projections.csv"
    }
    df = get_data(FTE_DICT, RUNNING_IN_DOMO)
    write_data(df, RUNNING_IN_DOMO)


# END SCRIPT

if __name__ == "__main__":
    main()