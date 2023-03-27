from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_fte, df_orm, df_headcounts):
    df = df_fte.copy()

    # validate the headcounts
    logging.info("\n\nHeadcount Validation\n\n")

    # filter df to get rid of null values in the "Company Seniority Date" column
    df = df[df['Company Seniority Date'].notna()]

    # print the number of rows in the df
    logging.info(f"Number of rows in df: {len(df)}")

    # count the number of 2020 values in the "Company Seniority Date" column
    logging.info(f"Number of 2020 values in the 'Company Seniority Date' column: {len(df[df['Company Seniority Date'].str.contains('2020')])}")




# END SCRIPT