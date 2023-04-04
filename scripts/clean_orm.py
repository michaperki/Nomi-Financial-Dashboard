from constants import *
from clean_data import clean_data
from clean_projections import clean_projections

# START SCRIPT
def clean_orm(df):

    # filter for HC = 1
    df = df.loc[df['HC'] == 1]

    # function that cleans the ORM data
    df = clean_data(df)

    df.rename(columns={
            'BU-FUNCTION KEY'       : 'BU-Function Key',
            'Start Date'            : 'Company Seniority Date',
            'Monthly Fully-Loaded'  : 'PnL Monthly',
            'Supervisor Name'       : 'Contact'
        }, inplace=True)

    df.columns = df.columns.str.replace("Fully-Loaded", "PnL")

    df["Vendor"]            = "# NO VENDOR"
    df["Project"]           = "# NO PROJECT"
    df['EXPENSE_BUCKET']    = "OPEN_ROLES"

    df[BONUS_COLS] = 0

    df['Engineering'].fillna('NOT ENGINEERING', inplace=True)

    df = df.loc[(df['BU'] != '') & (df['BU'].notnull())]

    df = clean_projections(df)

    return df
# END SCRIPT