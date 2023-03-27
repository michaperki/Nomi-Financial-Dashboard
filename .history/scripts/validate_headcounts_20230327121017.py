from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_fte, df_orm, df_headcounts):
    # in df_fte, find any row with a termination date in 1/1/2023-1/31/2023
    df = df_fte.loc[df_fte['Termination Date'].between('1/1/2023', '1/31/2023')]
    print(df)
    # print the head of the df
    logging.INFO("\n\nHeadcount Validation\n\n")
    logging.INFO(df.head())    

# END SCRIPT