from constants import *
import logging
from clean_data import clean_data

# START SCRIPT
def clean_ftc_for_deltas(df):
    # function that cleans the Software data

    df = clean_data(df)

    df.rename(columns={'Owner': 'Contact'}, inplace=True)

    df["Project"].fillna("# NO PROJECT", inplace=True)
    df['Engineering'] = "NOT ENGINEERING"
    df['EXPENSE_BUCKET'] = 'FTC'
    df[BONUS_COLS] = 0
    # df = clean_projections(df)
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
    df.reset_index(inplace=True)
    return df
# END SCRIPT