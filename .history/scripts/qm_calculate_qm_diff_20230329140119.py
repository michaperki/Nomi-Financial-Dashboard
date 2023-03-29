from constants import *
import logging
from clean_data import clean_data
import pandas as pd
from remove_string_from_column import remove_string_from_column
from qt_get_quarters_from_file_name import get_quarters_from_file_name
from qt_get_latest_data_for_each_quarter import get_latest_data_for_each_quarter
from qt_move_actuals_forward_one_quarter import move_actuals_forward_one_quarter
from qt_main_function_no_actuals import main_function_no_actuals
from qt_main_function import main_function




# START SCRIPT
def calculate_qm_diff(df_main, df_quarterly):
    df_monthly_diff = df_main.copy( deep=True )
    df_quarterly_diff = df_quarterly.copy( deep=True )
    df_monthly_diff = df_monthly_diff[df_monthly_diff['YEAR'] == CURR_YEAR]
    df_quarterly_diff = df_quarterly_diff[df_quarterly_diff['YEAR'] == CURR_YEAR]
    df_monthly_diff = df_monthly_diff[df_monthly_diff['CURRENT'] == '1']
    df_monthly_diff = df_monthly_diff.rename(columns={"ALLOCATED_AMOUNT": "VALUE_MONTHLY"})
    df_quarterly_diff = df_quarterly_diff.rename(columns={"ALLOCATED_AMOUNT": "VALUE_QUARTERLY"})
    df_monthly_diff['MONTH'] = df_monthly_diff['MONTH'].astype(int)
    df_quarterly_diff['MONTH'] = df_quarterly_diff['MONTH'].astype(int)
    # filter for the same columns
    df_monthly_diff = df_monthly_diff[['YEAR', 'QUARTER', 'MONTH', 'MONTH_NAME', 'Vendor', 'BU', 'Function', 'SAL_BONUS', 'IS Grouping', 'EXPENSE_BUCKET', 'ALLO_TYPE', 'VALUE_MONTHLY']]
    df_quarterly_diff = df_quarterly_diff[['YEAR', 'QUARTER', 'MONTH', 'MONTH_NAME', 'Vendor', 'BU', 'Function', 'SAL_BONUS', 'IS Grouping', 'EXPENSE_BUCKET', 'ALLO_TYPE', 'VALUE_QUARTERLY']]
    # join the data frames using a full outer join
    df_qm_diff = pd.merge(df_monthly_diff, df_quarterly_diff, how='outer', on=['YEAR', 'QUARTER', 'MONTH', 'MONTH_NAME', 'Vendor', 'BU', 'Function', 'SAL_BONUS', 'IS Grouping', 'EXPENSE_BUCKET', 'ALLO_TYPE'])
    # fill the missing values with 0
    df_qm_diff['VALUE_MONTHLY'] = df_qm_diff['VALUE_MONTHLY'].fillna(0)
    df_qm_diff['VALUE_QUARTERLY'] = df_qm_diff['VALUE_QUARTERLY'].fillna(0)
    # calculate the difference    # calculate the difference
    df_qm_diff['QM_DIFF'] = df_qm_diff['VALUE_MONTHLY'] - df_qm_diff['VALUE_QUARTERLY']

    # group by the YEAR, QUARTER, MONTH, BU, EXPENSE_BUCKET, ALLO_TYPE, Function, SAL_BONUS, IS Grouping, Vendor and sum the QM_DIFF, VALUE_MONTHLY, VALUE_QUARTERLY
    df_qm_diff = df_qm_diff.groupby(['YEAR', 'QUARTER', 'MONTH', 'MONTH_NAME', 'BU', 'EXPENSE_BUCKET', 'ALLO_TYPE', 'Function', 'SAL_BONUS', 'IS Grouping', 'Vendor']).agg({'QM_DIFF': 'sum', 'VALUE_MONTHLY': 'sum', 'VALUE_QUARTERLY': 'sum'}).reset_index()

    # if the absolute value of the QM_DIFF is less than 1, set it to 0
    df_qm_diff['QM_DIFF'] = df_qm_diff['QM_DIFF'].apply(lambda x: 0 if abs(x) < 1 else x)
    # remove the rows where the QM_DIFF is null
    df_qm_diff = df_qm_diff.loc[df_qm_diff['QM_DIFF'].notnull()]

    # remove the rows where QM_DIFF is 0
    df_qm_diff = df_qm_diff.loc[df_qm_diff['QM_DIFF'] != 0]

    # filter for data in this year
    df_qm_diff = df_qm_diff.loc[df_qm_diff['YEAR'] == CURR_YEAR]

    return df_qm_diff

# END SCRIPT