# this is another test script

# import detect environment
from detect_environment import detect_environment
from get_data import get_data

# START SCRIPT
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def main():
    RUNNING_LOCALLY = detect_environment()
    logging.info(f"Running locally: {RUNNING_LOCALLY}")
    PATH = "data/"
    FTE_DICT = {
    'DOMO_FILE': "FTE Projections",
    'FILE_PATH': PATH + "FTE Projections.csv"
    }
    get_data(FTE_DICT, RUNNING_LOCALLY)

# END SCRIPT

if __name__ == "__main__":
    main()