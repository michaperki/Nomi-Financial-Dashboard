import logging
import pandas as pd
from constants import *

# START SCRIPT

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

    df = df.loc[(df['BU']!='CARE : 2800 PATIENTS CHOICE') & (df['BU']!='DIRECT : 1600 SANO')].copy()
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
# END SCRIPT