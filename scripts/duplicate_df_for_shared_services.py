from imports import *

from constants import *

# START SCRIPT
def duplicate_df_for_shared_services(df):
    # if the dataframe is missing the Vendor column, add it
    if 'Vendor' not in df.columns:
        df['Vendor'] = "# NO VENDOR"

    df_not_shared = df.copy(deep=True)
    # filter for BU in NON_SHARED_BUs array

    df_not_shared = df_not_shared[df_not_shared['BU'].isin(NON_SHARED_BUs)]

    df_not_shared['ALLO_TYPE'] = 'NOT SHARED SERVICES'

    df_shared = df.copy(deep=True)

    # filter for BU not in NON_SHARED_BUs array
    df_shared = df_shared[~df_shared['BU'].isin(NON_SHARED_BUs)]

    df_shared['ALLO_TYPE'] = 'SHARED SERVICES'

    df_shared_care = df_shared.copy(deep=True)
    df_shared_connect = df_shared.copy(deep=True)
    df_shared_network = df_shared.copy(deep=True)
    df_shared_insights = df_shared.copy(deep=True)

    df_shared_care['BU'] = 'CARE'
    df_shared_connect['BU'] = 'CONNECT'
    df_shared_network['BU'] = 'NETWORK'
    df_shared_insights['BU'] = 'INSIGHTS'

    df_shared_dups = pd.concat((df_shared_care, df_shared_connect, df_shared_network, df_shared_insights), ignore_index=True)

    df_shared_dups['ALLOCATION_KEY'] = "Q" + df_shared_dups['QUARTER'].astype(str) + "|" + df_shared_dups['BU'].str.upper() + "|" + df_shared_dups['ALLO_TYPE'].str.upper() + "|" + df_shared_dups['Vendor'].str.upper() + "|" + df_shared_dups['YEAR'].astype(str) + "|" + df_shared_dups['EXPENSE_BUCKET']
    df_shared_dups.loc[(df_shared_dups['EXPENSE_BUCKET_2']=='FTE_AND_OPEN_ROLES'), 'ALLOCATION_KEY'] = "Q" + df_shared_dups['QUARTER'].astype(str) + "|" + df_shared_dups['BU'].str.upper() + "|" + df_shared_dups['ALLO_TYPE'].str.upper() + "|" + df_shared_dups['Function'].str.upper() + "|" + df_shared_dups['YEAR'].astype(str) + "|" + df_shared_dups['EXPENSE_BUCKET_2']

    # are there any rows where the ALLOCATION_KEY is null?
    if df_shared_dups.loc[df_shared_dups['ALLOCATION_KEY'].isnull()].shape[0] > 0:
        logging.debug("The first 15 rows where the ALLOCATION_KEY is null:")
        logging.debug(df_shared_dups.loc[df_shared_dups['ALLOCATION_KEY'].isnull()].head(15))

    df = pd.concat((df_not_shared, df_shared_dups), ignore_index=True)
    return df
# END SCRIPT