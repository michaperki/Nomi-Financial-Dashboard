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

    # print the sum of all SPEND_COLS formatted as a currency
    ACTUALS_SPEND = df['Amount'].sum()
    print(ACTUALS_SPEND)
    print("the total ACTUALS spend is " + "${:,.20}".format(ACTUALS_SPEND))
    print()


    # after removing the "CARE : 2800 PATIENTS CHOICE" and "DIRECT : 1600 SANO" rows
    df = df.loc[(df['BU']!='1100 Nomi Care : 2800 Patients Choice') & (df['BU']!='1050 Open Network : 1600 Sano')]
    print("after removing the 'CARE : 2800 PATIENTS CHOICE' and 'DIRECT : 1600 SANO' rows")
    ACTUALS_SPEND_NO_SANO_OR_PC = df['Amount'].sum()
    print("the total ACTUALS spend is " + "${:,.0f}".format(ACTUALS_SPEND_NO_SANO_OR_PC))
    print()  


    # print the sum of 'Amount' by YEAR using the "Date" column formatted as a currency
    # convert the "Date" column to a Year
    df['Year'] = pd.to_datetime(df['Date']).dt.year
    df['Month'] = pd.to_datetime(df['Date']).dt.month

    # ACTUALS_SPEND_EXCLUDING_FUTURE
    df = df[(df['Year'] < CURR_YEAR) | ((df['Year'] == CURR_YEAR) & (df['Month'] <= ACTUAL_FILE_DATE))]
    ACTUALS_SPEND_EXCLUDING_FUTURE = df['Amount'].sum()
    print("the total ACTUALS spend excluding future is " + "${:,.0f}".format(ACTUALS_SPEND_EXCLUDING_FUTURE))
    print()

    ACTUALS_SPEND_BY_YEAR = df.groupby('Year')['Amount'].sum()
    ACTUALS_SPEND_BY_YEAR = ACTUALS_SPEND_BY_YEAR.reset_index()    
    
    print("the ACTUALS spend by year is ")
    print(ACTUALS_SPEND_BY_YEAR.to_string())
    print()

    # filter the data for 2022
    # create a pivot table with the "Year" and "Month" as the index and the "Amount" as the values and 'Expense Bucket - Account field' as the rows
    # convert the "Amount" column to a currency
    # print the pivot table
    # filter for 2022
    ACTUALS_SPEND_BY_YEAR_MONTH = df[df['Year'] == 2022].pivot_table(index=['Expense Bucket - Account field'], values='Amount', columns=['Year', 'Month'], aggfunc='sum', fill_value=0, margins=True)
    #ACTUALS_SPEND_BY_YEAR_MONTH = ACTUALS_SPEND_BY_YEAR_MONTH.apply(lambda x: "${:,.2f}".format(x))
    ACTUALS_SPEND_BY_YEAR_MONTH = ACTUALS_SPEND_BY_YEAR_MONTH.reset_index()
    print("the ACTUALS spend by year and month is ")
    # print the pivot table rounded to the nearest dollar
    print(ACTUALS_SPEND_BY_YEAR_MONTH.round().to_string())
    # melt the pivot table
    print()

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
    # print the df_actuals_check dataframe
    print("the ACTUALS spend by year, month, and expense bucket is ")
    print(df_actuals_check.to_string())

    return {
        'SPEND': ACTUALS_SPEND_EXCLUDING_FUTURE,
        'SPEND_COLS': ['Amount'],
        'SPEND_BY_YEAR': ACTUALS_SPEND_BY_YEAR,
        'SPEND_BY_YEAR_MONTH': ACTUALS_SPEND_BY_YEAR_MONTH,
        'SPEND_BY_YEAR_MONTH_MELTED': df_actuals_check
    }

# END SCRIPT