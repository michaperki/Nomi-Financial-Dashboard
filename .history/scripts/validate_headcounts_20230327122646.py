from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_fte, df_orm, df_headcounts):
    df = df_fte.copy()


    # validate the headcounts
    logging.info("\n\nHeadcount Validation\n\n")
    # log the column names of df_fte
    logging.info(f"df_fte columns: {df.columns}")
    # log the column type of "Company Seniority Date"
    logging.info(f"df_fte['Company Seniority Date'] type: {type(df['Company Seniority Date'][0])}")
    # log column type of "Termination Date"
    logging.info(f"df_fte['Termination Date'] type: {type(df['Termination Date'][0])}")
    # log the number of null values in Company Seniority Date
    logging.info(f"Number of null values in df_fte['Company Seniority Date']: {df['Company Seniority Date'].isnull().sum()}")
    # log the number of null values in Termination Date
    logging.info(f"Number of null values in df_fte['Termination Date']: {df['Termination Date'].isnull().sum()}")

    # filter out the rows where the "Company Seniority Date" is null
    df = df[df['Company Seniority Date'].notnull()]

    # fill the null values in the "Termination Date" column with a date far in the future
    df['Termination Date'].fillna(pd.to_datetime('2099-12-31'), inplace=True)

    # convert the "Company Seniority Date" and "Termination Date" columns to datetime
    df['Company Seniority Date'] = pd.to_datetime(df['Company Seniority Date'])
    df['Termination Date'] = pd.to_datetime(df['Termination Date'])

    # filter the df to only include rows where the "Termination Date" is after 2023-01-01
    df = df[df['Termination Date'] > pd.to_datetime('2023-01-01')]

    # filter the df to only include rows where the "Company Seniority Date" is before 2023-01-01
    df = df[df['Company Seniority Date'] < pd.to_datetime('2023-01-01')]
    logging.info(f"Number of rows in df after filtering: {len(df)}")

    # create a new column called "Headcount" and set it to 1
    df['Headcount'] = 1

    # group the df by "Company Seniority Date" and sum the "Headcount" column
    df = df.groupby('Company Seniority Date').sum()

    # reset the index
    df.reset_index(inplace=True)

    # rename the "Company Seniority Date" column to "Date"
    df.rename(columns={'Company Seniority Date': 'Date'}, inplace=True)

    # set the "Date" column as the index
    df.set_index('Date', inplace=True)

    # log the head of the df
    logging.info(f"Head of df: {df.head()}")

    # log the tail of the df
    logging.info(f"Tail of df: {df.tail()}")




# END SCRIPT