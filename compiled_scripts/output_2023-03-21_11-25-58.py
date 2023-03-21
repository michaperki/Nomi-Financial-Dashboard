from domomagic import *
import numpy as np
import os
import pandas as pd
import warnings
import calendar
from dateutil.relativedelta import relativedelta
from datetime import timedelta
import datetime
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
# Output Arrays
OUTPUT_ARRAY = []
ERROR_ARRAY = []
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
### Declare other dictionaries ###
IS_GROUP_DICT = {
    "2 - COGS":"COGS",
    "3a - Sales & Mktg":"S&M",
    "3b - R&D":"R&D",
    "3c - G&A":"G&A"
}
EXPENSE_BUCKET_DICT = {
    "Tech - 6412 - FTC":"FTC",
    "Tech - 6414 - Software":"SOFTWARE",
    "Tech - 6413 - Pro Services & Advisory":"PRO_SERV",
    "Tech - 6000s - FTE":"FTE"
}
DICT_W_BONUS = {
'Jan PnL':'01|SALARY', 'Feb PnL':'02|SALARY', 'Mar PnL':'03|SALARY',
'Apr PnL':'04|SALARY', 'May PnL':'05|SALARY', 'Jun PnL':'06|SALARY',
'Jul PnL':'07|SALARY', 'Aug PnL':'08|SALARY', 'Sep PnL':'09|SALARY',
'Oct PnL':'10|SALARY', 'Nov PnL':'11|SALARY', 'Dec PnL':'12|SALARY',
'Jan - Bonus Accrual':'01|BONUS', 'Feb - Bonus Accrual':'02|BONUS', 'Mar - Bonus Accrual':'03|BONUS',
'Apr - Bonus Accrual':'04|BONUS', 'May - Bonus Accrual':'05|BONUS', 'Jun - Bonus Accrual':'06|BONUS',
'Jul - Bonus Accrual':'07|BONUS', 'Aug - Bonus Accrual':'08|BONUS', 'Sep - Bonus Accrual':'09|BONUS',
'Oct - Bonus Accrual':'10|BONUS', 'Nov - Bonus Accrual':'11|BONUS', 'Dec - Bonus Accrual':'12|BONUS'
}
MONTH_DICT = {
	"01": "Jan",	"02": "Feb",	"03": "Mar",
	"04": "Apr",	"05": "May",	"06": "Jun",
	"07": "Jul",	"08": "Aug",	"09": "Sep",
	"10": "Oct",	"11": "Nov",	"12": "Dec"
}
ALLOCATION_COL_DICT = {
    'Care':'Q1|'+ CURR_YEAR_STR +'|Care',           'Connect':'Q1|'+ CURR_YEAR_STR +'|Connect',             'Insights':'Q1|'+ CURR_YEAR_STR +'|Insights',               'Network':'Q1|'+ CURR_YEAR_STR +'|Network',
    'Care2':'Q2|'+ CURR_YEAR_STR +'|Care',          'Connect2':'Q2|'+ CURR_YEAR_STR +'|Connect',            'Insights2':'Q2|'+ CURR_YEAR_STR +'|Insights',              'Network2':'Q2|'+ CURR_YEAR_STR +'|Network',
    'Care3':'Q3|'+ CURR_YEAR_STR +'|Care',          'Connect3':'Q3|'+ CURR_YEAR_STR +'|Connect',            'Insights3':'Q3|'+ CURR_YEAR_STR +'|Insights',              'Network3':'Q3|'+ CURR_YEAR_STR +'|Network',
    'Care4':'Q4|'+ CURR_YEAR_STR +'|Care',          'Connect4':'Q4|'+ CURR_YEAR_STR +'|Connect',            'Insights4':'Q4|'+ CURR_YEAR_STR +'|Insights',              'Network4':'Q4|'+ CURR_YEAR_STR +'|Network',
    'Care5':'Q1|'+ str(CURR_YEAR-1) +'|Care',       'Connect5':'Q1|'+ str(CURR_YEAR-1) +'|Connect',         'Insights5':'Q1|'+ str(CURR_YEAR-1) +'|Insights',           'Network5':'Q1|'+ str(CURR_YEAR-1) +'|Network',
    'Care6':'Q2|'+ str(CURR_YEAR-1) +'|Care',       'Connect6':'Q2|'+ str(CURR_YEAR-1) +'|Connect',         'Insights6':'Q2|'+ str(CURR_YEAR-1) +'|Insights',           'Network6':'Q2|'+ str(CURR_YEAR-1) +'|Network',
    'Care7':'Q3|'+ str(CURR_YEAR-1) +'|Care',       'Connect7':'Q3|'+ str(CURR_YEAR-1) +'|Connect',         'Insights7':'Q3|'+ str(CURR_YEAR-1) +'|Insights',           'Network7':'Q3|'+ str(CURR_YEAR-1) +'|Network',
    'Care8':'Q4|'+ str(CURR_YEAR-1) +'|Care',       'Connect8':'Q4|'+ str(CURR_YEAR-1) +'|Connect',         'Insights8':'Q4|'+ str(CURR_YEAR-1) +'|Insights',           'Network8':'Q4|'+ str(CURR_YEAR-1) +'|Network',
}
### Column Name Arrays ###
BONUS_COLS = [
'Jan - Bonus Accrual', 'Feb - Bonus Accrual', 'Mar - Bonus Accrual',
'Apr - Bonus Accrual', 'May - Bonus Accrual', 'Jun - Bonus Accrual',
'Jul - Bonus Accrual', 'Aug - Bonus Accrual', 'Sep - Bonus Accrual',
'Oct - Bonus Accrual', 'Nov - Bonus Accrual', 'Dec - Bonus Accrual'
]
ORM_COLS = ['Jan Fully-Loaded', 'Feb Fully-Loaded', 'Mar Fully-Loaded', 'Apr Fully-Loaded', 'May Fully-Loaded', 'Jun Fully-Loaded', 'Jul Fully-Loaded', 'Aug Fully-Loaded', 'Sep Fully-Loaded', 'Oct Fully-Loaded', 'Nov Fully-Loaded', 'Dec Fully-Loaded']
PROJ_COLS = [
  'Vendor', 'BU', 'IS Grouping', 'Engineering', 'Function', 'Project', 'Contact', 'EXPENSE_BUCKET'
]
SPEND_COLS = [
  'Jan PnL','Feb PnL','Mar PnL',
  'Apr PnL','May PnL','Jun PnL',
  'Jul PnL','Aug PnL','Sep PnL',
  'Oct PnL','Nov PnL','Dec PnL'
  ]
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
ALL_PROJ_COLS = np.concatenate((PROJ_COLS, SPEND_COLS_W_BONUS))
### Non Shared BUs array
NON_SHARED_BUs = ["Care", "Connect", "Insights", "Network", "Trust"]
### HEADCOUNT CONSTANTS ###
HC_FTE_COLS = [
'EEID', 'BU', 'IS Grouping', 'Engineering', 'Product', 'Function', 'Role', 'Title', 'Employee Name',
'Company Seniority Date', 'Termination Date', 'EXPENSE_BUCKET', 'Open/Filled',
'Supervisor Name', 'Budget Approved?'
]
HC_SPEND_COLS_W_BONUS = [
'Jan PnL','Feb PnL','Mar PnL',
'Apr PnL','May PnL','Jun PnL',
'Jul PnL','Aug PnL','Sep PnL',
'Oct PnL','Nov PnL','Dec PnL',
'Jan - Bonus Accrual','Feb - Bonus Accrual','Mar - Bonus Accrual',
'Apr - Bonus Accrual','May - Bonus Accrual','Jun - Bonus Accrual',
'Jul - Bonus Accrual','Aug - Bonus Accrual','Sep - Bonus Accrual',
'Oct - Bonus Accrual','Nov - Bonus Accrual','Dec - Bonus Accrual', 'PnL Monthly',
]
SPEND_COLS_W_BONUS_AND_HC = [
'Jan PnL','Feb PnL','Mar PnL',
'Apr PnL','May PnL','Jun PnL',
'Jul PnL','Aug PnL','Sep PnL',
'Oct PnL','Nov PnL','Dec PnL',
'Jan - Bonus Accrual','Feb - Bonus Accrual','Mar - Bonus Accrual',
'Apr - Bonus Accrual','May - Bonus Accrual','Jun - Bonus Accrual',
'Jul - Bonus Accrual','Aug - Bonus Accrual','Sep - Bonus Accrual',
'Oct - Bonus Accrual','Nov - Bonus Accrual','Dec - Bonus Accrual', 'PnL Monthly',
'01|HC', '02|HC', '03|HC', '04|HC',
'05|HC', '06|HC', '07|HC', '08|HC',
'09|HC', '10|HC', '11|HC', '12|HC',
'01|HC_JOIN', '02|HC_JOIN', '03|HC_JOIN', '04|HC_JOIN',
'05|HC_JOIN', '06|HC_JOIN', '07|HC_JOIN', '08|HC_JOIN',
'09|HC_JOIN', '10|HC_JOIN', '11|HC_JOIN', '12|HC_JOIN',
'01|HC_DEPART', '02|HC_DEPART', '03|HC_DEPART', '04|HC_DEPART',
'05|HC_DEPART', '06|HC_DEPART', '07|HC_DEPART', '08|HC_DEPART',
'09|HC_DEPART', '10|HC_DEPART', '11|HC_DEPART', '12|HC_DEPART',
]
ALL_HC_PROJ_COLS = np.concatenate((HC_FTE_COLS, HC_SPEND_COLS_W_BONUS))
HC_COLS = [
'01|HC', '02|HC', '03|HC', '04|HC',
'05|HC', '06|HC', '07|HC', '08|HC',
'09|HC', '10|HC', '11|HC', '12|HC',
]
HC_DICT_W_BONUS = {
'Jan PnL':'01|SALARY', 'Feb PnL':'02|SALARY', 'Mar PnL':'03|SALARY',
'Apr PnL':'04|SALARY', 'May PnL':'05|SALARY', 'Jun PnL':'06|SALARY',
'Jul PnL':'07|SALARY', 'Aug PnL':'08|SALARY', 'Sep PnL':'09|SALARY',
'Oct PnL':'10|SALARY', 'Nov PnL':'11|SALARY', 'Dec PnL':'12|SALARY',
'Jan - Bonus Accrual':'01|BONUS', 'Feb - Bonus Accrual':'02|BONUS', 'Mar - Bonus Accrual':'03|BONUS',
'Apr - Bonus Accrual':'04|BONUS', 'May - Bonus Accrual':'05|BONUS', 'Jun - Bonus Accrual':'06|BONUS',
'Jul - Bonus Accrual':'07|BONUS', 'Aug - Bonus Accrual':'08|BONUS', 'Sep - Bonus Accrual':'09|BONUS',
'Oct - Bonus Accrual':'10|BONUS', 'Nov - Bonus Accrual':'11|BONUS', 'Dec - Bonus Accrual':'12|BONUS',
'PnL Monthly':'99|PNL MONTHLY'
}
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
def setup_data_validation_fte(df):
    # This function sets up the data validation for the FTE data
    # It returns a dictionary with the information needed for the validation
    # print the sum of all SPEND_COLS_W_BONUS formatted as a currency
    FTE_SPEND = df[SPEND_COLS_W_BONUS].sum().sum()
    logging.info("the total FTE spend is " + "${:,.0f}".format(FTE_SPEND))
    # print the sum of all SPEND_COLS_W_BONUS by YEAR formatted as a currency
    return {
        'SPEND': FTE_SPEND,
        'SPEND_COLS': SPEND_COLS_W_BONUS
    }
def setup_data_validation_orm(df):
    # This function sets up the data validation for the ORM data
    # It returns a dictionary with the information needed for the validation
    # print the sum of all SPEND_COLS formatted as a currency
    ORM_SPEND = df[ORM_COLS].sum().sum()
    logging.info("the total ORM spend is " + "${:,.0f}".format(ORM_SPEND))
    return {
        'SPEND': ORM_SPEND,
        'SPEND_COLS': ORM_COLS
    }
