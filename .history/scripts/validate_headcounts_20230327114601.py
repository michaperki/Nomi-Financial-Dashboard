from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_main, df_headcounts):
    # Validate headcounts against main df
    # print the head of both dfs

    print(df_main.head())
    print(df_headcounts.head())

    # filter the main df to only include EXPENSE_BUCKET_2 == "FTE AND OPEN ROLES" and YEAR == CURR_YEAR
    df_main = df_main.loc[(df_main['EXPENSE_BUCKET_2']=='FTE_AND_OPEN_ROLES') & (df_main['YEAR']==CURR_YEAR_STR)]

    # print the dimensions of the main df
    print(df_main.shape)

    # calculate the sum of allocated amount for each month
    df_main_sum = df_main.groupby(['MONTH'])['ALLOCATED_AMOUNT'].sum().reset_index()

    # print the head of the main df
    print(df_main_sum.head())

    # calculate the sum of headcount for each month
    df_headcounts_sum = df_headcounts.groupby(['MONTH'])['AMOUNT'].sum().reset_index()

    # print the head of the headcounts df
    print(df_headcounts_sum.head())

    # merge the two dfs
    df = df_main_sum.merge(df_headcounts_sum, how='left', left_on=['MONTH'], right_on=['MONTH'])

    # calculate the difference between the two
    df['DIFF'] = df['ALLOCATED_AMOUNT'] - df['AMOUNT']



    # print the head of the df
    print(df.head())
    

# END SCRIPT