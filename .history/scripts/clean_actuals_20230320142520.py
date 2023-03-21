import logging
import pandas as pd

from constants import *
from clean_data import clean_data
from remove_string_from_column import remove_string_from_column
from format_cash_view import format_cash_view
from join_name_map_to_actuals import join_name_map_to_actuals
from clean_actuals_fte import clean_actuals_fte

# START SCRIPT

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
    logging.debug("...number of rows removed: ", str(len(df.loc[(df['YEAR_INT']>CURR_YEAR) | ((df['MONTH_INT']>ACTUAL_FILE_DATE) & (df['YEAR_INT']==CURR_YEAR))])))
    ACTUALS_FUTURE_SPEND = df.loc[(df['YEAR_INT']>CURR_YEAR) | ((df['MONTH_INT']>ACTUAL_FILE_DATE) & (df['YEAR_INT']==CURR_YEAR))]['Amount'].sum()
    # print as a currency
    logging.debug("...amount of spend removed from actuals: ", "${:,.0f}".format(ACTUALS_FUTURE_SPEND))
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
# END SCRIPT