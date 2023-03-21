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
from dt_calculate_top_five import calculate_top_five


# START SCRIPT
def calculate_deltas(df_fte, df_ftc, df_pro_serv, df_software, df_actuals, ACTUAL_FILE_DATE, df_name_map):

    all_data = [df_software, df_ftc, df_pro_serv, df_fte, df_actuals]
    for df in all_data:
        df = df.copy(deep=True)
        
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

    # convert ACTUAL_FILE_DATE to int
    ACTUAL_FILE_DATE = int(ACTUAL_FILE_DATE)

    # TEMPORARILY changed CURR_YEAR to CURR_YEAR - 1
    df = df.loc[(df['YEAR']==CURR_YEAR) & (df['MONTH'].astype(int) <= ACTUAL_FILE_DATE)]

    df['Vendor'].fillna("# NO VENDOR", inplace=True)
    df['SAL_BONUS'].fillna("-", inplace=True)

    df = calculate_top_five(df, "TOP_5")
    # split the data into two dataframes based on the CASH_VIEW column
    df_cash_view = df.loc[df['CASH_VIEW'] == 1]
    df_non_cash_view = df.loc[df['CASH_VIEW'] == 0]

    df = calculate_top_five(df_cash_view, "TOP_5_cash_view")

    # rejoin the two dataframes
    df = pd.concat([df, df_non_cash_view], ignore_index=True)

    df.fillna({'PROJECTION':0, 'ACTUAL':0, 'QUARTER':"ALL"}, inplace=True)
    df['DELTA_(P-A)'] = df['PROJECTION'] - df['ACTUAL']

    # here are all the vendors that are missing from the projection
    # use df_sum and find all the vendors that have ACTUAL > 0 and PROJECTION = 0
    # then use that list to find all the rows in df where the vendor is in that list
    # then set the MISSING_FROM_PROJ column to 1

    try:
        df['MISSING_FROM_PROJ'] = np.where(((df['ACTUAL']>0) & (df['PROJECTION']==0)), 1, 0)
    except:
        df['MISSING_FROM_PROJ'] = 0
    MISSING_FROM_PROJ_ARRAY = list(set(df.loc[df['MISSING_FROM_PROJ']==1, "Vendor"].values))

    df['ALOM_MISSING_FROM_PROJ'] = np.where((df["Vendor"].isin(MISSING_FROM_PROJ_ARRAY)), 1, 0) # At least one month missing (ALOM missing)

    try:
        df['ABSENT_FROM_PROJ'] = np.where(((df['ACTUAL']>0) & (df['PROJECTION']==0) & (df['MONTH']=="999")), 1, 0)
    except:
        df['ABSENT_FROM_PROJ'] = 0
    ABSENT_FROM_PROJ_ARRAY = list(set(df.loc[df['ABSENT_FROM_PROJ']==1, "Vendor"].values))
    df['ABSENT_FROM_PROJ'] = np.where((df["Vendor"].isin(ABSENT_FROM_PROJ_ARRAY)), 1, 0)


    try:
        df['MISSING_FROM_ACT'] = np.where(((df['ACTUAL']==0) & (df['PROJECTION']>0)), 1, 0)
    except:
        df['MISSING_FROM_ACT'] = 0
    MISSING_FROM_ACT_ARRAY = list(set(df.loc[df['MISSING_FROM_ACT']==1, "Vendor"].values))

    df['ALOM_MISSING_FROM_ACT'] = np.where((df["Vendor"].isin(MISSING_FROM_ACT_ARRAY)), 1, 0)

    try:
        df['ABSENT_FROM_ACT'] = np.where(((df['ACTUAL']==0) & (df['PROJECTION']>0) & (df['MONTH']=="999")), 1, 0)
    except:
        df['ABSENT_FROM_ACT'] = 0
    ABSENT_FROM_ACT_ARRAY = list(set(df.loc[df['ABSENT_FROM_ACT']==1, "Vendor"].values))
    df['ABSENT_FROM_ACT'] = np.where((df["Vendor"].isin(ABSENT_FROM_ACT_ARRAY)), 1, 0)

    df = df.round(decimals=3)

    df['LAST_THREE_MONTHS'] = (df['MONTH'].astype(int) > (ACTUAL_FILE_DATE-3)) & (df['MONTH'].astype(int) <= (ACTUAL_FILE_DATE))

    total_delta = df.loc[(df['MONTH']!="999"), 'DELTA_(P-A)'].sum()
    try:
        total_delta_as_currency = "${:,.2f}".format(total_delta)
    except:
        logging.debug("Error -- could not format total delta:  ", total_delta)
        total_delta_as_currency = 0
    logging.debug("Compiled Annual Delta: " + str(total_delta_as_currency))

    df = pd.melt(df, id_vars=[
        'YEAR', 'Vendor', 'BU', 'Function', 'IS Grouping', 'EXPENSE_BUCKET',
        'MONTH_NAME', 'MONTH', 'QUARTER', 'TOP_5', 'MISSING_FROM_PROJ',
        'MISSING_FROM_ACT', 'ALOM_MISSING_FROM_ACT', 'ALOM_MISSING_FROM_PROJ',
        'ABSENT_FROM_PROJ', 'ABSENT_FROM_ACT', 'LAST_THREE_MONTHS'
        ], value_vars=['ACTUAL', 'PROJECTION', 'DELTA_(P-A)'], var_name="CATEGORY", value_name="VALUE")

    logging.debug(" ~ Calculate_Delta function complete ~ ")
    cols = df.columns.tolist()
    # convert the columns to a string, then remove the brackets and single quotes
    cols_str = str(cols).replace("[", "").replace("]", "").replace("'", "")
    logging.debug("here are the columns of the delta dataframe: " + cols_str)
    df['MISSING_FROM_ACT'] = np.where(df['Vendor'].isin(df_software_paid_by_cc['Vendor']), 0, df['MISSING_FROM_ACT'])
    df['ALOM_MISSING_FROM_ACT'] = np.where(df['Vendor'].isin(df_software_paid_by_cc['Vendor']), 0, df['ALOM_MISSING_FROM_ACT'])
    df['ABSENT_FROM_ACT'] = np.where(df['Vendor'].isin(df_software_paid_by_cc['Vendor']), 0, df['ABSENT_FROM_ACT'])

    return df
# END SCRIPT