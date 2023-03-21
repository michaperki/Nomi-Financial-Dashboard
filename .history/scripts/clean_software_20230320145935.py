import logging
import pandas as pd

from constants import *
from clean_data import clean_data
from clean_projections import clean_projections

# START SCRIPT
def clean_pro_serv(df):
    # function that cleans the Professional Services data
    df = clean_data(df)

    df['Engineering'] = "NOT ENGINEERING"
    df['EXPENSE_BUCKET'] = 'PRO_SERV'
    df[BONUS_COLS] = 0

    df = clean_projections(df)

    return df
# END SCRIPT