def setup_data_validation_ftc(df):
    # This function sets up the data validation for the FTC data
    # It returns a dictionary with the information needed for the validation
    # print the sum of all SPEND_COLS formatted as a currency
    FTC_SPEND = df[SPEND_COLS].sum().sum()
    logging.info("the total FTC spend is " + "${:,.0f}".format(FTC_SPEND))
    return {
        'SPEND': FTC_SPEND,
        'SPEND_COLS': SPEND_COLS
    }
def setup_data_validation_pro_serv(df):
    # This function sets up the data validation for the PRO_SERV data
    # It returns a dictionary with the information needed for the validation
    # print the sum of all SPEND_COLS formatted as a currency
    PRO_SERV_SPEND = df[SPEND_COLS].sum().sum()
    logging.info("the total PRO_SERV spend is " + "${:,.0f}".format(PRO_SERV_SPEND))
    
    return {
        'SPEND': PRO_SERV_SPEND,
        'SPEND_COLS': SPEND_COLS
    }
def setup_data_validation_software(df):
    # This function sets up the data validation for the SOFTWARE data
    # It returns a dictionary with the information needed for the validation
    # print the sum of all SPEND_COLS formatted as a currency
    SOFTWARE_SPEND = df[SPEND_COLS].sum().sum()
    logging.info("the total SOFTWARE spend is " + "${:,.0f}".format(SOFTWARE_SPEND))
    return {
        'SPEND': SOFTWARE_SPEND,
        'SPEND_COLS': SPEND_COLS
    }
def setup_data_validation_actuals(df, ACTUAL_FILE_DATE):
    # This function sets up the data validation for the ACTUALS data
    # It returns a dictionary with the information needed for the validation
    df = df.copy(deep=True)
    # if the Amount column has parentheses, then replace them with a negative sign
    df['Amount'] = df['Amount'].str.replace('(', '-', regex=False)
    df['Amount'] = df['Amount'].str.replace(')', '', regex=False)
    # if the Amount column has commas, then remove them
    df['Amount'] = df['Amount'].str.replace(',', '')
    # convert the Amount column to a float
    df['Amount'] = df['Amount'].astype(float)
    # convert the "Date" column to a Year
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    df['Month'] = pd.to_datetime(df['Date']).dt.month
    # print the sum of all SPEND_COLS formatted as a currency
    ACTUALS_SPEND = df['Amount'].sum()
    logging.debug("The raw actuals spend is " + "${:,.0f}".format(ACTUALS_SPEND))
    # after removing the "CARE : 2800 PATIENTS CHOICE" and "DIRECT : 1600 SANO" rows
    df = df.loc[(df['BU']!='1100 Nomi Care : 2800 Patients Choice') & (df['BU']!='1050 Open Network : 1600 Sano')]
    ACTUALS_SPEND_NO_SANO_OR_PC = df['Amount'].sum()
    logging.debug("...removed Sano and Patients Choice (" + "${:,.0f}".format(ACTUALS_SPEND - ACTUALS_SPEND_NO_SANO_OR_PC) + ") from the Actuals spend")
    # ACTUALS_SPEND_EXCLUDING_FUTURE
    df = df[(df['Year'] < CURR_YEAR) | ((df['Year'] == CURR_YEAR) & (df['Month'] <= ACTUAL_FILE_DATE))]
    ACTUALS_SPEND_EXCLUDING_FUTURE = df['Amount'].sum()
    logging.debug("...removed future months (" + "${:,.0f}".format(ACTUALS_SPEND_NO_SANO_OR_PC - ACTUALS_SPEND_EXCLUDING_FUTURE) + ") from the Actuals spend")
    logging.info("The actuals spend is " + "${:,.0f}".format(ACTUALS_SPEND_EXCLUDING_FUTURE))
    # df_actuals_check is a dataframe that contains the sum of the Amount column by Year, Month, and Expense Bucket - Account field
    df_actuals_check = df.groupby(['Year', 'Month', 'Expense Bucket - Account field'])['Amount'].sum()
    df_actuals_check = df_actuals_check.reset_index()
    df_actuals_check = df_actuals_check.rename(columns={'Amount': 'VAL_EXPECTED', 'Expense Bucket - Account field': 'VAL_MODEL', 'Year': 'YEAR', 'Month': 'MONTH'})
    # add a column SEGMENT to the df_actuals_check dataframe that is VALIDATION
    df_actuals_check['SEGMENT'] = 'VALIDATION'
    # add a column VAL_CHECKPOINT to the df_actuals_check dataframe that is "C1 - ACTUALS"
    df_actuals_check['VAL_CHECKPOINT'] = 'C1 - ACTUALS'
    # alter the VAL_MODEL column using EXPENSE_BUCKET_DICT
    df_actuals_check['VAL_MODEL'] = df_actuals_check['VAL_MODEL'].map(EXPENSE_BUCKET_DICT)
    return {
        'SPEND': ACTUALS_SPEND_EXCLUDING_FUTURE,
        'SPEND_COLS': ['Amount'],
        'SPEND_DETAIL': df_actuals_check
    }
def setup_for_data_validation(ACTUAL_FILE_DATE, FILE_DICT):
    # This function sets up the data validation
    # It runs the data validation setup functions
    # and returns a dictionary with the information needed for the validation
    # get the FTE data
    FTE = FILE_DICT['FTE']
    ORM = FILE_DICT['ORM']
    FTC = FILE_DICT['FTC']
    PRO_SERV = FILE_DICT['PRO_SERV']
    SOFTWARE = FILE_DICT['SOFTWARE']
    ACTUALS = FILE_DICT['ACTUALS']
    # set up the data validation for the FTE data
    val_fte = setup_data_validation_fte(FTE)
    # set up the data validation for the ORM data
    val_orm = setup_data_validation_orm(ORM)
    # set up the data validation for the FTC data
    val_ftc = setup_data_validation_ftc(FTC)
    # set up the data validation for the PRO_SERV data
    val_pro_serv = setup_data_validation_pro_serv(PRO_SERV)
    # set up the data validation for the SOFTWARE data
    val_software = setup_data_validation_software(SOFTWARE)
    # set up the data validation for the ACTUALS data
    val_actuals = setup_data_validation_actuals(ACTUALS, ACTUAL_FILE_DATE)
    return {
        'FTE': val_fte,
        'ORM': val_orm,
        'FTC': val_ftc,
        'PRO_SERV': val_pro_serv,
        'SOFTWARE': val_software,
        'ACTUALS': val_actuals
    }
def clean_data(df):
    # function that cleans the data
    # it replaces Inc(.) with Inc.
    # it removes duplicate whitespaces from the data
    # it replaces empty cells with NaN
    # it removes leading and trailing spaces from column names
    df = df.copy(deep=True)    
    df.replace("(?i)Inc\.?","Inc.",regex=True,inplace=True)
    df.replace('\s+',' ',regex=True,inplace=True)
    df.replace(r'^\s*$',np.nan,regex=True,inplace=True)
    df.columns = df.columns.str.strip()
    # if there first three columns are empty for a row, drop the row
    df.dropna(subset=df.columns[:5], how='all', inplace=True)
    return df
def clean_allocation_sheet(df, name_map):
    # function that cleans the allocation sheet
    df = clean_data(df)
    # fill in missing values with 0
    df.fillna(0, inplace=True)
    df.rename(columns=ALLOCATION_COL_DICT, inplace=True)
    # get the column that contains the word "Key"
    key_col = [col for col in df.columns if 'Key' in col]
    # if the number of dashes in the key column is 1, then add a dash to the end of the string "-NA"
    df.loc[df[key_col[0]].str.count('-') == 1, key_col[0]] = df[key_col[0]] + '-NA'
    # split the key column into 3 columns
    df[['BU','Vendor', 'Other']] = df[key_col[0]].str.split("-", n=2, expand=True)
    id_col = 'Vendor'
    value_col_list = ['Care', 'Connect', 'Insights', 'Network']
    # get a list of columns that contain one of the strings in the value_col_list
    value_cols = [col for col in df.columns if any(x in col for x in value_col_list)]
    df = pd.melt(df,id_vars=[id_col,'SOURCE'],value_vars=value_cols,value_name='ALLOCATION',var_name='QUARTER_YEAR_BU')
    df[['QUARTER','YEAR','BU']] = df['QUARTER_YEAR_BU'].str.split('|', expand=True)
    df = df.merge(name_map, how='left', left_on='Vendor', right_on='Entity')
    df['Vendor'] = df['Entity (New)'].fillna(df['Vendor'])
    # if there are null values in the QUARTER, BU, Vendor, YEAR, or SOURCE columns, print the rows
    if df.loc[(df['QUARTER'].isnull()) | (df['BU'].isnull()) | (df['Vendor'].isnull()) | (df['YEAR'].isnull()) | (df['SOURCE'].isnull())].shape[0] > 0:
        logging.warning("There are null values in the QUARTER, BU, Vendor, YEAR, or SOURCE columns of the allocation sheet")
    # get the mean of the ALLOCATION column for each QUARTER, YEAR, Vendor, BU, and SOURCE
    df = df.groupby(['QUARTER','YEAR','Vendor','BU','SOURCE']).agg({'ALLOCATION':'mean'}).reset_index()
    
    df['ALLOCATION_KEY'] = df['QUARTER'] + "|" + df['BU'].str.upper() + "|SHARED SERVICES|" + df['Vendor'].str.upper() + "|" + df['YEAR'] + "|" + df['SOURCE']
    
    # get the sum of the ALLOCATION column for each QUARTER, YEAR, Vendor, and SOURCE
    df_allo_total_by_Q = df.groupby(['QUARTER','YEAR','Vendor','SOURCE']).agg({'ALLOCATION':'sum'}).reset_index()
    # filter the data frame for rows where the ALLOCATION column is not equal to 1
    df_allo_total_by_Q = df_allo_total_by_Q.loc[df_allo_total_by_Q['ALLOCATION'] != 1]
    # group by YEAR, Vendor, and SOURCE and ALLOCATION and aggregate the QUARTER column
    df_allo_total_by_Q_sum = df_allo_total_by_Q.groupby(['YEAR','Vendor','SOURCE','ALLOCATION']).agg({'QUARTER':', '.join}).reset_index()
    df_allo_total_missing = df_allo_total_by_Q.loc[df_allo_total_by_Q['ALLOCATION'] == 0]
    
    # if there are rows in the data frame, print the rows
    if df_allo_total_by_Q_sum.shape[0] > 0:
        ERROR_ARRAY.append(df_allo_total_by_Q_sum)
        logging.warning("There are some allocation-quarters that do not add up to 1.0")
        logging.debug(df_allo_total_by_Q_sum.to_string(index=False))
        # if there are rows in the data frame, print the rows
        if df_allo_total_missing.shape[0] > 0:
                # store the sum of the ALLOCATION column in df where the SOURCE is "FTE_AND_OPEN_ROLES" in a variable
                ALLO_SUM_PRIOR = df['ALLOCATION'].sum()
                # for each Vendor in df_allo_total_missing, assign .5 to the
                # ALLOCATION column in df where the Vendor, Quarter, and Year is the same and the BU is
                # "CARE" or "CONNECT" and the SOURCE is "FTE_AND_OPEN_ROLES"
                # if the BU is "INSIGHTS" or "NETWORK", assign .0 to the ALLOCATION column
                for index, row in df_allo_total_missing.iterrows():
                    df.loc[(df['Vendor'] == row['Vendor']) & (df['QUARTER'] == row['QUARTER']) & (df['YEAR'] == row['YEAR']) & (df['BU'].isin(['Care','Connect'])), 'ALLOCATION'] = .5
                    df.loc[(df['Vendor'] == row['Vendor']) & (df['QUARTER'] == row['QUARTER']) & (df['YEAR'] == row['YEAR']) & (df['BU'].isin(['Insights','Network'])), 'ALLOCATION'] = 0   
                # store the sum of the ALLOCATION column in df where the SOURCE is "FTE_AND_OPEN_ROLES" in a variable
                ALLO_SUM_AFTER = df['ALLOCATION'].sum()
                logging.info("After assigning .5 to CARE/CONNECT and 0 to INSIGHTS/NETWORK, the sum of the ALLOCATION column for FTE_AND_OPEN_ROLES went from " + str(ALLO_SUM_PRIOR) + " to " + str(ALLO_SUM_AFTER))
                # check that the fix worked
                df_allo_total_by_Q = df.groupby(['QUARTER','YEAR','Vendor','SOURCE']).agg({'ALLOCATION':'sum'}).reset_index()
                # round the ALLOCATION column to 2 decimal places
                df_allo_total_by_Q['ALLOCATION'] = df_allo_total_by_Q['ALLOCATION'].round(2)
                # filter the data frame for rows where the ALLOCATION column is not equal to 1
                df_allo_total_by_Q = df_allo_total_by_Q.loc[df_allo_total_by_Q['ALLOCATION'] != 1]
                if df_allo_total_by_Q.shape[0] > 0:
                    logging.error("The fix did not work")
                    logging.debug(df_allo_total_by_Q.to_string(index=False))
        else:
            print("No rows have an ALLOCATION value of 0")
            print("")
    else:
        print("All rows have an ALLOCATION value of 1")
        print("")
    df = df[['ALLOCATION_KEY','ALLOCATION']]
    df = df.loc[df['ALLOCATION'].notnull()]
    # Group by ALLOCATION_KEY and average the ALLOCATION
    df = df.groupby(['ALLOCATION_KEY']).mean().reset_index()
    return df
