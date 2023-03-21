import logging
import pandas as pd

from constants import *


# START SCRIPT

def clean_projections(df):

    df = df.copy()

    df = df[ALL_PROJ_COLS]

    df = df.groupby([
        'Vendor',
        'BU',
        'IS Grouping',
        'Engineering',
        'Function',
        'Project',
        'Contact',
        'EXPENSE_BUCKET'
        ], dropna=False)[SPEND_COLS_W_BONUS].sum()

    # Clean summary data by reseting the index and parsing key
    df.reset_index(inplace=True)

    ### FORMAT PROJECTIONS ###
    df = pd.melt(
        df,
        id_vars=[
        'Vendor',
        'BU',
        'IS Grouping',
        'Engineering',
        'Function',
        'Project',
        'Contact',
        'EXPENSE_BUCKET'
        ],
        value_vars=SPEND_COLS_W_BONUS,
        var_name='MONTH',
        value_name='AMOUNT'
        )

    df['MONTH'] = df['MONTH'].replace(DICT_W_BONUS)
    df[['MONTH','SAL_BONUS']] = df['MONTH'].str.split("|", expand=True)

    df['YEAR'] = CURR_YEAR
    df['Type'] = "# NO TYPE"

    df = df.loc[(df['AMOUNT'] != 0) & (df['AMOUNT'].notnull())]
    df['PROJ_ACT'] = 'PROJECTION'
    df['QUARTER'] = pd.to_datetime(df['MONTH'].values, format='%m').astype('period[Q]').astype(str).str[-1:]

    return df

# END SCRIPT