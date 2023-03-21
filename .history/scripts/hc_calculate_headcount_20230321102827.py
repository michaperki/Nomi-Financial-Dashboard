from print_columns import print_columns
import logging
import pandas as pd
from constants import *
from clean_data import clean_data
from hc_clean_fte_for_hc import clean_fte_for_hc
from hc_clean_orm_for_hc import clean_orm_for_hc
from clean_allocation_sheet import clean_allocation_sheet
from hc_clean_headcounts import clean_headcounts
from join_allocation_to_df import join_allocation_to_df
from hc_format_headcounts import format_headcounts

# START SCRIPT
def calculate_headcount(df_fte, df_orm, df_fte_allocation):
    
    #Processing.py
    df_orm.rename(columns={
        'BU-FUNCTION KEY': 'BU-Function Key',
        'Start Date': 'Company Seniority Date',
        'Monthly Fully-Loaded':'PnL Monthly'},
                inplace=True)
    df_orm.columns = df_orm.columns.str.replace("Fully-Loaded", "PnL")

    # Add contants
    df_fte['Engineering'].fillna('NOT ENGINEERING', inplace=True)
    df_orm['Engineering'].fillna('NOT ENGINEERING', inplace=True)

    df_fte = clean_fte_for_hc(df_fte)
    df_orm = clean_orm_for_hc(df_orm)

    # Filter empty rows
    df_fte = df_fte.loc[(df_fte['BU'] != '') & (df_fte['BU'].notnull())]
    df_orm = df_orm.loc[(df_orm['BU'] != '') & (df_orm['BU'].notnull())]
    # df_orm = df_orm.loc[(df_orm['HC'] == 1)]

    df_orm['EXPENSE_BUCKET'] = 'OPEN_ROLES'
    df_fte['EXPENSE_BUCKET'] = 'FTE'

    df_fte_allocation['SOURCE'] = 'FTE_AND_OPEN_ROLES'
    df_fte_allocation['BU-Function Key'] = df_fte_allocation['BU-Function Key'] + "-na"

    df_fte_allocation = clean_allocation_sheet(df_fte_allocation, df_name_map)

    df = pd.concat((df_fte, df_orm))

    df = clean_headcounts(df)

    # split the df into two dfs, one with the FTE and one with the ORM
    df_fte = df.loc[df['EXPENSE_BUCKET'] == 'FTE']
    df_open_roles = df.loc[df['EXPENSE_BUCKET'] == 'OPEN_ROLES']

    df_fte = join_allocation_to_df(df_fte, df_fte_allocation)
    df_open_roles = join_allocation_to_df(df_open_roles, df_fte_allocation)

    df = pd.concat((df_fte, df_open_roles))

    df_final = format_headcounts(df)

    return df_final
# END SCRIPT