def remove_string_from_column(df, column, string):
    # function that removes a string from a column
    # after removing the string, convert any empty cells to NaN
    logging.debug(list(df[column].unique()))
    df[column] = df[column].str.replace(string, '', regex=True)
    df[column].replace(r'^\s*$',np.nan,regex=True,inplace=True)
    logging.debug(list(df[column].unique()))
    return df
def format_cash_view(df):
    df = df.copy(deep=True)
    # fill the blank cells in 'Cash View (FTC, PS, SW)' with 'ACCRUALS' and convert to uppercase
    df['Cash View (FTC, PS, SW)'].fillna('ACCRUALS', inplace=True)
    df['Cash View (FTC, PS, SW)'] = df['Cash View (FTC, PS, SW)'].str.upper()
    df.loc[  (df['SAL_BONUS'] == 'SALARY') & (df['EXPENSE_BUCKET'] == 'FTE'), 'Cash View (FTC, PS, SW)'] = 'CASH'
    df.loc[  (df['SAL_BONUS'] != 'SALARY') & (df['EXPENSE_BUCKET'] == 'FTE'), 'Cash View (FTC, PS, SW)'] = 'ACCRUALS'
    # rename the column 'Cash View (FTC, PS, SW)' to 'CASH_VIEW'
    df.rename(columns={'Cash View (FTC, PS, SW)':'CASH_VIEW'}, inplace=True)
    logging.debug("...unique values in CASH_VIEW column: " + str(list(df['CASH_VIEW'].unique())))
    return df
def join_name_map_to_actuals(df_actuals, df_name_map):
    # function that joins the name map to the actuals file
    df_actuals = df_actuals.copy(deep=True)
    df_name_map = df_name_map.copy(deep=True)
    # Rename Function to Function (New)
    df_name_map.rename(columns={'Function':'Function (New)'}, inplace=True)
    # Drop the columns that are not needed
    try:
        df_name_map.drop(['Expense Bucket'], axis=1, inplace=True)
    except KeyError:
        pass
    # if the Prepaid Vendor column is not "X", then it is null
    df_name_map.loc[df_name_map['Prepaid Vendor'] != 'X', 'Prepaid Vendor'] = np.nan
    # filter the data frame for rows where Prepaid Vendor is not null and get a list of the unique values in the Vendor column
    prepaid_vendor_list = df_name_map[df_name_map['Prepaid Vendor'].notnull()]['Entity (New)'].unique()
    logging.debug("Prepaid Vendors:" + str(prepaid_vendor_list))
    df = df_actuals.merge(df_name_map, how='left', on='Entity').copy(deep=True)
    # For vendors missing from name map, use vendor name in actuals file
    df['Entity (New)'].fillna(df['Entity'], inplace=True)
    # Rows without vendor in the actuals file receive '# NO VENDOR'
    df['Entity (New)'].fillna("# NO VENDOR", inplace=True)
    # Fill the Function (New) column with the 'Function' column if it is blank for FTE rows
    df.loc[    (df['EXPENSE_BUCKET'] == 'FTE'), 'Function (New)'] = df['FTE Function 2']
    # Drop the columns that are not needed
    df.drop(['Entity', 'FTE Function 2', 'Function'], axis=1, inplace=True)
    # Rename Entity (New) to Vendor
    df.rename(columns={'Entity (New)':'Vendor', 'Function (New)':'Function', 'Amount':'AMOUNT'}, inplace=True)
    # For rows where the Vendor is in the prepaid_vendor_list, set the Prepaid Vendor column to 'X'
    df.loc[df['Vendor'].isin(prepaid_vendor_list), 'Prepaid Vendor'] = 'X'
    # Fill the NA values in the 'Function' column with 'NO FUNCTION'
    df['Function'].fillna('# NO FUNCTION', inplace=True)
    
    # Sort the data frame by Vendor and Function
    df.sort_values(by=['Vendor', 'Function'], inplace=True)
    return df
def clean_actuals_fte(df):
    # function that cleans the actuals FTE data
    df = df.copy()
    ACT_FTE_COLS = [
        'Vendor', 'BU', 'IS Grouping', 'Engineering', 'Function',
        'Project', 'Contact', 'EXPENSE_BUCKET', 'EXPENSE_BUCKET_2',
        'MONTH', 'QUARTER', 'YEAR', 'AMOUNT', 'SAL_BONUS', 'Type',
        'CASH_VIEW', 'PROJ_ACT', 'ALLO_TYPE']
    # create a new array using ACT_FTE_COLS but remove "AMOUNT"
    ACT_FTE_COLS_NO_AMOUNT = ACT_FTE_COLS.copy()
    ACT_FTE_COLS_NO_AMOUNT.remove('AMOUNT')
    df.loc[df['EXPENSE_BUCKET'] == 'FTE']
    df['ALLO_TYPE'] = np.where(df['FTE Function 1'] == 'Shared Services',"SHARED SERVICES", "NOT SHARED SERVICES")
    df['ALLO_TYPE'].fillna("NOT SHARED SERVICES", inplace=True)
    # df['Function'] = df['FTE Function 2']
    df['EXPENSE_BUCKET_2'] = 'FTE_AND_OPEN_ROLES'
    df = df[ACT_FTE_COLS] # filter columns
    df = df.groupby(ACT_FTE_COLS_NO_AMOUNT).sum() # get the sum of amount
    df.reset_index(inplace=True)
    df['ALLOCATION']=1
    return df
def clean_actuals(df, actuals_date, name_map):
    # function that cleans the actuals data
    df = clean_data(df)
    # rename columns
    df.rename(columns={'FSLI v3':'IS Grouping'}, inplace=True)
    # if the Amount column has parentheses, then replace them with a negative sign
    df['Amount'] = df['Amount'].str.replace('(', '-', regex=False)
    df['Amount'] = df['Amount'].str.replace(')', '', regex=False)
    # if the Amount column has commas, then remove them
    df['Amount'] = df['Amount'].str.replace(',', '', regex=False)
    # convert the Amount column to a float
    df['Amount'] = df['Amount'].astype(float)
    # add constants
    df['Contact']   = "# NO CONTACT"
    df['Function']  = '# NO FUNCTION'
    df['PROJ_ACT']  = "ACTUAL"
    # fill in missing values
    df['Project'].fillna("# NO PROJECT", inplace=True)
    df['Type'].fillna("# NO TYPE", inplace=True)
    df['Engineering'].fillna("NOT ENGINEERING", inplace=True)
    # format date columns
    df['YEAR'] = pd.DatetimeIndex(df['Date']).year
    df['QUARTER'] = pd.DatetimeIndex(df['Date']).quarter.astype(str)
    df['MONTH'] = pd.DatetimeIndex(df['Date']).month.map(lambda x: f'{x:0>2}')
    # format MONTH_INT column
    df['MONTH_INT'] = df['MONTH'].astype(int)
    df['YEAR_INT'] = df['YEAR'].astype(int)
    try:
        # convert ACTUAL_FILE_DATE to int
        ACTUAL_FILE_DATE = int(actuals_date)
    except ValueError:
        logging.warning("...ACTUAL_FILE_DATE is not an integer, setting to zero")
        ACTUAL_FILE_DATE = 0
    # format BU column
    df = remove_string_from_column(df, 'BU', '\d{4}\s+Nomi( Health Inc)?[. ]?( : \d{4} )?')
    df[['BU', 'IS Grouping']] = df[['BU', 'IS Grouping']].fillna("# BLANK")
    df['IS Grouping'] = df['IS Grouping'].replace(IS_GROUP_DICT)
    df['EXPENSE_BUCKET'] = df['Expense Bucket - Account field'].replace(EXPENSE_BUCKET_DICT)
    df['SAL_BONUS'] = np.where(df['Account'] == "6044 Bonus expense (accrual)","BONUS", "SALARY")
    # print removing future months and print the amount of spend removed as a currency.
    # this amount needs to be used in data validation
    logging.debug("...removing future months from actuals")
    # print the number of rows removed
    logging.debug("...number of rows removed: " + str(len(df.loc[(df['YEAR_INT']>CURR_YEAR) | ((df['MONTH_INT']>ACTUAL_FILE_DATE) & (df['YEAR_INT']==CURR_YEAR))])))
    ACTUALS_FUTURE_SPEND = df.loc[(df['YEAR_INT']>CURR_YEAR) | ((df['MONTH_INT']>ACTUAL_FILE_DATE) & (df['YEAR_INT']==CURR_YEAR))]['Amount'].sum()
    # print as a currency
    logging.debug("...amount of spend removed from actuals: " + "${:,.0f}".format(ACTUALS_FUTURE_SPEND))
    # Filter rows in Actuals to exclude future months
    # remove rows where YEAR_INT is greater than CURR_YEAR
    # remove rows where MONTH_INT is greater than ACTUAL_FILE_DATE and YEAR_INT is equal to CURR_YEAR
    df = df.loc[~((df['YEAR_INT']>CURR_YEAR) | ((df['MONTH_INT']>ACTUAL_FILE_DATE) & (df['YEAR_INT']==CURR_YEAR)))]
    df = format_cash_view(df)
    df = join_name_map_to_actuals(df, name_map)
    # If the Prepaid Vendor column exists
    if 'Prepaid Vendor' in df.columns:
        # set CASH_VIEW to 'CASH' for rows where the Prepaid Vendor column is 'X'
        df.loc[df['Prepaid Vendor'] == 'X', 'CASH_VIEW'] = 'CASH'
    df_fte = df.copy(deep=True)
    df_fte = df_fte.loc[df_fte['EXPENSE_BUCKET'] == 'FTE']
    df_fte = clean_actuals_fte(df_fte)
    # Filter rows in Actuals to exclude FTE
    df = df.loc[df['EXPENSE_BUCKET'] != 'FTE']
    df = pd.concat([df, df_fte], ignore_index=True)
    # Filter actuals columns
    ACTUALS_COLS = ['Vendor', 'BU', 'IS Grouping', 'Engineering', 'Function', 'Project', 'Contact', 'PROJ_ACT', 'MONTH', 'AMOUNT', 'QUARTER', 'YEAR', 'Type', 'CASH_VIEW', 'EXPENSE_BUCKET', 'SAL_BONUS']
    ACTUALS_COLS_NO_AMOUNT = ['Vendor', 'BU', 'IS Grouping', 'Engineering', 'Function', 'Project', 'Contact', 'PROJ_ACT', 'MONTH', 'QUARTER', 'YEAR', 'Type', 'CASH_VIEW', 'EXPENSE_BUCKET', 'SAL_BONUS']
    df = df[ACTUALS_COLS]
    df = df.groupby(ACTUALS_COLS_NO_AMOUNT).sum()
    df.reset_index(inplace=True)
    return df
