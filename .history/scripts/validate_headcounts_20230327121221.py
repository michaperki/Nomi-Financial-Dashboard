from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_fte, df_orm, df_headcounts):
    logging.INFO("\n\nHeadcount Validation\n\n")
    # log the column names of df_fte
    logging.INFO(f"df_fte columns: {df_fte.columns}")
    # log the column type of "Company Seniority Date"
    logging.INFO(f"df_fte['Company Seniority Date'] type: {type(df_fte['Company Seniority Date'][0])}")
    # log column type of "Termination Date"
    logging.INFO(f"df_fte['Termination Date'] type: {type(df_fte['Termination Date'][0])}")
    # log the earliest date in Company Seniority Date
    logging.INFO(f"Earliest date in df_fte['Company Seniority Date']: {df_fte['Company Seniority Date'].min()}")
    # log the latest date in Company Seniority Date
    logging.INFO(f"Latest date in df_fte['Company Seniority Date']: {df_fte['Company Seniority Date'].max()}")
    # log the earliest date in Termination Date
    logging.INFO(f"Earliest date in df_fte['Termination Date']: {df_fte['Termination Date'].min()}")
    # log the latest date in Termination Date
    logging.INFO(f"Latest date in df_fte['Termination Date']: {df_fte['Termination Date'].max()}")
    # log the number of null values in Company Seniority Date
    logging.INFO(f"Number of null values in df_fte['Company Seniority Date']: {df_fte['Company Seniority Date'].isnull().sum()}")
    # log the number of null values in Termination Date
    logging.INFO(f"Number of null values in df_fte['Termination Date']: {df_fte['Termination Date'].isnull().sum()}")
    

# END SCRIPT