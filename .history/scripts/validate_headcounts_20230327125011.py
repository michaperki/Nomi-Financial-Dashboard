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
    logging.info(f"Number of null values in the 'Termination Date' column: {hc_no_depart}")
    hc_depart_2023 = len(df[df['Termination Date'].str.contains('2023')])
    logging.info(f"Number of 2023 values in the 'Termination Date' column: {hc_depart_2023}")
    hc_depart_prior = hc_total - hc_no_depart - hc_depart_2023
    logging.info(f"Number of prior values in the 'Termination Date' column: {hc_depart_prior}")


# END SCRIPT