def clean_projections(df):
    df = df.copy()
    df = df[ALL_PROJ_COLS]
    df = df.groupby([
        'Vendor',
        'BU',
        'IS Grouping',
        'Engineering',
        'Function',
        'Project',
        'Contact',
        'EXPENSE_BUCKET'
        ], dropna=False)[SPEND_COLS_W_BONUS].sum()
    # Clean summary data by reseting the index and parsing key
    df.reset_index(inplace=True)
    ### FORMAT PROJECTIONS ###
    df = pd.melt(
        df,
        id_vars=[
        'Vendor',
        'BU',
        'IS Grouping',
        'Engineering',
        'Function',
        'Project',
        'Contact',
        'EXPENSE_BUCKET'
        ],
        value_vars=SPEND_COLS_W_BONUS,
        var_name='MONTH',
        value_name='AMOUNT'
        )
    df['MONTH'] = df['MONTH'].replace(DICT_W_BONUS)
    df[['MONTH','SAL_BONUS']] = df['MONTH'].str.split("|", expand=True)
    df['YEAR'] = CURR_YEAR
    df['Type'] = "# NO TYPE"
    df = df.loc[(df['AMOUNT'] != 0) & (df['AMOUNT'].notnull())]
    df['PROJ_ACT'] = 'PROJECTION'
    df['QUARTER'] = pd.to_datetime(df['MONTH'].values, format='%m').astype('period[Q]').astype(str).str[-1:]
    return df
def clean_fte(df):
    # function that cleans the FTE data
    df = clean_data(df)
    df.rename(columns={'Supervisor Name': 'Contact'}, inplace=True)
    df["Vendor"] = "# NO VENDOR"
    df["Project"] = "# NO PROJECT"
    df['Engineering'].fillna('NOT ENGINEERING', inplace=True)
    df['EXPENSE_BUCKET'] = 'FTE'
    df = df.loc[(df['BU'] != '') & (df['BU'].notnull())]
    df = clean_projections(df)
    return df
def clean_orm(df):
    # filter for HC = 1
    df = df.loc[df['HC'] == 1]
    # function that cleans the ORM data
    df = clean_data(df)
    df.rename(columns={
            'BU-FUNCTION KEY'       : 'BU-Function Key',
            'Start Date'            : 'Company Seniority Date',
            'Monthly Fully-Loaded'  : 'PnL Monthly',
            'Supervisor Name'       : 'Contact'
        }, inplace=True)
    df.columns = df.columns.str.replace("Fully-Loaded", "PnL")
    df["Vendor"]            = "# NO VENDOR"
    df["Project"]           = "# NO PROJECT"
    df['EXPENSE_BUCKET']    = "OPEN_ROLES"
    df[BONUS_COLS] = 0
    df['Engineering'].fillna('NOT ENGINEERING', inplace=True)
    df = df.loc[(df['BU'] != '') & (df['BU'].notnull())]
    df = clean_projections(df)
    return df
def clean_ftc(df):
    # function that cleans the FTC data
    df = clean_data(df)
    df.rename(columns={'Owner': 'Contact'}, inplace=True)
    df['Project'] = df['Project'].fillna("# NO PROJECT")
    df['Contact'] = df['Contact'].fillna("# NO CONTACT")
    df['Engineering'] = "NOT ENGINEERING"
    df['EXPENSE_BUCKET'] = 'FTC'
    df[BONUS_COLS] = 0
    df = clean_projections(df)
    return df
def clean_pro_serv(df):
    # function that cleans the Professional Services data
    df = clean_data(df)
    df['Engineering'] = "NOT ENGINEERING"
    df['EXPENSE_BUCKET'] = 'PRO_SERV'
    df[BONUS_COLS] = 0
    df = clean_projections(df)
    return df
def clean_software(df):
    # function that cleans the Software data
    df = clean_data(df)
    df.rename(columns={'Owner': 'Contact'}, inplace=True)
    df["Project"] = "# NO PROJECT"
    df['Engineering'] = "NOT ENGINEERING"
    df['EXPENSE_BUCKET'] = 'SOFTWARE'
    df[BONUS_COLS] = 0
    df = clean_projections(df)
    return df
def validate(expected, actual):
    # this function takes an expected value and an actual value
    # it rounds to the nearest whole number and prints if they are the same
    # it returns True if they are the same and False if they are not
    # round to the nearest whole number
    expected = round(expected)
    actual = round(actual)
    # print if they are the same (or within .01% of each other)
    # print the numbers as currency with commas and no decimals
    # if there is a difference, print the difference as a currency and percentage
    if abs(expected - actual) <= (expected * .0001):
        logging.info("the spend is within .01% of the expected spend")
        return True
    else:
        logging.warning("the expected spend is " + "${:,.0f}".format(expected))
        logging.warning("the actual spend is " + "${:,.0f}".format(actual))
        logging.warning("the spend is not within .01% of the expected spend")
        logging.warning("the difference is " + "${:,.0f}".format(actual - expected))
        logging.warning("the difference is " + "{:.2%}".format((actual - expected) / expected))
        return False
def validation_checkpoint(val_dict, df_fte, df_open_roles, df_ftc, df_pro_serv, df_software, df_actuals):
    FTE_SUM_C0 = val_dict['FTE']['SPEND']
    OPEN_ROLES_SUM_C0 = val_dict['ORM']['SPEND']
    FTC_SUM_C0 = val_dict['FTC']['SPEND']
    PRO_SERV_SUM_C0 = val_dict['PRO_SERV']['SPEND']
    SOFTWARE_SUM_C0 = val_dict['SOFTWARE']['SPEND']
    ACTUALS_SUM_C0 = val_dict['ACTUALS']['SPEND']
    ACTUALS_SUM_DETAIL_C0 = val_dict['ACTUALS']['SPEND_DETAIL']
    FTE_SUM_C1 = df_fte['AMOUNT'].sum()
    OPEN_ROLES_SUM_C1 = df_open_roles['AMOUNT'].sum()
    FTC_SUM_C1 = df_ftc['AMOUNT'].sum()
    PRO_SERV_SUM_C1 = df_pro_serv['AMOUNT'].sum()
    SOFTWARE_SUM_C1 = df_software['AMOUNT'].sum()
    ACTUALS_SUM_C1 = df_actuals['AMOUNT'].sum()
    c1_fte_valid = validate(FTE_SUM_C0, FTE_SUM_C1)
    c1_open_roles_valid = validate(OPEN_ROLES_SUM_C0, OPEN_ROLES_SUM_C1)
    c1_ftc_valid = validate(FTC_SUM_C0, FTC_SUM_C1)
    c1_pro_serv_valid = validate(PRO_SERV_SUM_C0, PRO_SERV_SUM_C1)
    c1_software_valid = validate(SOFTWARE_SUM_C0, SOFTWARE_SUM_C1)
    c1_actuals_valid = validate(ACTUALS_SUM_C0, ACTUALS_SUM_C1)
def duplicate_df_for_shared_services(df):
    # if the dataframe is missing the Vendor column, add it
    if 'Vendor' not in df.columns:
        df['Vendor'] = "# NO VENDOR"
    df_not_shared = df.copy(deep=True)
    # filter for BU in NON_SHARED_BUs array
    df_not_shared = df_not_shared[df_not_shared['BU'].isin(NON_SHARED_BUs)]
    df_not_shared['ALLO_TYPE'] = 'NOT SHARED SERVICES'
    df_shared = df.copy(deep=True)
    # filter for BU not in NON_SHARED_BUs array
    df_shared = df_shared[~df_shared['BU'].isin(NON_SHARED_BUs)]
    df_shared['ALLO_TYPE'] = 'SHARED SERVICES'
    df_shared_care = df_shared.copy(deep=True)
    df_shared_connect = df_shared.copy(deep=True)
    df_shared_network = df_shared.copy(deep=True)
    df_shared_insights = df_shared.copy(deep=True)
    df_shared_care['BU'] = 'CARE'
    df_shared_connect['BU'] = 'CONNECT'
    df_shared_network['BU'] = 'NETWORK'
    df_shared_insights['BU'] = 'INSIGHTS'
    df_shared_dups = pd.concat((df_shared_care, df_shared_connect, df_shared_network, df_shared_insights), ignore_index=True)
    df_shared_dups['ALLOCATION_KEY'] = "Q" + df_shared_dups['QUARTER'].astype(str) + "|" + df_shared_dups['BU'].str.upper() + "|" + df_shared_dups['ALLO_TYPE'].str.upper() + "|" + df_shared_dups['Vendor'].str.upper() + "|" + df_shared_dups['YEAR'].astype(str) + "|" + df_shared_dups['EXPENSE_BUCKET']
    df_shared_dups.loc[(df_shared_dups['EXPENSE_BUCKET_2']=='FTE_AND_OPEN_ROLES'), 'ALLOCATION_KEY'] = "Q" + df_shared_dups['QUARTER'].astype(str) + "|" + df_shared_dups['BU'].str.upper() + "|" + df_shared_dups['ALLO_TYPE'].str.upper() + "|" + df_shared_dups['Function'].str.upper() + "|" + df_shared_dups['YEAR'].astype(str) + "|" + df_shared_dups['EXPENSE_BUCKET_2']
    # are there any rows where the ALLOCATION_KEY is null?
    if df_shared_dups.loc[df_shared_dups['ALLOCATION_KEY'].isnull()].shape[0] > 0:
        logging.debug("The first 15 rows where the ALLOCATION_KEY is null:")
        logging.debug(df_shared_dups.loc[df_shared_dups['ALLOCATION_KEY'].isnull()].head(15))
    df = pd.concat((df_not_shared, df_shared_dups), ignore_index=True)
    return df
