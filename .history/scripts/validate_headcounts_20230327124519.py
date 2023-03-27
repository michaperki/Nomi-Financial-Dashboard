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
    

    # get the number of rows in df_fte where the "Company Seniority Date" contains "2019", "2020", "2021", or "2022"
    logging.info(f"Number of rows in df_fte where the 'Company Seniority Date ' contains '2019', '2020', '2021', or '2022': {len(df_fte[df_fte['Company Seniority Date'].str.contains('2019|2020|2021|2022')])}")





# END SCRIPT