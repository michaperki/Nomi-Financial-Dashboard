from domomagic import *
import os
import pandas as pd
import warnings
import calendar
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
### General Constants ###
CURR_YEAR = 2023
CURR_YEAR_STR = str(CURR_YEAR)
### Controller Constants ###
# These are the switches that control which scripts are run
HEADCOUNT_CONTROLLER = True
QUARTERLY_CONTROLLER = True
DELTA_CONTROLLER = True
ANALYSIS_CONTROLLER = False
# This is used for the first run of the year (i.e. no Actuals file yet) If there
# is no Actuals file for the current year, then set this to True This will set
# the ACTUAL_FILE_DATE to zero and the script will run
FIRST_RUN_OF_YEAR = False
DATA_VALIDATION_CONTROLLER = True
QM_DIFF_CONTROLLER = True
### File Paths ###
# monthly files
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
# Name Map File
PATH = "data/2023/"
NAME_MAP_DICT = {
    'DOMO_FILE': "Vendor Name Map",
    'FILE_PATH': PATH + "Vendor Name Map.csv"
}
# Allocation Files
PATH = "data/2023/allocations/"
FTE_ALLOCATION_DICT = {
    'DOMO_FILE': "FTE & Open Roles Allocation Table",
    'FILE_PATH': PATH + "FTE & Open Roles Allocation Table.csv",
}
FTC_ALLOCATION_DICT = {
    'DOMO_FILE': "FTC Allocation Table",
    'FILE_PATH': PATH + "FTC Allocation Table.csv",
}
PRO_SERV_ALLOCATION_DICT = {
    'DOMO_FILE': "Pro Serv Allocation Table",
    'FILE_PATH': PATH + "Pro Serv Allocation Table.csv",
}
SOFTWARE_ALLOCATION_DICT = {
    'DOMO_FILE': "Software Allocation Table",
    'FILE_PATH': PATH + "Software Allocation Table.csv",
}
### Column Name Arrays ###
SPEND_COLS_W_BONUS = [
  'Jan PnL','Feb PnL','Mar PnL',
  'Apr PnL','May PnL','Jun PnL',
  'Jul PnL','Aug PnL','Sep PnL',
  'Oct PnL','Nov PnL','Dec PnL',
  'Jan - Bonus Accrual','Feb - Bonus Accrual','Mar - Bonus Accrual',
  'Apr - Bonus Accrual','May - Bonus Accrual','Jun - Bonus Accrual',
  'Jul - Bonus Accrual','Aug - Bonus Accrual','Sep - Bonus Accrual',
  'Oct - Bonus Accrual','Nov - Bonus Accrual','Dec - Bonus Accrual'
]
def detect_environment():
    try:
        return os.environ['HOME'] == r"/home/domo"
    except KeyError:
        return False
def get_data_from_local(file_name, header=0):
    # This function gets the data from the local file from a csv
    # and returns a data frame
    warnings.simplefilter(action='ignore', category=UserWarning)
    df = pd.read_csv(file_name, header=header)
    return df
def get_data_from_domo(dataset_id):
    # This function gets the data from Domo
    # and returns a data frame
    df = read_dataframe(dataset_id)
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
        # split the columns into groups of 10
        for i in range(0, len(df.columns), 10):
            # print the columns in each group as a string, separated by a comma
            logging.debug("..." + ", ".join(df.columns[i:i+10]))
    else:
        logging.debug(",".join(df.columns))
def get_data(DICT, RUNNING_IN_DOMO):
    # This function reads the data using the information from a dictionary and
    # returns a data frame
    DOMO_NAME = DICT['DOMO_FILE']
    FILE_PATH = DICT['FILE_PATH']
    # If the header is not specified, then use the default value of 0
    try:
        HEADER = DICT['HEADER']
    except KeyError:
        HEADER = 0
    return get_data_from_either(DOMO_NAME, FILE_PATH, HEADER, RUNNING_IN_DOMO)