def join_allocation_to_df(df, df_allocation):
    # function that joins the allocation data to the df
    # first, duplicate the df for the shared services
    # create a new column EXPENSE_BUCKET_2
    df['EXPENSE_BUCKET_2'] = df['EXPENSE_BUCKET']
    df.loc[((df['EXPENSE_BUCKET']=='FTE') | (df['EXPENSE_BUCKET']=='OPEN_ROLES')), 'EXPENSE_BUCKET_2'] = 'FTE_AND_OPEN_ROLES'
    # if the PROJ_ACT column is PROJECTION and the EXPENSE_BUCKET_2 column is FTE_AND_OPEN_ROLES,
    # use the function column instead of the Vendor column to calculate df_sum
    if df.loc[(df['PROJ_ACT']=='PROJECTION') & (df['EXPENSE_BUCKET_2']=='FTE_AND_OPEN_ROLES')].shape[0] > 0:
        df_sum = df.groupby(['EXPENSE_BUCKET_2', 'Function', 'YEAR'])['AMOUNT'].sum().reset_index()
        # rename the Function column to Vendor
        df_sum.rename(columns={'Function': 'Vendor'}, inplace=True)
    else:
        df_sum = df.groupby(['EXPENSE_BUCKET_2', 'Vendor', 'YEAR'])['AMOUNT'].sum().reset_index()
    df = duplicate_df_for_shared_services(df)
    # filter df_allocation to remove rows where the ALLOCATION_KEY is null or the ALLOCATION is null or the ALLOCATION is 0
    df_allocation = df_allocation.loc[~df_allocation['ALLOCATION_KEY'].isnull()]
    df_allocation = df_allocation.loc[~df_allocation['ALLOCATION'].isnull()]
    df_allocation = df_allocation.loc[df_allocation['ALLOCATION'] != 0]    
    
    df = df.merge(df_allocation, how='left', left_on='ALLOCATION_KEY', right_on='ALLOCATION_KEY')
    df['ALLOCATION'] = df['ALLOCATION'].fillna(0).replace('', 0)
    # if the ALLO_TYPE is NOT SHARED SERVICES, then the ALLOCATION should be 1
    df.loc[(df['ALLO_TYPE']=='NOT SHARED SERVICES'), 'ALLOCATION'] = 1
    # if the PROJ_ACT is ACTUAL and the EXPENSE_BUCKET_2 is FTE_AND_OPEN_ROLES, then the ALLOCATION should be 1
    df.loc[(df['PROJ_ACT']=='ACTUAL') & (df['EXPENSE_BUCKET_2']=='FTE_AND_OPEN_ROLES'), 'ALLOCATION'] = 1
    # if there are rows where Vendor is "# NO VENDOR" and the ALLOCATION is 0,
    # then replace the ALLOCATION with .5 for CARE and CONNECT
    # print the number of rows where Vendor is "# NO VENDOR" and the ALLOCATION is 0
    logging.debug("number of rows where Vendor is # NO VENDOR and the ALLOCATION is 0: " + str(df.loc[(df['Vendor']=='# NO VENDOR') & (df['ALLOCATION']==0)].shape[0]))
    logging.debug(df.loc[(df['Vendor']=='# NO VENDOR') & (df['ALLOCATION']==0)].head(10).to_string())
    # print the number of rows where ALLOCATION is 0
    logging.debug("number of rows where ALLOCATION is 0: " + str(df.loc[df['ALLOCATION']==0].shape[0]))
    logging.debug("allocating .5 to # NO VENDOR for CARE and CONNECT")
    # print the number of rows where Vendor is "# NO VENDOR" and the ALLOCATION is 0 and the SOURCE is not "FTE_AND_OPEN_ROLES"
    logging.debug("number of rows where Vendor is # NO VENDOR and the ALLOCATION is 0 and the SOURCE is not FTE_AND_OPEN_ROLES: " + str(df.loc[(df['Vendor']=='# NO VENDOR') & (df['ALLOCATION']==0) & (df['EXPENSE_BUCKET_2']!='FTE_AND_OPEN_ROLES')].shape[0]))
    df.loc[(df['Vendor']=='# NO VENDOR') & (df['ALLOCATION']==0) & (df['BU']=='CARE') & (df['EXPENSE_BUCKET_2']!='FTE_AND_OPEN_ROLES'), 'ALLOCATION'] = .5
    df.loc[(df['Vendor']=='# NO VENDOR') & (df['ALLOCATION']==0) & (df['BU']=='CONNECT') & (df['EXPENSE_BUCKET_2']!='FTE_AND_OPEN_ROLES'), 'ALLOCATION'] = .5
    logging.debug("after adjusting # NO VENDOR, the number of rows where ALLOCATION is 0 is: " + str(df.loc[df['ALLOCATION']==0].shape[0]))
    df['ALLOCATION'] = df['ALLOCATION'].astype(float)
    df['ALLOCATED_AMOUNT'] = df['AMOUNT'] * df['ALLOCATION']
    # if Amount is null, then fill it with 0
    df['AMOUNT'] = df['AMOUNT'].fillna(0)
    # if Allocated Amount is null, then fill it with 0
    df['ALLOCATED_AMOUNT'] = df['ALLOCATED_AMOUNT'].fillna(0)
    # if Amount is not 0 then Allocated Amount should not be 0
    # This happens because the ALLOCATION is 0
    # Replace the ALLOCATION for these
    # are there rows where AMOUNT is not null and the AMOUNT is not 0
    # and ALLOCATED_AMOUNT is null or 0?
    df_missing_spend = df.loc[(df['AMOUNT'] != 0) & ((df['ALLOCATED_AMOUNT'] == 0)) & ((df['PROJ_ACT'] == "ACTUAL"))]
    if df_missing_spend.shape[0] > 0:
        logging.debug("There are rows where AMOUNT is not null and the AMOUNT is not 0 and ALLOCATED_AMOUNT is null or 0")
        # print the unique values of BU
        logging.debug("The unique values of BU are: " + str(df_missing_spend['BU'].unique()))
        # filter out rows where BU is "NETWORK" or "INSIGHTS"
        df_missing_spend = df_missing_spend.loc[(df_missing_spend['BU'] != 'NETWORK') & (df_missing_spend['BU'] != 'INSIGHTS')]
        # print the unique values of BU
        logging.debug("The unique values of BU are: " + str(df_missing_spend['BU'].unique()))
        # filter out rows where Vendor is "# NO VENDOR"
        df_missing_spend = df_missing_spend.loc[df_missing_spend['Vendor'] != '# NO VENDOR']
    if df_missing_spend.shape[0] > 0:
        # print "before the fix" and give the total spend in df
        logging.debug("Before the fix, the total spend is: " + str(df['ALLOCATED_AMOUNT'].sum()))
        logging.debug("There are rows where spend is missing:")
        logging.debug(df_missing_spend.head(10).to_string())
        # print the count of unique BUs for each Vendor and EXPENSE_BUCKET_2 where AMOUNT is not null and the AMOUNT is not 0
        logging.debug("The count of unique BUs for each Vendor and EXPENSE_BUCKET_2 where AMOUNT is not null and the AMOUNT is not 0:")
        logging.debug(df_missing_spend.groupby(['Vendor', 'EXPENSE_BUCKET_2'])['BU'].nunique().to_string())
        # divide 1 by the count of unique BUs for each Vendor and EXPENSE_BUCKET_2 where AMOUNT is not null and the AMOUNT is not 0
        # and use that as the ALLOCATION
        df_missing_spend['ALLOCATION'] = 1 / df_missing_spend.groupby(['Vendor', 'EXPENSE_BUCKET_2'])['BU'].transform('nunique')
        # recalculate the ALLOCATED_AMOUNT
        df_missing_spend['ALLOCATED_AMOUNT'] = df_missing_spend['AMOUNT'] * df_missing_spend['ALLOCATION']
        # replace the ALLOCATION and ALLOCATED_AMOUNT in the original df
        df.loc[df_missing_spend.index, 'ALLOCATION'] = df_missing_spend['ALLOCATION']
        df.loc[df_missing_spend.index, 'ALLOCATED_AMOUNT'] = df_missing_spend['ALLOCATED_AMOUNT']
        # print "after the fix" and give the total spend in df
        logging.debug("After the fix, the total spend is: " + str(df['ALLOCATED_AMOUNT'].sum()))
        
    else:
        logging.debug("There are no rows with missing spend")
    # remove rows where the ALLOCATED_AMOUNT is null or 0
    df = df.loc[~df['ALLOCATED_AMOUNT'].isnull()]
    df = df.loc[df['ALLOCATED_AMOUNT'] != 0]
    # are there any rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 0?
    # print the BU, Vendor, EXPENSE_BUCKET_2, ALLO_TYPE, ALLOCATION, ALLOCATION_KEY, and ALLOCATED_AMOUNT for the first 15 rows
    if df.loc[(df['ALLO_TYPE']=='SHARED SERVICES') & (df['ALLOCATION']==0)].shape[0] > 0:
        logging.debug("The first 15 rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 0:")
        logging.debug(df.loc[(df['ALLO_TYPE']=='SHARED SERVICES') & (df['ALLOCATION']==0)].head(10))
    else:
        logging.debug("There are no rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 0")
        # are there any rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 1?
        # print the BU, Vendor, EXPENSE_BUCKET_2, ALLO_TYPE, ALLOCATION, ALLOCATION_KEY, and ALLOCATED_AMOUNT for the first 15 rows
        if df.loc[(df['ALLO_TYPE']=='SHARED SERVICES') & (df['ALLOCATION']==1)].shape[0] > 0:
            logging.debug("The first 15 rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 1:")
            logging.debug(df.loc[(df['ALLO_TYPE']=='SHARED SERVICES') & (df['ALLOCATION']==1)].head(15))
        else:
            logging.debug("There are no rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 1")
        # print the sum of ALLOCATED_AMOUNT for each EXPENSE_BUCKET_2
        logging.debug("The sum of ALLOCATED_AMOUNT for each EXPENSE_BUCKET_2:")
        logging.debug(df.groupby('EXPENSE_BUCKET_2')['ALLOCATED_AMOUNT'].sum().to_string())
    # print the head of df
    logging.debug("The values after allocating")
    # if the EXPENSE_BUCKET_2 has one unique value and that value is "FTE AND "
    if df.loc[(df['PROJ_ACT']=='PROJECTION') & (df['EXPENSE_BUCKET_2']=='FTE_AND_OPEN_ROLES')].shape[0] > 0:
        df_sum_2 = df.groupby(['EXPENSE_BUCKET_2', 'Function', 'YEAR'])['ALLOCATED_AMOUNT'].sum().reset_index()
        # rename the columns
        df_sum_2.rename(columns={'Function': 'Vendor'}, inplace=True)
    else:
        df_sum_2 = df.groupby(['EXPENSE_BUCKET_2', 'Vendor', 'YEAR'])['ALLOCATED_AMOUNT'].sum().reset_index()
    # get sum of AMOUNT for each EXPENSE_BUCKET_2 and Vendor and join to df_sum from earlier
    try:
        # merge df_sum_2 with df_sum
        df_sum = pd.merge(df_sum, df_sum_2, how='outer', on=['EXPENSE_BUCKET_2', 'YEAR', 'Vendor'])
        df_sum['ALLOCATED_AMOUNT'] = df_sum['ALLOCATED_AMOUNT'].fillna(0)
        df_sum['ALLOCATED_AMOUNT'] = df_sum['ALLOCATED_AMOUNT'].astype(float)
        df_sum['AMOUNT'] = df_sum['AMOUNT'].astype(float)
        df_sum['DIFFERENCE'] = df_sum['AMOUNT'] - df_sum['ALLOCATED_AMOUNT']
        df_sum['PERCENT_DIFFERENCE'] = df_sum['DIFFERENCE'] / df_sum['AMOUNT']
        df_sum['PERCENT_DIFFERENCE'] = df_sum['PERCENT_DIFFERENCE'].fillna(0)
        # remove the % sign from the PERCENT_DIFFERENCE column
        df_sum['PERCENT_DIFFERENCE'] = df_sum['PERCENT_DIFFERENCE'].astype(float)
        df_sum['PERCENT_DIFFERENCE'] = df_sum['PERCENT_DIFFERENCE'] * 100
        df_sum['PERCENT_DIFFERENCE'] = df_sum['PERCENT_DIFFERENCE'].apply(lambda x: round(x, 4))
        df_sum['PERCENT_DIFFERENCE'] = df_sum['PERCENT_DIFFERENCE'].apply(lambda x: str(x) + '%')
        # filter for rows where the absolute value of PERCENT_DIFFERENCE is greater than .1
        df_sum = df_sum.loc[abs(df_sum['DIFFERENCE'].astype(float)) > 1]
        # sort by the PERCENT_DIFFERENCE column
        df_sum = df_sum.sort_values(by='PERCENT_DIFFERENCE', ascending=False)
    
    except Exception as e:
        logging.debug(e)
        logging.debug("There was an error merging df_sum and df.groupby(['EXPENSE_BUCKET_2', 'Vendor'])['ALLOCATED_AMOUNT'].sum().reset_index()")
        logging.debug("df_sum:")
        logging.debug(df_sum.head(15).to_string())
        logging.debug("df.groupby(['EXPENSE_BUCKET_2', 'Vendor'])['ALLOCATED_AMOUNT'].sum().reset_index():")
        logging.debug(df.groupby(['EXPENSE_BUCKET_2', 'Vendor'])['ALLOCATED_AMOUNT'].sum().reset_index().head(10))
    # if there are any rows in df_sum
    if df_sum.shape[0] > 0:
        # print the first 15 rows of df_sum
        logging.debug("The first 15 rows where pre-allocation and post-allocation don't match:")
        logging.debug(df_sum.head(10).to_string())
    else:
        logging.info("Pre-allocation and post-allocation match for all rows.")
    # filter for rows where the ALLO_TYPE is SHARED SERVICES
    df_checking = df.loc[df['ALLO_TYPE']=='SHARED SERVICES']
    # what is the sum of ALLOCATED_AMOUNT for each Vendor, BU, Quarter, Year, and EXPENSE_BUCKET_2?
    logging.debug("The sum of ALLOCATION for each Vendor, BU, Quarter, Year, and EXPENSE_BUCKET_2:")
    df_allo_total = df_checking.groupby(['Vendor', 'QUARTER', 'YEAR', 'EXPENSE_BUCKET_2'])['ALLOCATION'].sum()
    logging.debug("The number of rows for each Vendor, Quarter, Year, and EXPENSE_BUCKET_2:")
    df_rows_total = df_checking.groupby(['Vendor', 'QUARTER', 'YEAR', 'EXPENSE_BUCKET_2']).size()
    # how many unique BU values are there for each Vendor, Quarter, Year, and EXPENSE_BUCKET_2?
    df_bu_total = df_checking.groupby(['Vendor', 'QUARTER', 'YEAR', 'EXPENSE_BUCKET_2'])['BU'].nunique()
    df_allo_check = df_allo_total / df_rows_total
    df_allo_check = df_allo_check.reset_index()
    df_allo_check = df_allo_check.merge(df_bu_total, how='left', left_on=['Vendor', 'QUARTER', 'YEAR', 'EXPENSE_BUCKET_2'], right_on=['Vendor', 'QUARTER', 'YEAR', 'EXPENSE_BUCKET_2'])
    df_allo_check = df_allo_check.rename(columns={'BU': 'BU_COUNT'})
    df_allo_check = df_allo_check.loc[df_allo_check['BU_COUNT']!=2]
    
    # what is the sum of ALLOCATED_AMOUNT for each Vendor, BU, Quarter, Year, and EXPENSE_BUCKET_2 divided by the number of rows for each Vendor, Quarter, Year, and EXPENSE_BUCKET_2?
    logging.debug("The sum of ALLOCATION for each Vendor, BU, Quarter, Year, and EXPENSE_BUCKET_2 divided by the number of rows for each Vendor, Quarter, Year, and EXPENSE_BUCKET_2:")
    logging.debug(df_allo_check.head(25).to_string())
    return df
