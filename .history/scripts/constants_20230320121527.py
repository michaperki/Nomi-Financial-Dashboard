# START SCRIPT
import numpy as np
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

# END SCRIPT