from constants import *
import logging

# START SCRIPT
def clean_orm_for_hc(df):
    # function that cleans the ORM data for HC (doesn't run the format_projections functions)

    # filter for HC = 1
    df = df.loc[df['HC'] == 1]

    # function that cleans the ORM data
    df = clean_data(df)

    df.rename(columns={
            'BU-FUNCTION KEY'       : 'BU-Function Key',
            'Start Date'            : 'Company Seniority Date',
            'Monthly Fully-Loaded'  : 'PnL Monthly'
        }, inplace=True)

    df.columns = df.columns.str.replace("Fully-Loaded", "PnL")

    df["Vendor"]            = "# NO VENDOR"
    df["Project"]           = "# NO PROJECT"
    df['EXPENSE_BUCKET']    = "OPEN_ROLES"
    
    # if the BONUS_COLS are not in the df, add them and fill with 0
    for col in BONUS_COLS:
        if col not in df.columns:
            df[col] = 0

    df['Engineering'].fillna('NOT ENGINEERING', inplace=True)

    df = df.loc[(df['BU'] != '') & (df['BU'].notnull())]

    return df
# END SCRIPT