def format_final_df(df, ACTUAL_FILE_DATE):
    df['ALLOCATED_AMOUNT'] = df['AMOUNT'] * df['ALLOCATION']
    df['DATE'] = df['YEAR'].astype(str) + "-" + df['MONTH']
    df['DATE'] = pd.to_datetime(df['DATE'])
    #Postprocessing.py
    # set currrent
    df['CURRENT'] = np.where(
        (((df['MONTH'].astype(int) > int(ACTUAL_FILE_DATE))\
            & (df['PROJ_ACT'] == "PROJECTION")\
            & (df['YEAR'] == CURR_YEAR))\
        | ((df['MONTH'].astype(int) <= int(ACTUAL_FILE_DATE))\
            & (df['PROJ_ACT'] == "ACTUAL")\
            & (df['YEAR'] == CURR_YEAR))\
        | (df['PROJ_ACT'] == "ACTUAL")\
            & (df['YEAR'] < CURR_YEAR)),\
        '1', '0'
    )
    MONTH_DICT = {
        "01": "Jan",	"02": "Feb",	"03": "Mar",
        "04": "Apr",	"05": "May",	"06": "Jun",
        "07": "Jul",	"08": "Aug",	"09": "Sep",
        "10": "Oct",	"11": "Nov",	"12": "Dec"
    }
    # Small formatting changes
    df['MONTH_NAME'] = df['MONTH'].replace(MONTH_DICT)
    df['BU'] = df['BU'].str.upper()
    df['Engineering'] = df['Engineering'].str.upper()
    df['Vendor'] = df['Vendor'].str.upper()
    df['Function'] = df['Function'].str.upper()
    df['Type'] = df['Type'].str.upper()
    df['Project'] = df['Project'].str.upper()
    df['EXPENSE_BUCKET'] = df['EXPENSE_BUCKET'].str.replace("_"," ")
    df['EXPENSE_BUCKET_2'] = df['EXPENSE_BUCKET_2'].str.replace("_"," ")
    df = df.loc[(df['BU']!='CARE : 2800 PATIENTS CHOICE') & (df['BU']!='DIRECT : 1600 SANO')]
    df['ACTUAL_FILE_DATE'] = ACTUAL_FILE_DATE
    try:
        df.loc[(df['CASH_VIEW'].isnull()) & (df['PROJ_ACT']=='PROJECTION'), 'CASH_VIEW'] = "# NO CASH VIEW (PROJECTION)"
    except:
        print("Unable to set CASH_VIEW for projections, possibly no CASH_VIEW column in the data frame")
        # if there is no CASH_VIEW column, then add it
        # for Projections, set the CASH_VIEW to "# NO CASH VIEW (PROJECTION)"
        # for Actuals, set the CASH_VIEW to "# NO CASH VIEW (ACTUAL)"
        df['CASH_VIEW'] = np.where(
            (df['PROJ_ACT'] == "PROJECTION"), "# NO CASH VIEW (PROJECTION)", "ACCRUAL"
        )
    # remove any rows where the absolute value of ALLOCATED_AMOUNT is less than one and print the number of rows removed
    num_rows_removed = df.loc[abs(df['ALLOCATED_AMOUNT']) < 1].shape[0]
    df = df.loc[abs(df['ALLOCATED_AMOUNT']) >= 1]
    logging.debug("Removed " + str(num_rows_removed) + " rows where the absolute value of ALLOCATED_AMOUNT was less than one")
    return df
def validation_complete(val_dict, df):
    FTE_SUM_C0 = val_dict['FTE']['SPEND']
    OPEN_ROLES_SUM_C0 = val_dict['ORM']['SPEND']
    FTC_SUM_C0 = val_dict['FTC']['SPEND']
    PRO_SERV_SUM_C0 = val_dict['PRO_SERV']['SPEND']
    SOFTWARE_SUM_C0 = val_dict['SOFTWARE']['SPEND']
    ACTUALS_SUM_C0 = val_dict['ACTUALS']['SPEND']
    ACTUALS_SUM_DETAIL_C0 = val_dict['ACTUALS']['SPEND_DETAIL']
    FTE_SUM_C2 = df[(df['EXPENSE_BUCKET'] == 'FTE') & (df['PROJ_ACT'] == 'PROJECTION')]['ALLOCATED_AMOUNT'].sum()
    PRO_SERV_SUM_C2 = df[(df['EXPENSE_BUCKET'] == 'PRO SERV') & (df['PROJ_ACT'] == 'PROJECTION')]['ALLOCATED_AMOUNT'].sum()
    SOFTWARE_SUM_C2 = df[(df['EXPENSE_BUCKET'] == 'SOFTWARE') & (df['PROJ_ACT'] == 'PROJECTION')]['ALLOCATED_AMOUNT'].sum()
    FTC_SUM_C2 = df[(df['EXPENSE_BUCKET'] == 'FTC') & (df['PROJ_ACT'] == 'PROJECTION')]['ALLOCATED_AMOUNT'].sum()
    OPEN_ROLES_SUM_C2 = df[(df['EXPENSE_BUCKET'] == 'OPEN ROLES') & (df['PROJ_ACT'] == 'PROJECTION')]['ALLOCATED_AMOUNT'].sum()
    ACTUALS_SUM_C2 = df[(df['PROJ_ACT'] == 'ACTUAL')]['ALLOCATED_AMOUNT'].sum()
    # filter df for PROJ_ACT = ACTUAL
    # group by EXPENSE_BUCKET, MONTH, and YEAR
    # sum the ALLOCATED_AMOUNT
    # join the ALLOCATED_AMOUNT to the ACTUALS_SUM_DETAIL_C0
    # on EXPENSE_BUCKET, MONTH, and YEAR
    # calculate the difference between the ACTUALS_SUM_DETAIL_C0 and the ACTUALS_SUM_DETAIL_C2
    # print the result
    ACTUALS_SUM_DETAIL_C2 = df[(df['PROJ_ACT'] == 'ACTUAL')].groupby(['EXPENSE_BUCKET', 'MONTH', 'YEAR'])['ALLOCATED_AMOUNT'].sum().reset_index()
    # rename the ALLOCATED_AMOUNT column to ALLOCATED_AMOUNT column to VAL_ACTUAL and the EXPENSE_BUCKET column to VAL_MODEL
    ACTUALS_SUM_DETAIL_C2 = ACTUALS_SUM_DETAIL_C2.rename(columns={'ALLOCATED_AMOUNT': 'VAL_ACTUAL', 'EXPENSE_BUCKET': 'VAL_MODEL'})
    # join the ACTUALS_SUM_DETAIL_C2 to the ACTUALS_SUM_DETAIL_C0
    logging.debug(ACTUALS_SUM_DETAIL_C2.to_string())
    logging.debug("type: " + str(type(ACTUALS_SUM_DETAIL_C2)))
    logging.debug(ACTUALS_SUM_DETAIL_C0.to_string())
    logging.debug("type: " + str(type(ACTUALS_SUM_DETAIL_C0)))
    # add a leading zero to the MONTH column in ACTUALS_SUM_DETAIL_C0
    ACTUALS_SUM_DETAIL_C0['MONTH'] = ACTUALS_SUM_DETAIL_C0['MONTH'].apply(lambda x: '{0:0>2}'.format(x))
    # join the ACTUALS_SUM_DETAIL_C2 to the ACTUALS_SUM_DETAIL_C0
    ACTUALS_SUM_DETAIL_C2 = pd.merge(ACTUALS_SUM_DETAIL_C0, ACTUALS_SUM_DETAIL_C2, how='left', on=['VAL_MODEL', 'MONTH', 'YEAR'])
    # calculate the difference between the VAL_ACTUAL and VAL_EXPECTED
    logging.debug(ACTUALS_SUM_DETAIL_C2.to_string())
    c2_fte_valid = validate(FTE_SUM_C0, FTE_SUM_C2)
    c2_pro_serv_valid = validate(PRO_SERV_SUM_C0, PRO_SERV_SUM_C2)
    c2_software_valid = validate(SOFTWARE_SUM_C0, SOFTWARE_SUM_C2)
    c2_ftc_valid = validate(FTC_SUM_C0, FTC_SUM_C2)
    c2_open_roles_valid = validate(OPEN_ROLES_SUM_C0, OPEN_ROLES_SUM_C2)
    c2_actuals_valid = validate(ACTUALS_SUM_C0, ACTUALS_SUM_C2)
    # Create a data frame with the results of the data validation
    # Where the data frame has 6 rows and 5 columns, with the following column names:
    # VAL_CHECKPOINT, VAL_MODEL, VAL_ACTUAL, VAL_EXPECTED, VAL_VALID
    df_data_validation = pd.DataFrame(
        {
            'VAL_CHECKPOINT': ['MAIN', 'MAIN', 'MAIN', 'MAIN', 'MAIN', 'MAIN'], 
            'VAL_MODEL': ['FTE', 'PRO SERV', 'SOFTWARE', 'FTC', 'OPEN ROLES', 'ACTUALS'],
            'VAL_ACTUAL': [FTE_SUM_C2, PRO_SERV_SUM_C2, SOFTWARE_SUM_C2, FTC_SUM_C2, OPEN_ROLES_SUM_C2, ACTUALS_SUM_C2],
            'VAL_EXPECTED': [FTE_SUM_C0, PRO_SERV_SUM_C0, SOFTWARE_SUM_C0, FTC_SUM_C0, OPEN_ROLES_SUM_C0, ACTUALS_SUM_C0],
            'VAL_VALID': [c2_fte_valid, c2_pro_serv_valid, c2_software_valid, c2_ftc_valid, c2_open_roles_valid, c2_actuals_valid]
        }
    )
    return df_data_validation
