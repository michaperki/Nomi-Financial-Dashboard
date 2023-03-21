# this is another test script

# import detect environment
from detect_environment import detect_environment
from get_data import get_data
from write_data import write_data

# import logging
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


# START SCRIPT
PATH = "data/2023/monthly/"
FTE_DICT = {
    'DOMO_FILE': "FTE Projections",
    'FILE_PATH': PATH + "FTE Projections.csv",
}
ORM_DICT = {
    'DOMO_FILE': "Open Roles Projections",
    'FILE_PATH': PATH + "Open Roles Projections.csv",
}
FTC_DICT = {
    'DOMO_FILE': "FTC Projections",
    'FILE_PATH': PATH + "FTC Projections.csv",
}
PRO_SERV_DICT = {
    'DOMO_FILE': "Pro Serv Projections",
    'FILE_PATH': PATH + "Pro Serv Projections.csv",
}
SOFTWARE_DICT = {
    'DOMO_FILE': "Software Projections",
    'FILE_PATH': PATH + "Software Projections.csv",
}
ACTUALS_DICT = {
    'DOMO_FILE': "Actuals",
    'FILE_PATH': PATH + "Actuals.csv",
}

def main():
    RUNNING_IN_DOMO = detect_environment()
    logging.info(f"Running in Domo: {RUNNING_IN_DOMO}")
    df = get_data(ACTUALS_DICT, RUNNING_IN_DOMO)
    write_data(df, RUNNING_IN_DOMO)


# END SCRIPT

if __name__ == "__main__":
    main()