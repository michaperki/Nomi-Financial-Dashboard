from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_main, df_headcounts):
    # Validate headcounts against main df

    # filter the main df to only include EXPENSE_BUCKET_2 == "FTE AND OPEN ROLES" and YEAR == CURR_YEAR
    df_main = df_main.loc[(df_main['EXPENSE_BUCKET_2']=='FTE AND OPEN ROLES') & (df_main['YEAR']==CURR_YEAR)]

    # filter the headcounts df to exclude MONTH == "ALL"
    df_headcounts = df_headcounts.loc[df_headcounts['MONTH']!='99']

    # calculate the sum of allocated amount for each month
    df_main_sum = df_main.groupby(['MONTH'])['ALLOCATED_AMOUNT'].sum().reset_index()

    # calculate the sum of headcount for each month
    df_headcounts_sum = df_headcounts.groupby(['MONTH'])['ALLOCATED_AMOUNT'].sum().reset_index()

    # rename the ALLOCATED_AMOUNT column to HEADCOUNTS
    df_headcounts_sum.rename(columns={'ALLOCATED_AMOUNT': 'HEADCOUNTS'}, inplace=True)

    # merge the two dfs
    df = df_main_sum.merge(df_headcounts_sum, how='left', left_on=['MONTH'], right_on=['MONTH'])

    # calculate the difference between the two sums
    df['DIFF'] = df['ALLOCATED_AMOUNT'] - df['HEADCOUNTS']

    # print the head of the df
    logging.INFO("\n\nHeadcount Validation\n\n")
    logging.INFO(df.head())




    # print the head of the df
    print(df.head())
    

# END SCRIPT