from constants import *
import logging
import pandas as pd
from clean_actuals import clean_actuals
from clean_data import clean_data
from dt_clean_software_for_deltas import clean_software_for_deltas
from dt_clean_ftc_for_deltas import clean_ftc_for_deltas
from dt_clean_pro_serv_for_deltas import clean_pro_serv_for_deltas
from dt_clean_fte_for_deltas import clean_fte_for_deltas
from format_final_df import format_final_df


# START SCRIPT
def calculate_deltas(df_fte, df_ftc, df_pro_serv, df_software, df_actuals, ACTUAL_FILE_DATE, df_name_map):

    models = [df_software, df_ftc, df_pro_serv, df_fte]
    df_actuals = clean_actuals(df_actuals, ACTUAL_FILE_DATE, df_name_map)
    df_actuals = df_actuals.loc[
        (df_actuals['EXPENSE_BUCKET'] == "SOFTWARE") | 
        (df_actuals['EXPENSE_BUCKET'] == "FTC") |
        (df_actuals['EXPENSE_BUCKET'] == "PRO_SERV") |
        (df_actuals['EXPENSE_BUCKET'] == "FTE")
    ]
    df_software['Paid by Credit Card (Y/N)'].fillna('N', inplace=True)
    df_software_paid_by_cc = df_software.loc[df_software['Paid by Credit Card (Y/N)'] == "Y"]
    df_software_paid_by_cc = df_software_paid_by_cc[['Vendor', 'Paid by Credit Card (Y/N)']]
    df_software_paid_by_cc = df_software_paid_by_cc.drop_duplicates()
    df_software_paid_by_cc = df_software_paid_by_cc.rename(columns={"Paid by Credit Card (Y/N)": "PAID_BY_CC"})
    df_software_paid_by_cc['PAID_BY_CC'] = 1
    
    # this will convert Inc to Inc. 
    df_software_paid_by_cc = clean_data(df_software_paid_by_cc)

    # convert the vendor names to upper case
    df_software_paid_by_cc['Vendor'] = df_software_paid_by_cc['Vendor'].str.upper()
    df_software = clean_software_for_deltas(df_software)
    df_ftc = clean_ftc_for_deltas(df_ftc)
    df_pro_serv = clean_pro_serv_for_deltas(df_pro_serv)
    df_fte = clean_fte_for_deltas(df_fte)
    
    df = pd.concat([df_ftc, df_software, df_pro_serv, df_fte], ignore_index=True)
    df_formatted_projections = pd.melt(
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
    
    df_formatted_projections['MONTH'] = df_formatted_projections['MONTH'].replace(DICT_W_BONUS)
    df_formatted_projections[['MONTH','SAL_BONUS']] = df_formatted_projections['MONTH'].str.split("|", expand=True)

    # Again, setting year back TEMPORARILY
    df_formatted_projections['YEAR'] = CURR_YEAR
    df_formatted_projections['Type'] = "# NO TYPE"

    df_formatted_projections = df_formatted_projections.loc[(df_formatted_projections['AMOUNT'] != 0) & (df_formatted_projections['AMOUNT'].notnull())]
    df_formatted_projections['PROJ_ACT'] = 'PROJECTION'
    df_formatted_projections['QUARTER'] = pd.to_datetime(df_formatted_projections['MONTH'].values, format='%m').astype('period[Q]').astype(str).str[-1:]

    # Filter actuals columns
    df_formatted_actuals = df_actuals[['Vendor', 'BU', 'IS Grouping', 'Engineering', 'Function', 'Project', 'Contact', 'PROJ_ACT', 'MONTH', 'AMOUNT', 'QUARTER', 'YEAR', 'Type', 'CASH_VIEW', 'EXPENSE_BUCKET', 'SAL_BONUS']]
    df_formatted_actuals = df_formatted_actuals.groupby(['Vendor', 'BU', 'IS Grouping', 'Engineering', 'Function', 'Project', 'Contact', 'PROJ_ACT', 'MONTH', 'QUARTER', 'YEAR', 'Type', 'CASH_VIEW', 'EXPENSE_BUCKET', 'SAL_BONUS']).sum()
    df_formatted_actuals.reset_index(inplace=True)
    df = pd.concat((df_formatted_projections, df_formatted_actuals), ignore_index=True)
    df['EXPENSE_BUCKET_2'] = df['EXPENSE_BUCKET']
    df['ALLOCATION'] = 1
    df = format_final_df(df, ACTUAL_FILE_DATE)

    return df
# END SCRIPT