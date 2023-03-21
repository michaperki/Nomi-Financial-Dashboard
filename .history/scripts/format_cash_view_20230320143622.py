from constants import *
import logging
from clean_data import clean_data
from remove_string_from_column import remove_string_from_column

# START SCRIPT
def format_cash_view(df):
    df = df.copy(deep=True)

    # fill the blank cells in 'Cash View (FTC, PS, SW)' with 'ACCRUALS' and convert to uppercase
    df['Cash View (FTC, PS, SW)'].fillna('ACCRUALS', inplace=True)
    df['Cash View (FTC, PS, SW)'] = df['Cash View (FTC, PS, SW)'].str.upper()

    df.loc[  (df['SAL_BONUS'] == 'SALARY') & (df['EXPENSE_BUCKET'] == 'FTE'), 'Cash View (FTC, PS, SW)'] = 'CASH'
    df.loc[  (df['SAL_BONUS'] != 'SALARY') & (df['EXPENSE_BUCKET'] == 'FTE'), 'Cash View (FTC, PS, SW)'] = 'ACCRUALS'

    # rename the column 'Cash View (FTC, PS, SW)' to 'CASH_VIEW'
    df.rename(columns={'Cash View (FTC, PS, SW)':'CASH_VIEW'}, inplace=True)
    logging.debug("...unique values in CASH_VIEW column: " + list(df['CASH_VIEW'].unique()))

    return df
# END SCRIPT