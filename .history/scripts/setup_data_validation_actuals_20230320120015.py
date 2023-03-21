from constants import *
import logging
import pandas as pd

# START SCRIPT
def setup_data_validation_actuals(df, ACTUAL_FILE_DATE):
    # This function sets up the data validation for the ACTUALS data
    # It returns a dictionary with the information needed for the validation

    df = df.copy(deep=True)
    # if the Amount column has parentheses, then replace them with a negative sign
    df['Amount'] = df['Amount'].str.replace('(', '-')
    df['Amount'] = df['Amount'].str.replace(')', '')
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

# END SCRIPT