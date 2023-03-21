# this is another test script

# import detect environment
from constants import *
from detect_environment import detect_environment
from get_data import get_data
from write_data import write_data
from get_actuals_date import get_actuals_date
from setup_data_validation import setup_for_data_validation


# import logging
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


# START SCRIPT
def main():
    RUNNING_IN_DOMO = detect_environment()
    logging.warning(f"Running in Domo: {RUNNING_IN_DOMO}")

    df_fte = get_data(FTE_DICT, RUNNING_IN_DOMO)
    df_open_roles = get_data(ORM_DICT, RUNNING_IN_DOMO)
    df_ftc = get_data(FTC_DICT, RUNNING_IN_DOMO)
    df_pro_serv = get_data(PRO_SERV_DICT, RUNNING_IN_DOMO)
    df_software = get_data(SOFTWARE_DICT, RUNNING_IN_DOMO)
    df_actuals = get_data(ACTUALS_DICT, RUNNING_IN_DOMO)
    df_name_map = get_data(NAME_MAP_DICT, RUNNING_IN_DOMO)
    df_fte_allocation = get_data(FTE_ALLOCATION_DICT, RUNNING_IN_DOMO)
    df_ftc_allocation = get_data(FTC_ALLOCATION_DICT, RUNNING_IN_DOMO)
    df_pro_serv_allocation = get_data(PRO_SERV_ALLOCATION_DICT, RUNNING_IN_DOMO)
    df_software_allocation = get_data(SOFTWARE_ALLOCATION_DICT, RUNNING_IN_DOMO)

    # create a dictionary of the monthly dataframes
    df_monthly_dict = {
        'FTE': df_fte,
        'ORM': df_open_roles,
        'FTC': df_ftc,
        'PRO_SERV': df_pro_serv,
        'SOFTWARE': df_software,
        'ACTUALS': df_actuals,
    }

    # if it is from the first run of the year, then the actual file date is 0
    if not FIRST_RUN_OF_YEAR:
        ACTUAL_FILE_DATE = get_actuals_date(df_actuals)
    else:
        ACTUAL_FILE_DATE = 0
        logging.warning("First Run of the Year (Actuals File Date = 0)")

    # if data validation is turned on, then run the setup
    if DATA_VALIDATION_CONTROLLER:
        setup_for_data_validation(ACTUAL_FILE_DATE, df_monthly_dict)
    
    write_data(df_name_map, RUNNING_IN_DOMO)
# END SCRIPT

if __name__ == "__main__":
    main()