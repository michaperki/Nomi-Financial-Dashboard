import logging
import pandas as pd

from constants import *
from clean_data import clean_data
from clean_projections import clean_projections

# START SCRIPT
def clean_ftc(df):
    # function that cleans the FTC data
    df = clean_data(df)

    df.rename(columns={'Owner': 'Contact'}, inplace=True)

    df['Project'] = df['Project'].fillna("# NO PROJECT")
    df['Contact'] = df['Contact'].fillna("# NO CONTACT")

    df['Engineering'] = "NOT ENGINEERING"
    df['EXPENSE_BUCKET'] = 'FTC'

    df[BONUS_COLS] = 0

    df = clean_projections(df)

    return df
# END SCRIPT