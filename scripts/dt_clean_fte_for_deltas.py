from constants import *
from clean_data import clean_data

# START SCRIPT
def clean_fte_for_deltas(df):
    # function that cleans the Software data

    df = clean_data(df)

    df.rename(columns={'Supervisor Name': 'Contact'}, inplace=True)
    df["Project"] = "# NO PROJECT"
    df["Vendor"] = "# NO VENDOR"
    df['Engineering'].fillna("NOT ENGINEERING")
    df['EXPENSE_BUCKET'] = 'FTE'
    df[BONUS_COLS].fillna(0)
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