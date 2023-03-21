# this is another test script

# import detect environment
from detect_environment import detect_environment
from get_data import get_data
from write_data import write_data
from get_actuals_date import get_actuals_date
from constants import *

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

    # get the actuals file date
    ACTUALS_FILE_DATE = get_actuals_date(df_actuals)
    
    
    write_data(df_name_map, RUNNING_IN_DOMO)
# END SCRIPT

if __name__ == "__main__":
    main()