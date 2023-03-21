import logging
import pandas as pd
from constants import *
from clean_data import clean_data

# START SCRIPT
def clean_fte_for_hc(df):
    # function that cleans the FTE data for HC (doesn't run the format_projections functions)
    df = clean_data(df)

    df["Vendor"] = "# NO VENDOR"
    df["Project"] = "# NO PROJECT"
    df['Engineering'].fillna('NOT ENGINEERING', inplace=True)
    df['EXPENSE_BUCKET'] = 'FTE'
    df = df.loc[(df['BU'] != '') & (df['BU'].notnull())]

    return df
# END SCRIPT