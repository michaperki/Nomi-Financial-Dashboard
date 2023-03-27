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

    # create a new column called "Month" and set it to the month of the "Company Seniority Date"
    df['Month'] = df['Company Seniority Date'].dt.month

    # create a new column called "Headcount" and set it to 1
    df['Headcount'] = 1

    # group the df by "Company Seniority Date" and sum the "Headcount" column
    df = df.groupby('Month').sum()

    # reset the index
    df.reset_index(inplace=True)

    # rename the "Company Seniority Date" column to "Date"
    df.rename(columns={'Month': 'Date'}, inplace=True)

    # set the "Date" column as the index
    df.set_index('Date', inplace=True)

    # get the sum of the "Headcount" column where the index is 1
    expected_january = df.loc[1, 'Headcount']
    # get the sum of the "Headcount" column where the index is 2
    expected_february = df.loc[2, 'Headcount']
    # get the sum of the "Headcount" column where the index is 3
    expected_march = df.loc[3, 'Headcount']
    # get the sum of the "Headcount" column where the index is 4
    expected_april = df.loc[4, 'Headcount']
    # get the sum of the "Headcount" column where the index is 5
    expected_may = df.loc[5, 'Headcount']
    # get the sum of the "Headcount" column where the index is 6
    expected_june = df.loc[6, 'Headcount']
    # get the sum of the "Headcount" column where the index is 7
    expected_july = df.loc[7, 'Headcount']
    # get the sum of the "Headcount" column where the index is 8
    expected_august = df.loc[8, 'Headcount']
    # get the sum of the "Headcount" column where the index is 9
    expected_september = df.loc[9, 'Headcount']
    # get the sum of the "Headcount" column where the index is 10
    expected_october = df.loc[10, 'Headcount']
    # get the sum of the "Headcount" column where the index is 11
    expected_november = df.loc[11, 'Headcount']
    # get the sum of the "Headcount" column where the index is 12
    expected_december = df.loc[12, 'Headcount']

    # log the expected values
    logging.info(f"Expected January: {expected_january}")
    logging.info(f"Expected February: {expected_february}")
    logging.info(f"Expected March: {expected_march}")
    logging.info(f"Expected April: {expected_april}")
    logging.info(f"Expected May: {expected_may}")
    logging.info(f"Expected June: {expected_june}")
    logging.info(f"Expected July: {expected_july}")
    logging.info(f"Expected August: {expected_august}")
    logging.info(f"Expected September: {expected_september}")
    logging.info(f"Expected October: {expected_october}")
    logging.info(f"Expected November: {expected_november}")
    logging.info(f"Expected December: {expected_december}")
    



# END SCRIPT