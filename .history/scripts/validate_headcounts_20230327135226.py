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

    hc_2020 = len(df[df['Company Seniority Date'].str.contains('2020')])
    hc_2021 = len(df[df['Company Seniority Date'].str.contains('2021')])
    hc_2022 = len(df[df['Company Seniority Date'].str.contains('2022')])
    hc_2023 = len(df[df['Company Seniority Date'].str.contains('2023')])

    # total the number of rows in the df
    hc_total = hc_2020 + hc_2021 + hc_2022 + hc_2023
    hc_no_depart = len(df[df['Termination Date'].isna()])

    # filter df to get rid of null values in the "Termination Date" column
    df = df[df['Termination Date'].notna()]
    hc_depart_2023 = len(df[df['Termination Date'].str.contains('2023')])
    hc_depart_prior = hc_total - hc_no_depart - hc_depart_2023

    # number of employees at the start of 2023
    hc_start_2023 = hc_total - hc_depart_prior - hc_2023
    logging.info(f"Number of employees at the start of 2023: {hc_start_2023}")

    # number of employees at the end of 2023
    hc_end_2023 = hc_start_2023 + hc_2023 - hc_depart_2023
    logging.info(f"Number of employees at the end of 2023: {hc_end_2023}")

    df = df_orm.copy()    
    # filter df to get rid of null values in the "Start Date" column
    df = df[df['Company Seniority Date'].notna()]
    # filter to get rows where 'HC' is 1
    df = df[df['HC'] == 1]
    orm_addition = len(df)

    hc_end_2023 = hc_end_2023 + orm_addition
    logging.info(f"Number of employees at the end of 2023 after ORM additions: {hc_end_2023}")

    valid_change_in_hc = hc_end_2023 - hc_start_2023

    # log the head of df_headcounts
    logging.info("\n\nHeadcounts")
    df_actual = df_headcounts.copy()
    # filter for CATEGORY = 'HC_JOIN' or 'HC_DEPART'
    df_actual = df_actual[(df_actual['CATEGORY'] == 'HC_JOIN') | (df_actual['CATEGORY'] == 'HC_DEPART')]

    df = df_actual.loc[df_actual['CATEGORY'] == 'HC_JOIN'].copy()
    
    hc_2023 = df[df['YEAR'] == 2023]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of 2023 values in the 'ALLOCATION' column: {hc_2023}")

    df = df_actual.loc[df_actual['CATEGORY'] == 'HC_DEPART'].copy()
    hc_depart_2023 = df[df['YEAR'] == 2023]['ALLOCATED_AMOUNT'].sum()
    logging.info(f"Number of 2023 values in the 'ALLOCATION' column: {hc_depart_2023}")

    change_in_hc = hc_2023 - hc_depart_2023

    # round both values to the nearest whole number
    change_in_hc = round(change_in_hc)
    valid_change_in_hc = round(valid_change_in_hc)
    
    logging.info(f"Change in headcount: {change_in_hc}")

    logging.info(f"Valid change in headcount: {valid_change_in_hc}")
    validate(valid_change_in_hc, change_in_hc)





    

# END SCRIPT