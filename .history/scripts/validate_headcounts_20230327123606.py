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
    df_join = df.groupby('Month').sum()

    # reset the index
    df_join.reset_index(inplace=True)

    # rename the "Company Seniority Date" column to "Date"
    df_join.rename(columns={'Month': 'Date'}, inplace=True)

    # set the "Date" column as the index
    df_join.set_index('Date', inplace=True)

    # get the sum of the "Headcount" column where the index is 1
    expected_january = df_join.loc[1, 'Headcount']
    # get the sum of the "Headcount" column where the index is 2
    expected_february = df_join.loc[2, 'Headcount']
    # get the sum of the "Headcount" column where the index is 3
    expected_march = df_join.loc[3, 'Headcount']
    # get the sum of the "Headcount" column where the index is 4
    expected_april = df_join.loc[4, 'Headcount']
    # get the sum of the "Headcount" column where the index is 5
    expected_may = df_join.loc[5, 'Headcount']
    # get the sum of the "Headcount" column where the index is 6
    expected_june = df_join.loc[6, 'Headcount']
    # get the sum of the "Headcount" column where the index is 7
    expected_july = df_join.loc[7, 'Headcount']
    # get the sum of the "Headcount" column where the index is 8
    expected_august = df_join.loc[8, 'Headcount']
    # get the sum of the "Headcount" column where the index is 9
    expected_september = df_join.loc[9, 'Headcount']
    # get the sum of the "Headcount" column where the index is 10
    expected_october = df_join.loc[10, 'Headcount']
    # get the sum of the "Headcount" column where the index is 11
    expected_november = df_join.loc[11, 'Headcount']
    # get the sum of the "Headcount" column where the index is 12
    expected_december = df_join.loc[12, 'Headcount']

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

    # create a new column called "Depart Month" and set it to the month of the "Termination Date"
    df['Depart Month'] = df['Termination Date'].dt.month

    # create a new column called "Depart Headcount" and set it to 1
    df['Depart Headcount'] = 1

    # group the df by "Depart Month" and sum the "Depart Headcount" column
    df_depart = df.groupby('Depart Month').sum()

    # reset the index
    df_depart.reset_index(inplace=True)

    # rename the "Depart Month" column to "Date"
    df_depart.rename(columns={'Depart Month': 'Date'}, inplace=True)

    # set the "Date" column as the index
    df_depart.set_index('Date', inplace=True)

    # get the sum of the "Depart Headcount" column where the index is 1
    depart_january = df_depart.loc[1, 'Depart Headcount']
    # get the sum of the "Depart Headcount" column where the index is 2
    depart_february = df_depart.loc[2, 'Depart Headcount']
    # get the sum of the "Depart Headcount" column where the index is 3
    depart_march = df_depart.loc[3, 'Depart Headcount']
    # get the sum of the "Depart Headcount" column where the index is 4
    depart_april = df_depart.loc[4, 'Depart Headcount']
    # get the sum of the "Depart Headcount" column where the index is 5
    depart_may = df_depart.loc[5, 'Depart Headcount']
    # get the sum of the "Depart Headcount" column where the index is 6
    depart_june = df_depart.loc[6, 'Depart Headcount']
    # get the sum of the "Depart Headcount" column where the index is 7
    depart_july = df_depart.loc[7, 'Depart Headcount']
    # get the sum of the "Depart Headcount" column where the index is 8
    depart_august = df_depart.loc[8, 'Depart Headcount']
    # get the sum of the "Depart Headcount" column where the index is 9
    depart_september = df_depart.loc[9, 'Depart Headcount']
    # get the sum of the "Depart Headcount" column where the index is 10
    depart_october = df_depart.loc[10, 'Depart Headcount']
    # get the sum of the "Depart Headcount" column where the index is 11
    depart_november = df_depart.loc[11, 'Depart Headcount']
    # get the sum of the "Depart Headcount" column where the index is 12
    depart_december = df_depart.loc[12, 'Depart Headcount']

    # log the expected values
    logging.info(f"Depart January: {depart_january}")
    logging.info(f"Depart February: {depart_february}")
    logging.info(f"Depart March: {depart_march}")
    logging.info(f"Depart April: {depart_april}")
    logging.info(f"Depart May: {depart_may}")
    logging.info(f"Depart June: {depart_june}")
    logging.info(f"Depart July: {depart_july}")
    logging.info(f"Depart August: {depart_august}")
    logging.info(f"Depart September: {depart_september}")
    logging.info(f"Depart October: {depart_october}")
    logging.info(f"Depart November: {depart_november}")
    logging.info(f"Depart December: {depart_december}")







# END SCRIPT