def clean_fte_for_hc(df):
    # function that cleans the FTE data for HC (doesn't run the format_projections functions)
    df = clean_data(df)
    df["Vendor"] = "# NO VENDOR"
    df["Project"] = "# NO PROJECT"
    df['Engineering'].fillna('NOT ENGINEERING', inplace=True)
    df['EXPENSE_BUCKET'] = 'FTE'
    df = df.loc[(df['BU'] != '') & (df['BU'].notnull())]
    return df
def clean_orm_for_hc(df):
    # function that cleans the ORM data for HC (doesn't run the format_projections functions)
    # filter for HC = 1
    df = df.loc[df['HC'] == 1]
    # function that cleans the ORM data
    df = clean_data(df)
    df.rename(columns={
            'BU-FUNCTION KEY'       : 'BU-Function Key',
            'Start Date'            : 'Company Seniority Date',
            'Monthly Fully-Loaded'  : 'PnL Monthly'
        }, inplace=True)
    df.columns = df.columns.str.replace("Fully-Loaded", "PnL")
    df["Vendor"]            = "# NO VENDOR"
    df["Project"]           = "# NO PROJECT"
    df['EXPENSE_BUCKET']    = "OPEN_ROLES"
    
    # if the BONUS_COLS are not in the df, add them and fill with 0
    for col in BONUS_COLS:
        if col not in df.columns:
            df[col] = 0
    df['Engineering'].fillna('NOT ENGINEERING', inplace=True)
    df = df.loc[(df['BU'] != '') & (df['BU'].notnull())]
    return df
