from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_fte, df_orm, df_headcounts):
    # filter df_fte to only include employees termination date in January 2023 (any day in the month))
    df_fte = df_fte[df_fte['Termination Date'].dt.month == 1] 

    # print the head of the df
    logging.INFO("\n\nHeadcount Validation\n\n")

    

# END SCRIPT