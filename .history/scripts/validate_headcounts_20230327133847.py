from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_fte, df_orm, df_headcounts):
    df = df_fte.copy()

    # validate the headcounts
    logging.info("\n\nHeadcount Validation\n\n")
    logging.info("FTE")
    # filter df to get rid of null values in the "Company Seniority Date" column
    df = df[df['Company Seniority Date'].notna()]

    # print the number of rows in the df
    logging.info(f"Number of rows in df: {len(df)}")

    # count the number of 2020 values in the "Company Seniority Date" column
    hc_2019 = len(df[df['Company Seniority Date'].str.contains('2019')])
    logging.info(f"Number of 2019 values in the 'Company Seniority Date' column: {hc_2019}")
    hc_2020 = len(df[df['Company Seniority Date'].str.contains('2020')])
    logging.info(f"Number of 2020 values in the 'Company Seniority Date' column: {hc_2020}")
    hc_2021 = len(df[df['Company Seniority Date'].str.contains('2021')])
    logging.info(f"Number of 2021 values in the 'Company Seniority Date' column: {hc_2021}")
    hc_2022 = len(df[df['Company Seniority Date'].str.contains('2022')])
    logging.info(f"Number of 2022 values in the 'Company Seniority Date' column: {hc_2022}")
    hc_2023 = len(df[df['Company Seniority Date'].str.contains('2023')])
    logging.info(f"Number of 2023 values in the 'Company Seniority Date' column: {hc_2023}")

    # total the number of rows in the df
    hc_total = hc_2019 + hc_2020 + hc_2021 + hc_2022 + hc_2023
    logging.info(f"Total number of rows in the df: {hc_total}")

    hc_no_depart = len(df[df['Termination Date'].isna()])
    # filter df to get rid of null values in the "Termination Date" column
    df = df[df['Termination Date'].notna()]
    logging.info(f"Number of null values in the 'Termination Date' column: {hc_no_depart}")
    hc_depart_2023 = len(df[df['Termination Date'].str.contains('2023')])
    logging.info(f"Number of 2023 values in the 'Termination Date' column: {hc_depart_2023}")
    hc_depart_prior = hc_total - hc_no_depart - hc_depart_2023
    logging.info(f"Number of prior values in the 'Termination Date' column: {hc_depart_prior}")

    # number of employees at the start of 2023
    hc_start_2023 = hc_total - hc_depart_prior - hc_2023
    logging.info(f"Number of employees at the start of 2023: {hc_start_2023}")

    # number of employees at the end of 2023
    hc_end_2023 = hc_start_2023 + hc_2023 - hc_depart_2023
    logging.info(f"Number of employees at the end of 2023: {hc_end_2023}")

    logging.info("\n\nORM")
    df = df_orm.copy()

    # print the columns in the df
    
    # filter df to get rid of null values in the "Start Date" column
    df = df[df['Company Seniority Date'].notna()]
    # filter to get rows where 'HC' is 1
    df = df[df['HC'] == 1]

    # print the number of rows in the df
    logging.info(f"Number of rows in df: {len(df)}")


    # log the head of df_headcounts
    logging.info("\n\nHeadcounts")
    df_actual = df_headcounts.copy()
    # filter for CATEGORY = 'HC_JOIN' or 'HC_DEPART'
    df_actual = df_actual[(df_actual['CATEGORY'] == 'HC_JOIN') | (df['CATEGORY'] == 'HC_DEPART')]

    df = df_actual.loc[df_actual['CATEGORY'] == 'HC_JOIN']

    # filter f
    
    hc_2023 = df[df['YEAR'] == 2023]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of 2023 values in the 'ALLOCATION' column: {hc_2023}")
    hc_2023_jan = df[(df['YEAR'] == 2023) & (df['MONTH'] == '01')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of JANUARY 2023 values in the 'ALLOCATION' column: {hc_2023_jan}")
    hc_2023_feb = df[(df['YEAR'] == 2023) & (df['MONTH'] == '02')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of FEBRUARY 2023 values in the 'ALLOCATION' column: {hc_2023_feb}")
    hc_2023_mar = df[(df['YEAR'] == 2023) & (df['MONTH'] == '03')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of MARCH 2023 values in the 'ALLOCATION' column: {hc_2023_mar}")
    hc_2023_apr = df[(df['YEAR'] == 2023) & (df['MONTH'] == '04')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of APRIL 2023 values in the 'ALLOCATION' column: {hc_2023_apr}")
    hc_2023_may = df[(df['YEAR'] == 2023) & (df['MONTH'] == '05')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of MAY 2023 values in the 'ALLOCATION' column: {hc_2023_may}")
    hc_2023_jun = df[(df['YEAR'] == 2023) & (df['MONTH'] == '06')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of JUNE 2023 values in the 'ALLOCATION' column: {hc_2023_jun}")
    hc_2023_jul = df[(df['YEAR'] == 2023) & (df['MONTH'] == '07')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of JULY 2023 values in the 'ALLOCATION' column: {hc_2023_jul}")
    hc_2023_aug = df[(df['YEAR'] == 2023) & (df['MONTH'] == '08')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of AUGUST 2023 values in the 'ALLOCATION' column: {hc_2023_aug}")
    hc_2023_sep = df[(df['YEAR'] == 2023) & (df['MONTH'] == '09')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of SEPTEMBER 2023 values in the 'ALLOCATION' column: {hc_2023_sep}")
    hc_2023_oct = df[(df['YEAR'] == 2023) & (df['MONTH'] == '10')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of OCTOBER 2023 values in the 'ALLOCATION' column: {hc_2023_oct}")
    hc_2023_nov = df[(df['YEAR'] == 2023) & (df['MONTH'] == '11')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of NOVEMBER 2023 values in the 'ALLOCATION' column: {hc_2023_nov}")
    hc_2023_dec = df[(df['YEAR'] == 2023) & (df['MONTH'] == '12')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of DECEMBER 2023 values in the 'ALLOCATION' column: {hc_2023_dec}")

    df = df_actual.loc[df_actual['CATEGORY'] == 'HC_DEPART']
    hc_depart_2023 = df[df['YEAR'] == 2023]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of 2023 values in the 'ALLOCATION' column: {hc_depart_2023}")
    hc_depart_2023_jan = df[(df['YEAR'] == 2023) & (df['MONTH'] == '01')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of JANUARY 2023 values in the 'ALLOCATION' column: {hc_depart_2023_jan}")
    hc_depart_2023_feb = df[(df['YEAR'] == 2023) & (df['MONTH'] == '02')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of FEBRUARY 2023 values in the 'ALLOCATION' column: {hc_depart_2023_feb}")
    hc_depart_2023_mar = df[(df['YEAR'] == 2023) & (df['MONTH'] == '03')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of MARCH 2023 values in the 'ALLOCATION' column: {hc_depart_2023_mar}")
    hc_depart_2023_apr = df[(df['YEAR'] == 2023) & (df['MONTH'] == '04')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of APRIL 2023 values in the 'ALLOCATION' column: {hc_depart_2023_apr}")
    hc_depart_2023_may = df[(df['YEAR'] == 2023) & (df['MONTH'] == '05')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of MAY 2023 values in the 'ALLOCATION' column: {hc_depart_2023_may}")
    hc_depart_2023_jun = df[(df['YEAR'] == 2023) & (df['MONTH'] == '06')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of JUNE 2023 values in the 'ALLOCATION' column: {hc_depart_2023_jun}")
    hc_depart_2023_jul = df[(df['YEAR'] == 2023) & (df['MONTH'] == '07')]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of JULY 202





    

# END SCRIPT