def complete_data_import(df):
    # This function completes the data import
    # It prints some information about the data frame
    # and stores some information about the data frame
    # to be used for validation later
    # if the data frame has a _FILE_NAME_ column, print the first value
    if '_FILE_NAME_' in df.columns:
        FILENAME = df['_FILE_NAME_'].iloc[0]
        logging.info("the file name is " + FILENAME)
    else:
        logging.info("the file name is not available (likely the Name Map)")
    # print the dimensions of the data frame
    logging.info(f"the data frame has {df.shape[0]} rows and {df.shape[1]} columns")
    print_columns(df)
def get_date_from_string(date_string):
    # This function converts a string containing
    # a month name into a date. Should also work for three letter month names
    month_str_to_int_dict = {month: index for index, month in enumerate(calendar.month_name) if month}
    short_month_str_to_int_dict = {month: index for index, month in enumerate(calendar.month_abbr) if month}
    # append the short month names to the dictionary
    month_str_to_int_dict.update(short_month_str_to_int_dict)
    for key, value in month_str_to_int_dict.items():
        # convert key to lowercase
        if key.lower() in date_string.lower():
            date_val = value
            break
    return date_val
def get_actuals_date(df_actuals):
    # function that returns the actuals file date
    
    ACTUAL_FILE_NAME = df_actuals['_FILE_NAME_'].iat[0].lower()
    ACTUAL_FILE_DATE = get_date_from_string(ACTUAL_FILE_NAME)
    logging.warning(f"Actuals File Date: {ACTUAL_FILE_DATE}")
    return ACTUAL_FILE_DATE
def setup_val_fte(df):
    # This function sets up the data validation for the FTE data
    # It returns a dictionary with the information needed for the validation
    # print the sum of all SPEND_COLS_W_BONUS formatted as a currency
    FTE_SPEND = df[SPEND_COLS_W_BONUS].sum().sum()
    print("the total FTE spend is " + "${:,.2f}".format(FTE_SPEND))
    print()
    # print the sum of all SPEND_COLS_W_BONUS by YEAR formatted as a currency
    return {
        'SPEND': FTE_SPEND,
        'SPEND_COLS': SPEND_COLS_W_BONUS
    }
def setup_for_data_validation(ACTUAL_FILE_DATE, FILE_DICT):
    # This function sets up the data validation
    # It runs the data validation setup functions
    # and returns a dictionary with the information needed for the validation
    # get the FTE data
    FTE = FILE_DICT['FTE']
    # set up the data validation for the FTE data
    val_fte = setup_val_fte(FTE)
    # # set up the data validation for the ORM data
    # val_orm = setup_val_orm()
    # # set up the data validation for the FTC data
    # val_ftc = setup_val_ftc()
    # # set up the data validation for the PRO_SERV data
    # val_pro_serv = setup_val_pro_serv()
    # # set up the data validation for the SOFTWARE data
    # val_software = setup_val_software()
    # # set up the data validation for the ACTUALS data
    # val_actuals = setup_val_actuals(ACTUAL_FILE_DATE)
    return {
        'FTE': val_fte,
        # 'ORM': val_orm,
        # 'FTC': val_ftc,
        # 'PRO_SERV': val_pro_serv,
        # 'SOFTWARE': val_software,
        # 'ACTUALS': val_actuals
    }
def write_data(df, RUNNING_IN_DOMO):
    if RUNNING_IN_DOMO:
        write_dataframe(df)
    else:
        df.to_csv("data/output/Output.csv")
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
    }
    # if it is from the first run of the year, then the actual file date is 0
    if not FIRST_RUN_OF_YEAR:
        ACTUAL_FILE_DATE = get_actuals_date(df_actuals)
        # add the actuals dataframe to the monthly dictionary
        df_monthly_dict['ACTUALS'] = df_actuals
    else:
        ACTUAL_FILE_DATE = 0
        logging.warning("First Run of the Year (Actuals File Date = 0)")
    # if data validation is turned on, then run the setup
    if DATA_VALIDATION_CONTROLLER:
        setup_for_data_validation(ACTUAL_FILE_DATE, df_monthly_dict)
    
    write_data(df_name_map, RUNNING_IN_DOMO)
main()