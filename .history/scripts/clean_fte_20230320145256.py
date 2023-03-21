import logging
import pandas as pd

from constants import *
from clean_projections import clean_projections

# START SCRIPT
def clean_fte(df):
    # function that cleans the FTE data

    df = clean_data(df)

    df.rename(columns={'Supervisor Name': 'Contact'}, inplace=True)
    df["Vendor"] = "# NO VENDOR"
    df["Project"] = "# NO PROJECT"
    df['Engineering'].fillna('NOT ENGINEERING', inplace=True)
    df['EXPENSE_BUCKET'] = 'FTE'
    df = df.loc[(df['BU'] != '') & (df['BU'].notnull())]

    df = clean_projections(df)

    return df
# END SCRIPT