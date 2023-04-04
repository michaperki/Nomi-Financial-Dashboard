from constants import *
import logging
import pandas as pd


# START SCRIPT
def calculate_qm_diff(df_monthly, df_quarterly):
    """
    Calculate the difference between the monthly and quarterly allocated amounts for the current year.

    Args:
        df_monthly (pandas.DataFrame): DataFrame containing the monthly allocated amounts.
        df_quarterly (pandas.DataFrame): DataFrame containing the quarterly allocated amounts.

    Returns:
        pandas.DataFrame: DataFrame containing the difference between the monthly and quarterly allocated amounts for the current year.

    """
    
    # common columns array
    common_columns = ['YEAR', 'QUARTER', 'MONTH', 'MONTH_NAME', 'Vendor', 'BU', 'Function', 'SAL_BONUS', 'IS Grouping', 'EXPENSE_BUCKET', 'ALLO_TYPE']

    # Filter df_monthly for 'YEAR' == 2023 and 'CURRENT' == 1
    df_monthly = df_monthly[(df_monthly['YEAR'] == CURR_YEAR) & (df_monthly['CURRENT'] == '1')]

    # Filter the columns for df_monthly and df_quarterly
    df_monthly_filtered = df_monthly[common_columns+['CURRENT', 'ALLOCATED_AMOUNT']]
    df_quarterly_filtered = df_quarterly[common_columns+['ALLOCATED_AMOUNT']]

    # Group by the common columns and sum the ALLOCATED_AMOUNT column for both data frames
    df_monthly_filtered = df_monthly_filtered.groupby(common_columns)['ALLOCATED_AMOUNT'].sum()
    df_quarterly_filtered = df_quarterly_filtered.groupby(common_columns)['ALLOCATED_AMOUNT'].sum()

    # Join the two data frames on the common columns
    df_joined = pd.merge(df_monthly_filtered, df_quarterly_filtered, on=common_columns, how='outer')
    
    # Group the joined data frame by the common columns and sum the ALLOCATED_AMOUNT column
    df_summed = df_joined.groupby(common_columns)['ALLOCATED_AMOUNT_x', 'ALLOCATED_AMOUNT_y'].sum()
    
    # Rename the summed columns and reset the index
    df_summed = df_summed.rename(columns={'ALLOCATED_AMOUNT_x': 'VALUE_MONTHLY', 'ALLOCATED_AMOUNT_y': 'VALUE_QUARTERLY'}).reset_index()

    df_qm_diff = df_summed.copy()
    
    # fill the missing values with 0
    df_qm_diff[['VALUE_MONTHLY', 'VALUE_QUARTERLY']] = df_qm_diff[['VALUE_MONTHLY', 'VALUE_QUARTERLY']].fillna(0)

    # calculate the difference    # calculate the difference
    df_qm_diff['QM_DIFF'] = df_qm_diff['VALUE_MONTHLY'] - df_qm_diff['VALUE_QUARTERLY']

    # if the absolute value of the QM_DIFF is less than 1, set it to 0
    df_qm_diff['QM_DIFF'] = df_qm_diff['QM_DIFF'].apply(lambda x: 0 if abs(x) < 1 else x)

    # filter for data in this year
    df_qm_diff = df_qm_diff.loc[df_qm_diff['YEAR'] == CURR_YEAR]
    
    return df_qm_diff

# END SCRIPT

