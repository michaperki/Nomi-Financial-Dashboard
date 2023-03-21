from domomagic import *
import numpy as np
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
# Output Arrays
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
            # if there are rows in df where the SOURCE is "FTE_AND_OPEN_ROLES"
            if df[df['SOURCE'] == 'FTE_AND_OPEN_ROLES'].shape[0] > 0:
                # store the sum of the ALLOCATION column in df where the SOURCE is "FTE_AND_OPEN_ROLES" in a variable
                FTE_ALLO_SUM_PRIOR = df[df['SOURCE'] == 'FTE_AND_OPEN_ROLES']['ALLOCATION'].sum()
                # for each Vendor in df_allo_total_missing, assign .5 to the
                # ALLOCATION column in df where the Vendor, Quarter, and Year is the same and the BU is
                # "CARE" or "CONNECT" and the SOURCE is "FTE_AND_OPEN_ROLES"
                # if the BU is "INSIGHTS" or "NETWORK", assign .0 to the ALLOCATION column
                for index, row in df_allo_total_missing.iterrows():
                    df.loc[(df['Vendor'] == row['Vendor']) & (df['QUARTER'] == row['QUARTER']) & (df['YEAR'] == row['YEAR']) & (df['SOURCE'] == 'FTE_AND_OPEN_ROLES') & (df['BU'].isin(['Care','Connect'])), 'ALLOCATION'] = .5
                    df.loc[(df['Vendor'] == row['Vendor']) & (df['QUARTER'] == row['QUARTER']) & (df['YEAR'] == row['YEAR']) & (df['SOURCE'] == 'FTE_AND_OPEN_ROLES') & (df['BU'].isin(['Insights','Network'])), 'ALLOCATION'] = 0   
                # store the sum of the ALLOCATION column in df where the SOURCE is "FTE_AND_OPEN_ROLES" in a variable
                FTE_ALLO_SUM_AFTER = df[df['SOURCE'] == 'FTE_AND_OPEN_ROLES']['ALLOCATION'].sum()
                logging.info("After assigning .5 to CARE/CONNECT and 0 to INSIGHTS/NETWORK, the sum of the ALLOCATION column for FTE_AND_OPEN_ROLES went from " + str(FTE_ALLO_SUM_PRIOR) + " to " + str(FTE_ALLO_SUM_AFTER))
                # check that the fix worked
                df_allo_total_by_Q = df.groupby(['QUARTER','YEAR','Vendor','SOURCE']).agg({'ALLOCATION':'sum'}).reset_index()
                df_allo_total_by_Q = df_allo_total_by_Q.loc[df_allo_total_by_Q['ALLOCATION'] != 1]
                df_allo_total_by_Q_sum = df_allo_total_by_Q.groupby(['YEAR','Vendor','SOURCE','ALLOCATION']).agg({'QUARTER':', '.join}).reset_index()
                if df_allo_total_by_Q_sum.shape[0] > 0:
                    logging.error("The fix for FTE_AND_OPEN_ROLES did not work")
                    logging.debug(df_allo_total_by_Q_sum.to_string(index=False))
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
    logging.debug("...removing", string, "from", column)
    logging.debug("...unique values in ", column, "are", list(df[column].unique()))
    df[column] = df[column].str.replace(string, '', regex=True)
    df[column].replace(r'^\s*$',np.nan,regex=True,inplace=True)
    logging.debug("...after removing, unique values in ", column, "are", list(df[column].unique()))
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
    print("...unique values in CASH_VIEW column: ", list(df['CASH_VIEW'].unique()))
    print("")
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
    print("Prepaid Vendors:", prepaid_vendor_list)
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
    df['Amount'] = df['Amount'].str.replace('(', '-')
    df['Amount'] = df['Amount'].str.replace(')', '')
    # if the Amount column has commas, then remove them
    df['Amount'] = df['Amount'].str.replace(',', '')
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
        print("...ACTUAL_FILE_DATE is not an integer")
        print("...setting ACTUAL_FILE_DATE to 0")
        ACTUAL_FILE_DATE = 0
    # format BU column
    df = remove_string_from_column(df, 'BU', '\d{4}\s+Nomi( Health Inc)?[. ]?( : \d{4} )?')
    df[['BU', 'IS Grouping']] = df[['BU', 'IS Grouping']].fillna("# BLANK")
    df['IS Grouping'] = df['IS Grouping'].replace(IS_GROUP_DICT)
    df['EXPENSE_BUCKET'] = df['Expense Bucket - Account field'].replace(EXPENSE_BUCKET_DICT)
    df['SAL_BONUS'] = np.where(df['Account'] == "6044 Bonus expense (accrual)","BONUS", "SALARY")
    # print removing future months and print the amount of spend removed as a currency.
    # this amount needs to be used in data validation
    print("...removing future months from actuals")
    # print the number of rows removed
    print("...number of rows removed: ", len(df.loc[(df['YEAR_INT']>CURR_YEAR) | ((df['MONTH_INT']>ACTUAL_FILE_DATE) & (df['YEAR_INT']==CURR_YEAR))]))
    ACTUALS_FUTURE_SPEND = df.loc[(df['YEAR_INT']>CURR_YEAR) | ((df['MONTH_INT']>ACTUAL_FILE_DATE) & (df['YEAR_INT']==CURR_YEAR))]['Amount'].sum()
    # print as a currency
    print("...amount of spend removed from actuals: ", "${:,.0f}".format(ACTUALS_FUTURE_SPEND))
    print("")
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
        setup_for_data_validation(ACTUAL_FILE_DATE, df_monthly_dict)
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
    
    write_data(df_name_map, RUNNING_IN_DOMO)
main()