def clean_headcounts(df):
    df = df.copy(deep=True)
    df['EXPENSE_BUCKET_2'] = "FTE_AND_OPEN_ROLES"
    df = df[ALL_HC_PROJ_COLS]
    df.loc[df['Termination Date'].isnull(), 'Termination Date'] = pd.Timestamp("01-01-2200")
    df.loc[df['Company Seniority Date'].isnull(), 'Company Seniority Date'] = pd.Timestamp("01-01-2200")
    df['Join_Month'] = pd.to_datetime(df["Company Seniority Date"], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m'))
    df['Depart_Month'] = pd.to_datetime(df["Termination Date"], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m'))
    # convert company seniority date to datetime
    df['Company Seniority Date'] = pd.to_datetime(df['Company Seniority Date'], format='%Y-%m-%d')
    # convert termination date to datetime
    df['Termination Date'] = pd.to_datetime(df['Termination Date'], format='%Y-%m-%d')
    def compare_months(row, month):
        date_val = CURR_YEAR_STR + month + "01"
        date_val = pd.to_datetime(date_val)
        # go forward one month
        date_val = date_val + relativedelta(months=1)
        # go back one day to get last day of previous (ie current) month
        date_val = date_val - timedelta(days=1)
        return int((row['Company Seniority Date'] <= date_val) & ((row['Termination Date'] > date_val) | pd.isnull(row['Termination Date'])))
    for key in MONTH_DICT.keys():
        df[key+"|HC"] = df.apply(lambda row: compare_months(row, key), axis=1)
    def compare_join_months(row, month):
        date_val = CURR_YEAR_STR + "-" + month
        return int((row['Join_Month'] == date_val))
    for key in MONTH_DICT.keys():
        df[key+"|HC_JOIN"] = df.apply(lambda row: compare_join_months(row, key), axis=1)
    def compare_departure_months(row, month):
        date_val = CURR_YEAR_STR + "-" + month
        return int((row['Depart_Month'] == date_val))
    for key in MONTH_DICT.keys():
        df[key+"|HC_DEPART"] = df.apply(lambda row: compare_departure_months(row, key), axis=1)
    df = pd.melt(
        df,
        id_vars=HC_FTE_COLS,
        value_vars=SPEND_COLS_W_BONUS_AND_HC,
        var_name='MONTH',
        value_name='AMOUNT'
    )
    df['MONTH'].replace(HC_DICT_W_BONUS, inplace=True)
    df[['MONTH', 'CATEGORY']] = df['MONTH'].str.split("|", expand=True)
    df['YEAR'] = CURR_YEAR
    MONTH_TO_QUART = {
        "01":1,"02":1,"03":1,
        "04":2,"05":2,"06":2,
        "07":3,"08":3,"09":3,
        "10":4,"11":4,"12":4,
                    }
    
    df['QUARTER'] = df['MONTH'].replace(MONTH_TO_QUART)
    df['PROJ_ACT'] = "PROJECTION"
    return df
def format_headcounts(df):
    df = df.copy(deep=True)
    # print the number of rows where MONTH is 99
    logging.debug("Number of rows where MONTH is 99: " + str(len(df.loc[df['MONTH']=="99"])))
    df['ALLOCATED_AMOUNT'] = df['AMOUNT'] * df['ALLOCATION']
    # store the number of rows in the df
    df_len = len(df)
    df = df.loc[(df['ALLOCATED_AMOUNT']!=0) | (df['MONTH']=="99")]
    # if the number of rows in the df has changed, print a message
    if df_len != len(df):
        logging.debug("Removed rows with 0 allocated amount")
        logging.debug(str(df_len - len(df)) + " rows removed")
        # print rows remaining
        logging.debug(str(len(df)) + " rows remaining")
    df['BU'] = df['BU'].str.upper()
    df['Engineering'] = df['Engineering'].str.upper()
    df['Function'] = df['Function'].str.upper()
    df['EXPENSE_BUCKET'] = df['EXPENSE_BUCKET'].str.replace("_"," ")
    df['EXPENSE_BUCKET_2'] = df['EXPENSE_BUCKET_2'].str.replace("_"," ")
    df['MONTH_NAME'] = df['MONTH'].replace(MONTH_DICT)
    # Get today's month
    CURR_MONTH = datetime.datetime.now().strftime("%m")
    df['CURRENT'] = np.where(df['MONTH'] <= CURR_MONTH, 1, 0)
    # Get the last day of the current month as a datetime object
    CURR_MONTH_LAST_DAY = datetime.datetime.now().replace(day=calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1])
    # Add a PnL YtD Join columm where the CATEGORY is PNL MONTHLY and the Company Seniority Date is less than or equal to the last day of the current month and
    # the Termination Date is greater than or equal to the last day of the current month
    df['PnL_YTD_JOIN'] = np.where(
        (df['CATEGORY'] == 'PNL MONTHLY') &
        (df['Company Seniority Date'] <= CURR_MONTH_LAST_DAY) &
        (df['Company Seniority Date'].dt.year == CURR_YEAR) &
        (df['Termination Date'] >= CURR_MONTH_LAST_DAY) &
        (df['YEAR'] == CURR_YEAR),
        1, 0)
    # Add a PnL YtD Depart columm where the CATEGORY is PNL MONTHLY and the Termination Date is less than or equal to the last day of the current month
    df['PnL_YTD_DEPART'] = np.where(
        (df['CATEGORY'] == 'PNL MONTHLY') &
        (df['Termination Date'] <= CURR_MONTH_LAST_DAY) &
        (df['Termination Date'].dt.year == CURR_YEAR),
        1, 0)
    # add a YEAR column
    df['YEAR'] = CURR_YEAR
    return df
def calculate_headcount(df_fte, df_orm, df_fte_allocation, df_name_map):
    
    #Processing.py
    df_orm.rename(columns={
        'BU-FUNCTION KEY': 'BU-Function Key',
        'Start Date': 'Company Seniority Date',
        'Monthly Fully-Loaded':'PnL Monthly'},
                inplace=True)
    df_orm.columns = df_orm.columns.str.replace("Fully-Loaded", "PnL")
    # Add contants
    df_fte['Engineering'].fillna('NOT ENGINEERING', inplace=True)
    df_orm['Engineering'].fillna('NOT ENGINEERING', inplace=True)
    df_fte = clean_fte_for_hc(df_fte)
    df_orm = clean_orm_for_hc(df_orm)
    # Filter empty rows
    df_fte = df_fte.loc[(df_fte['BU'] != '') & (df_fte['BU'].notnull())]
    df_orm = df_orm.loc[(df_orm['BU'] != '') & (df_orm['BU'].notnull())]
    # df_orm = df_orm.loc[(df_orm['HC'] == 1)]
    df_orm['EXPENSE_BUCKET'] = 'OPEN_ROLES'
    df_fte['EXPENSE_BUCKET'] = 'FTE'
    df_fte_allocation['SOURCE'] = 'FTE_AND_OPEN_ROLES'
    df_fte_allocation['BU-Function Key'] = df_fte_allocation['BU-Function Key'] + "-na"
    df_fte_allocation = clean_allocation_sheet(df_fte_allocation, df_name_map)
    df = pd.concat((df_fte, df_orm))
    df = clean_headcounts(df)
    # split the df into two dfs, one with the FTE and one with the ORM
    df_fte = df.loc[df['EXPENSE_BUCKET'] == 'FTE']
    df_open_roles = df.loc[df['EXPENSE_BUCKET'] == 'OPEN_ROLES']
    df_fte = join_allocation_to_df(df_fte, df_fte_allocation)
    df_open_roles = join_allocation_to_df(df_open_roles, df_fte_allocation)
    df = pd.concat((df_fte, df_open_roles))
    df_final = format_headcounts(df)
    return df_final
def clean_software_for_deltas(df):
    # function that cleans the Software data
    df = clean_data(df)
    df.rename(columns={'Owner': 'Contact'}, inplace=True)
    df["Project"] = "# NO PROJECT"
    df['Engineering'] = "NOT ENGINEERING"
    df['EXPENSE_BUCKET'] = 'SOFTWARE'
    df[BONUS_COLS] = 0
    # df = clean_projections(df)
    df = df[ALL_PROJ_COLS]
    df = df.groupby([
            'Vendor',
            'BU',
            'IS Grouping',
            'Engineering',
            'Function',
            'Project',
            'Contact',
            'EXPENSE_BUCKET'
            ], dropna=False)[SPEND_COLS_W_BONUS].sum()
    df.reset_index(inplace=True)
    return df
def clean_ftc_for_deltas(df):
    # function that cleans the Software data
    df = clean_data(df)
    df.rename(columns={'Owner': 'Contact'}, inplace=True)
    df["Project"].fillna("# NO PROJECT", inplace=True)
    df['Engineering'] = "NOT ENGINEERING"
    df['EXPENSE_BUCKET'] = 'FTC'
    df[BONUS_COLS] = 0
    # df = clean_projections(df)
    df = df[ALL_PROJ_COLS]
    df = df.groupby([
            'Vendor',
            'BU',
            'IS Grouping',
            'Engineering',
            'Function',
            'Project',
            'Contact',
            'EXPENSE_BUCKET'
            ], dropna=False)[SPEND_COLS_W_BONUS].sum()
    df.reset_index(inplace=True)
    return df
def clean_pro_serv_for_deltas(df):
    # function that cleans the Software data
    df = clean_data(df)
    df.rename(columns={'Owner': 'Contact'}, inplace=True)
    df["Project"] = "# NO PROJECT"
    df['Engineering'] = "NOT ENGINEERING"
    df['EXPENSE_BUCKET'] = 'PRO_SERV'
    df[BONUS_COLS] = 0
    # df = clean_projections(df)
    df = df[ALL_PROJ_COLS]
    df = df.groupby([
            'Vendor',
            'BU',
            'IS Grouping',
            'Engineering',
            'Function',
            'Project',
            'Contact',
            'EXPENSE_BUCKET'
            ], dropna=False)[SPEND_COLS_W_BONUS].sum()
    df.reset_index(inplace=True)
    return df
def clean_fte_for_deltas(df):
    # function that cleans the Software data
    df = clean_data(df)
    df.rename(columns={'Supervisor Name': 'Contact'}, inplace=True)
    df["Project"] = "# NO PROJECT"
    df["Vendor"] = "# NO VENDOR"
    df['Engineering'].fillna("NOT ENGINEERING")
    df['EXPENSE_BUCKET'] = 'FTE'
    df[BONUS_COLS].fillna(0)
    # df = clean_projections(df)
    df = df[ALL_PROJ_COLS]
    df = df.groupby([
            'Vendor',
            'BU',
            'IS Grouping',
            'Engineering',
            'Function',
            'Project',
            'Contact',
            'EXPENSE_BUCKET'
            ], dropna=False)[SPEND_COLS_W_BONUS].sum()
    df.reset_index(inplace=True)
    return df
def calculate_deltas(df_fte, df_ftc, df_pro_serv, df_software, df_actuals, ACTUAL_FILE_DATE, df_name_map):
    models = [df_software, df_ftc, df_pro_serv, df_fte]
    df_actuals = clean_actuals(df_actuals, ACTUAL_FILE_DATE, df_name_map)
    df_actuals = df_actuals.loc[
        (df_actuals['EXPENSE_BUCKET'] == "SOFTWARE") | 
        (df_actuals['EXPENSE_BUCKET'] == "FTC") |
        (df_actuals['EXPENSE_BUCKET'] == "PRO_SERV") |
        (df_actuals['EXPENSE_BUCKET'] == "FTE")
    ]
    df_software['Paid by Credit Card (Y/N)'].fillna('N', inplace=True)
    df_software_paid_by_cc = df_software.loc[df_software['Paid by Credit Card (Y/N)'] == "Y"]
    df_software_paid_by_cc = df_software_paid_by_cc[['Vendor', 'Paid by Credit Card (Y/N)']]
    df_software_paid_by_cc = df_software_paid_by_cc.drop_duplicates()
    df_software_paid_by_cc = df_software_paid_by_cc.rename(columns={"Paid by Credit Card (Y/N)": "PAID_BY_CC"})
    df_software_paid_by_cc['PAID_BY_CC'] = 1
    
    # this will convert Inc to Inc. 
    df_software_paid_by_cc = clean_data(df_software_paid_by_cc)
    # convert the vendor names to upper case
    df_software_paid_by_cc['Vendor'] = df_software_paid_by_cc['Vendor'].str.upper()
    df_software = clean_software_for_deltas(df_software)
    df_ftc = clean_ftc_for_deltas(df_ftc)
    df_pro_serv = clean_pro_serv_for_deltas(df_pro_serv)
    df_fte = clean_fte_for_deltas(df_fte)
    
    df = pd.concat([df_ftc, df_software, df_pro_serv, df_fte], ignore_index=True)
    df_formatted_projections = pd.melt(
        df,
        id_vars=[
        'Vendor',
        'BU',
        'IS Grouping',
        'Engineering',
        'Function',
        'Project',
        'Contact',
        'EXPENSE_BUCKET'
        ],
        value_vars=SPEND_COLS_W_BONUS,
        var_name='MONTH',
        value_name='AMOUNT'
        )
    
    df_formatted_projections['MONTH'] = df_formatted_projections['MONTH'].replace(DICT_W_BONUS)
    df_formatted_projections[['MONTH','SAL_BONUS']] = df_formatted_projections['MONTH'].str.split("|", expand=True)
    # Again, setting year back TEMPORARILY
    df_formatted_projections['YEAR'] = CURR_YEAR
    df_formatted_projections['Type'] = "# NO TYPE"
    df_formatted_projections = df_formatted_projections.loc[(df_formatted_projections['AMOUNT'] != 0) & (df_formatted_projections['AMOUNT'].notnull())]
    df_formatted_projections['PROJ_ACT'] = 'PROJECTION'
    df_formatted_projections['QUARTER'] = pd.to_datetime(df_formatted_projections['MONTH'].values, format='%m').astype('period[Q]').astype(str).str[-1:]
    # Filter actuals columns
    df_formatted_actuals = df_actuals[['Vendor', 'BU', 'IS Grouping', 'Engineering', 'Function', 'Project', 'Contact', 'PROJ_ACT', 'MONTH', 'AMOUNT', 'QUARTER', 'YEAR', 'Type', 'CASH_VIEW', 'EXPENSE_BUCKET', 'SAL_BONUS']]
    df_formatted_actuals = df_formatted_actuals.groupby(['Vendor', 'BU', 'IS Grouping', 'Engineering', 'Function', 'Project', 'Contact', 'PROJ_ACT', 'MONTH', 'QUARTER', 'YEAR', 'Type', 'CASH_VIEW', 'EXPENSE_BUCKET', 'SAL_BONUS']).sum()
    df_formatted_actuals.reset_index(inplace=True)
    df = pd.concat((df_formatted_projections, df_formatted_actuals), ignore_index=True)
    df['EXPENSE_BUCKET_2'] = df['EXPENSE_BUCKET']
    df['ALLOCATION'] = 1
    df = format_final_df(df, ACTUAL_FILE_DATE)
    # convert ACTUAL_FILE_DATE to int
    ACTUAL_FILE_DATE = int(ACTUAL_FILE_DATE)
    # TEMPORARILY changed CURR_YEAR to CURR_YEAR - 1
    df = df.loc[(df['YEAR']==CURR_YEAR) & (df['MONTH'].astype(int) <= ACTUAL_FILE_DATE)]
    df['Vendor'].fillna("# NO VENDOR", inplace=True)
    df['SAL_BONUS'].fillna("-", inplace=True)
    df_pivot = df.pivot_table(index=['YEAR', 'QUARTER', 'MONTH_NAME','MONTH','Vendor', 'BU', 'Function', 'IS Grouping','EXPENSE_BUCKET'], values='ALLOCATED_AMOUNT', columns='PROJ_ACT', aggfunc='sum')
    df_pivot.reset_index(inplace=True)
    df_sum = df_pivot.groupby(['YEAR','Vendor','EXPENSE_BUCKET'], as_index=False).sum()
    df_sum['MONTH_NAME']='ALL'
    df_sum['MONTH']="999"
    df_top_5 = df_sum.loc[(df_sum['Vendor']!="# NO VENDOR")].sort_values(by=['ACTUAL'], ascending=False).head(5)
    TOP_5_ARRAY = df_top_5["Vendor"].values
    # convert the array to a string, then remove the brackets and single quotes
    TOP_5_ARRAY_STR = str(TOP_5_ARRAY).replace("[", "").replace("]", "").replace("'", "")
    logging.debug("here is the top 5 array as a string: " + TOP_5_ARRAY_STR)
    df = df_sum.append(df_pivot)
    df["TOP_5"] = 0
    for V in TOP_5_ARRAY:
        df["TOP_5"] = np.where(df['Vendor']==V, 1, df["TOP_5"])
    df.fillna({'PROJECTION':0, 'ACTUAL':0, 'QUARTER':"ALL"}, inplace=True)
    df['DELTA_(P-A)'] = df['PROJECTION'] - df['ACTUAL']
    # here are all the vendors that are missing from the projection
    # use df_sum and find all the vendors that have ACTUAL > 0 and PROJECTION = 0
    # then use that list to find all the rows in df where the vendor is in that list
    # then set the MISSING_FROM_PROJ column to 1
    try:
        df['MISSING_FROM_PROJ'] = np.where(((df['ACTUAL']>0) & (df['PROJECTION']==0)), 1, 0)
    except:
        df['MISSING_FROM_PROJ'] = 0
    MISSING_FROM_PROJ_ARRAY = list(set(df.loc[df['MISSING_FROM_PROJ']==1, "Vendor"].values))
    df['ALOM_MISSING_FROM_PROJ'] = np.where((df["Vendor"].isin(MISSING_FROM_PROJ_ARRAY)), 1, 0) # At least one month missing (ALOM missing)
    try:
        df['ABSENT_FROM_PROJ'] = np.where(((df['ACTUAL']>0) & (df['PROJECTION']==0) & (df['MONTH']=="999")), 1, 0)
    except:
        df['ABSENT_FROM_PROJ'] = 0
    ABSENT_FROM_PROJ_ARRAY = list(set(df.loc[df['ABSENT_FROM_PROJ']==1, "Vendor"].values))
    df['ABSENT_FROM_PROJ'] = np.where((df["Vendor"].isin(ABSENT_FROM_PROJ_ARRAY)), 1, 0)
    try:
        df['MISSING_FROM_ACT'] = np.where(((df['ACTUAL']==0) & (df['PROJECTION']>0)), 1, 0)
    except:
        df['MISSING_FROM_ACT'] = 0
    MISSING_FROM_ACT_ARRAY = list(set(df.loc[df['MISSING_FROM_ACT']==1, "Vendor"].values))
    df['ALOM_MISSING_FROM_ACT'] = np.where((df["Vendor"].isin(MISSING_FROM_ACT_ARRAY)), 1, 0)
    try:
        df['ABSENT_FROM_ACT'] = np.where(((df['ACTUAL']==0) & (df['PROJECTION']>0) & (df['MONTH']=="999")), 1, 0)
    except:
        df['ABSENT_FROM_ACT'] = 0
    ABSENT_FROM_ACT_ARRAY = list(set(df.loc[df['ABSENT_FROM_ACT']==1, "Vendor"].values))
    df['ABSENT_FROM_ACT'] = np.where((df["Vendor"].isin(ABSENT_FROM_ACT_ARRAY)), 1, 0)
    df = df.round(decimals=3)
    df['LAST_THREE_MONTHS'] = (df['MONTH'].astype(int) > (ACTUAL_FILE_DATE-3)) & (df['MONTH'].astype(int) <= (ACTUAL_FILE_DATE))
    total_delta = df.loc[(df['MONTH']!="999"), 'DELTA_(P-A)'].sum()
    try:
        total_delta_as_currency = "${:,.2f}".format(total_delta)
    except:
        logging.debug("Error -- could not format total delta:  ", total_delta)
        total_delta_as_currency = 0
    logging.debug("Compiled Annual Delta: ", total_delta_as_currency)
    df = pd.melt(df, id_vars=[
        'YEAR', 'Vendor', 'BU', 'Function', 'IS Grouping', 'EXPENSE_BUCKET',
        'MONTH_NAME', 'MONTH', 'QUARTER', 'TOP_5', 'MISSING_FROM_PROJ',
        'MISSING_FROM_ACT', 'ALOM_MISSING_FROM_ACT', 'ALOM_MISSING_FROM_PROJ',
        'ABSENT_FROM_PROJ', 'ABSENT_FROM_ACT', 'LAST_THREE_MONTHS'
        ], value_vars=['ACTUAL', 'PROJECTION', 'DELTA_(P-A)'], var_name="CATEGORY", value_name="VALUE")
    logging.debug(" ~ Calculate_Delta function complete ~ ")
    logging.debug("here are the columns of the delta dataframe: ", df.columns)
    df['MISSING_FROM_ACT'] = np.where(df['Vendor'].isin(df_software_paid_by_cc['Vendor']), 0, df['MISSING_FROM_ACT'])
    df['ALOM_MISSING_FROM_ACT'] = np.where(df['Vendor'].isin(df_software_paid_by_cc['Vendor']), 0, df['ALOM_MISSING_FROM_ACT'])
    df['ABSENT_FROM_ACT'] = np.where(df['Vendor'].isin(df_software_paid_by_cc['Vendor']), 0, df['ABSENT_FROM_ACT'])
    return df
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
    df = format_final_df(df, ACTUAL_FILE_DATE)
    df['SEGMENT'] = "MAIN"
    df_validation = validation_complete(val_dict, df)
    OUTPUT_ARRAY = [df, df_validation]
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
        all_data = [df_actuals, df_software, df_ftc, df_pro_serv, df_fte]
        df_delta = calculate_deltas(df_fte, df_ftc, df_pro_serv, df_software, df_actuals, ACTUAL_FILE_DATE, df_name_map)
        df_delta['SEGMENT'] = 'DELTA'
        OUTPUT_ARRAY.append(df_delta)
    write_data(df_validation, RUNNING_IN_DOMO)
main()