from constants import *
from clean_data import clean_data
from clean_projections import clean_projections

# START SCRIPT
def clean_software(df):
    # function that cleans the Software data

    df = clean_data(df)

    df.rename(columns={'Owner': 'Contact'}, inplace=True)
    df["Project"] = "# NO PROJECT"
    df['Engineering'] = "NOT ENGINEERING"
    df['EXPENSE_BUCKET'] = 'SOFTWARE'
    df[BONUS_COLS] = 0
    df = clean_projections(df)

    return df
# END SCRIPT