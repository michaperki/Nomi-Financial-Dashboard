# this is another test script

# import detect environment
from constants import *
from detect_environment import detect_environment
from get_data import get_data
from write_data import write_data
from get_actuals_date import get_actuals_date
from setup_data_validation import setup_for_data_validation
from clean_allocation_sheet import clean_allocation_sheet
from clean_actuals import clean_actuals
from clean_fte import clean_fte
from clean_orm import clean_orm
from clean_ftc import clean_ftc
from clean_pro_serv import clean_pro_serv
from clean_software import clean_software
from validation_checkpoint import validation_checkpoint
from join_allocation_to_df import join_allocation_to_df
from format_final_df import format_final_df
from validation_complete import validation_complete
from hc_calculate_headcount import calculate_headcount
from clean_data import clean_data
from dt_calculate_deltas import calculate_deltas
from qt_format_quarterly_data import format_quarterly_data
from qm_calculate_qm_diff import calculate_qm_diff

import pandas as pd

# import logging
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


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
        val_dict = setup_for_data_validation(ACTUAL_FILE_DATE, df_monthly_dict)

    ### Data Cleaning ###
    # Allocations
    df_fte_allocation['SOURCE'] = 'FTE_AND_OPEN_ROLES'
    df_ftc_allocation['SOURCE'] = 'FTC'
    df_pro_serv_allocation['SOURCE'] = 'PRO_SERV'
    df_software_allocation['SOURCE'] = 'SOFTWARE'

    df_fte_allocation = clean_allocation_sheet(df_fte_allocation, df_name_map)
    df_ftc_allocation = clean_allocation_sheet(df_ftc_allocation, df_name_map)
    df_pro_serv_allocation = clean_allocation_sheet(df_pro_serv_allocation, df_name_map)
    df_software_allocation = clean_allocation_sheet(df_software_allocation, df_name_map)

    df_actuals = clean_actuals(df_actuals, ACTUAL_FILE_DATE, df_name_map)
    
    df_fte = clean_fte(df_fte)
    df_open_roles = clean_orm(df_open_roles)
    df_ftc = clean_ftc(df_ftc)
    df_pro_serv = clean_pro_serv(df_pro_serv)
    df_software = clean_software(df_software)

    # if data validation is turned on, then run the checkpoint
    if DATA_VALIDATION_CONTROLLER:
        validation_checkpoint(val_dict, df_fte, df_open_roles, df_ftc, df_pro_serv, df_software, df_actuals)

    df_fte = join_allocation_to_df(df_fte, df_fte_allocation)
    df_open_roles = join_allocation_to_df(df_open_roles, df_fte_allocation)
    df_ftc = join_allocation_to_df(df_ftc, df_ftc_allocation)
    df_pro_serv = join_allocation_to_df(df_pro_serv, df_pro_serv_allocation)
    df_software = join_allocation_to_df(df_software, df_software_allocation)

    df_allocation = pd.concat((df_fte_allocation, df_ftc_allocation, df_pro_serv_allocation, df_software_allocation), ignore_index=True)
    df_actuals = join_allocation_to_df(df_actuals, df_allocation)
    df = pd.concat((df_actuals, df_fte, df_open_roles, df_software, df_pro_serv, df_ftc), ignore_index=True)
    df_main = format_final_df(df, ACTUAL_FILE_DATE)
    df_main['SEGMENT'] = "MAIN"

    df_validation = validation_complete(val_dict, df_main)
    OUTPUT_ARRAY = [df_main, df_validation]

    if HEADCOUNT_CONTROLLER:
        df_fte_hc = get_data(FTE_DICT, RUNNING_IN_DOMO)
        df_orm_hc = get_data(ORM_DICT, RUNNING_IN_DOMO)
        df_fte_allocation_hc = get_data(FTE_ALLOCATION_DICT, RUNNING_IN_DOMO)
        all_data = [df_fte_hc, df_fte_allocation_hc,df_orm_hc]

        for df in all_data:
            df = clean_data(df)

        df_headcount = calculate_headcount(df_fte_hc, df_orm_hc, df_fte_allocation_hc, df_name_map)

        # drop the columns EEID, Product, and Title from df_headcount
        df_headcount.drop(columns=['EEID', 'Product', 'Title'], inplace=True)
        df_headcount['SEGMENT'] = 'FTE_ORM'
        OUTPUT_ARRAY.append(df_headcount)

    if DELTA_CONTROLLER:
        df_actuals = get_data(ACTUALS_DICT, RUNNING_IN_DOMO)    
        df_software = get_data(SOFTWARE_DICT, RUNNING_IN_DOMO)
        df_ftc = get_data(FTC_DICT, RUNNING_IN_DOMO)
        df_pro_serv = get_data(PRO_SERV_DICT, RUNNING_IN_DOMO)
        df_fte = get_data(FTE_DICT, RUNNING_IN_DOMO)
        df_delta = calculate_deltas(df_fte, df_ftc, df_pro_serv, df_software, df_actuals, ACTUAL_FILE_DATE, df_name_map)
        df_delta['SEGMENT'] = 'DELTA'
        OUTPUT_ARRAY.append(df_delta)

    if QUARTERLY_CONTROLLER:
        df_fte = get_data(FTE_QUARTERLY_DICT, RUNNING_IN_DOMO)
        df_orm = get_data(ORM_QUARTERLY_DICT, RUNNING_IN_DOMO)
        df_ftc = get_data(FTC_QUARTERLY_DICT, RUNNING_IN_DOMO)
        df_pro_serv = get_data(PRO_SERV_QUARTERLY_DICT, RUNNING_IN_DOMO)
        df_software = get_data(SOFTWARE_QUARTERLY_DICT, RUNNING_IN_DOMO)
        df_actuals = get_data(ACTUALS_QUARTERLY_DICT, RUNNING_IN_DOMO)
        df_name_map = get_data(NAME_MAP_DICT, RUNNING_IN_DOMO)
        df_fte_allocation = get_data(FTE_ALLOCATION_DICT, RUNNING_IN_DOMO)
        df_ftc_allocation = get_data(FTC_ALLOCATION_DICT, RUNNING_IN_DOMO)
        df_pro_serv_allocation = get_data(PRO_SERV_ALLOCATION_DICT, RUNNING_IN_DOMO)
        df_software_allocation = get_data(SOFTWARE_ALLOCATION_DICT, RUNNING_IN_DOMO)
        df_quarterly = format_quarterly_data(df_fte, df_orm, df_ftc, df_pro_serv, df_software, df_actuals, df_fte_allocation, df_ftc_allocation, df_pro_serv_allocation, df_software_allocation, df_name_map)
        df_quarterly['SEGMENT'] = 'QUARTERLY'
        OUTPUT_ARRAY.append(df_quarterly)

    if QM_DIFF_CONTROLLER:
        df_qm_diff = calculate_qm_diff(df_main, df_quarterly)
        df_qm_diff['SEGMENT'] = 'QM_DIFF'
        OUTPUT_ARRAY.append(df_qm_diff)

    df = pd.concat(OUTPUT_ARRAY, ignore_index=True)

    if not DELTA_CONTROLLER:
        df['TOP_5'] = np.nan
        df['VALUE'] = np.nan

    write_data(df, RUNNING_IN_DOMO)
# END SCRIPT

if __name__ == "__main__":
    main()