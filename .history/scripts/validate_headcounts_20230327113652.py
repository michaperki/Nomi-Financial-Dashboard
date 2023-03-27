from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_main, df_headcounts):
    # Validate headcounts against main df
    # print the head of both dfs
    
    # filter the main df to only include EXPENSE_BUCKET_2 == "FTE AND OPEN ROLES" and YEAR == CURR_YEAR
    df_main = df_main.loc[(df_main['EXPENSE_BUCKET_2']=='FTE_AND_OPEN_ROLES') & (df_main['YEAR']==CURR_YEAR)]

    # calculate the sum of allocated amount for each month
    df_main_sum = df_main.groupby(['Vendor', 'MONTH'])['ALLOCATED_AMOUNT'].sum().reset_index()

    # calculate the sum of headcount for each month
    df_headcounts_sum = df_headcounts.groupby(['Vendor', 'MONTH'])['AMOUNT'].sum().reset_index()

    # merge the two dfs
    df = df_main_sum.merge(df_headcounts_sum, how='left', left_on=['Vendor', 'MONTH'], right_on=['Vendor', 'MONTH'])

    # calculate the difference between the two dfs
    df['DIFF'] = df['ALLOCATED_AMOUNT'] - df['AMOUNT']

    # print the head of the merged df
    print(df.head().to_string())
    

# END SCRIPT