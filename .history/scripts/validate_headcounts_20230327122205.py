from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_fte, df_orm, df_headcounts):
    # validate the headcounts
    logging.info("\n\nHeadcount Validation\n\n")
    # log the column names of df_fte
    logging.info(f"df_fte columns: {df_fte.columns}")
    # log the column type of "Company Seniority Date"
    logging.info(f"df_fte['Company Seniority Date'] type: {type(df_fte['Company Seniority Date'][0])}")
    # log column type of "Termination Date"
    logging.info(f"df_fte['Termination Date'] type: {type(df_fte['Termination Date'][0])}")
    # log the number of null values in Company Seniority Date
    logging.info(f"Number of null values in df_fte['Company Seniority Date']: {df_fte['Company Seniority Date'].isnull().sum()}")
    # log the number of null values in Termination Date
    logging.info(f"Number of null values in df_fte['Termination Date']: {df_fte['Termination Date'].isnull().sum()}")

    # filter out the rows where the "Company Seniority Date" is null
    df_fte = df_fte[df_fte['Company Seniority Date'].notnull()]

    # fill the null values in the "Termination Date" column with a date far in the future
    df_fte['Termination Date'].fillna(pd.to_datetime('2099-12-31'), inplace=True)

    # convert the "Company Seniority Date" and "Termination Date" columns to datetime
    df_fte['Company Seniority Date'] = pd.to_datetime(df_fte['Company Seniority Date'])
    df_fte['Termination Date'] = pd.to_datetime(df_fte['Termination Date'])

    # filter the df to only include rows where the "Termination Date" is after 2023-01-01
    df_fte = df_fte[df_fte['Termination Date'] > pd.to_datetime('2023-01-01')]

    # log the number of Termination Dates in January 2023 (any day in this month)
    logging.info(f"Number of Termination Dates in January 2023: {df_fte[df_fte['Termination Date'] < pd.to_datetime('2023-31-01')].shape[0]}")


# END SCRIPT