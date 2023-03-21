from constants import *
import logging
from clean_data import clean_data
from remove_string_from_column import remove_string_from_column
from format_cash_view import format_cash_view
from join_name_map_to_actuals import join_name_map_to_actuals

# START SCRIPT
def clean_actuals_fte(df):
    # function that cleans the actuals FTE data

    df = df.copy()

    ACT_FTE_COLS = [
        'Vendor', 'BU', 'IS Grouping', 'Engineering', 'Function',
        'Project', 'Contact', 'EXPENSE_BUCKET', 'EXPENSE_BUCKET_2',
        'MONTH', 'QUARTER', 'YEAR', 'AMOUNT', 'SAL_BONUS', 'Type',
        'CASH_VIEW', 'PROJ_ACT', 'ALLO_TYPE']

    # create a new array using ACT_FTE_COLS but remove "AMOUNT"
    ACT_FTE_COLS_NO_AMOUNT = ACT_FTE_COLS.copy()
    ACT_FTE_COLS_NO_AMOUNT.remove('AMOUNT')

    df.loc[df['EXPENSE_BUCKET'] == 'FTE']
    df['ALLO_TYPE'] = np.where(df['FTE Function 1'] == 'Shared Services',"SHARED SERVICES", "NOT SHARED SERVICES")
    df['ALLO_TYPE'].fillna("NOT SHARED SERVICES", inplace=True)
    # df['Function'] = df['FTE Function 2']
    df['EXPENSE_BUCKET_2'] = 'FTE_AND_OPEN_ROLES'
    df = df[ACT_FTE_COLS] # filter columns
    df = df.groupby(ACT_FTE_COLS_NO_AMOUNT).sum() # get the sum of amount
    df.reset_index(inplace=True)
    df['ALLOCATION']=1

    return df
# END SCRIPT