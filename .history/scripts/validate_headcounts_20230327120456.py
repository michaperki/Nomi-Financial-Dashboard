from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_fte, df_orm, df_headcounts):
    # df_fte has the columns Company Seniority Date and Termination Date
    # Seniority Date is the date the employee started
    # Termination Date is the date the employee left
    # df_orm has the columns Start Date and Termination Date
    # Start Date is the date the employee started
    # Termination Date is the date the employee left
    # df_headcounts has the total headcount for each month
    # df_headcounts has the columns Month, and Headcount

    # calculate the number of employees in each month of 2023 in df_fte
    # for each month, count the number of employees that have a Seniority Date prior to the end of the month and a Termination Date after the start of the month

    df = df_fte.copy()
    print(df.head())



    # print the head of the df
    logging.INFO("\n\nHeadcount Validation\n\n")

    

# END SCRIPT