from constants import *
import logging
from clean_data import clean_data
import pandas as pd

# START SCRIPT
def clean_allocation_sheet(df, name_map):
    # function that cleans the allocation sheet

    df = clean_data(df)

    # fill in missing values with 0
    df.fillna(0, inplace=True)
    df.rename(columns=ALLOCATION_COL_DICT, inplace=True)
    # get the column that contains the word "Key"
    key_col = [col for col in df.columns if 'Key' in col]
    # if the number of dashes in the key column is 1, then add a dash to the end of the string "-NA"
    df.loc[df[key_col[0]].str.count('-') == 1, key_col[0]] = df[key_col[0]] + '-NA'
    # split the key column into 3 columns
    df[['BU','Vendor', 'Other']] = df[key_col[0]].str.split("-", n=2, expand=True)
    id_col = 'Vendor'
    value_col_list = ['Care', 'Connect', 'Insights', 'Network']
    # get a list of columns that contain one of the strings in the value_col_list
    value_cols = [col for col in df.columns if any(x in col for x in value_col_list)]
    df = pd.melt(df,id_vars=[id_col,'SOURCE'],value_vars=value_cols,value_name='ALLOCATION',var_name='QUARTER_YEAR_BU')
    df[['QUARTER','YEAR','BU']] = df['QUARTER_YEAR_BU'].str.split('|', expand=True)

    df = df.merge(name_map, how='left', left_on='Vendor', right_on='Entity')
    df['Vendor'] = df['Entity (New)'].fillna(df['Vendor'])

    # if there are null values in the QUARTER, BU, Vendor, YEAR, or SOURCE columns, print the rows
    if df.loc[(df['QUARTER'].isnull()) | (df['BU'].isnull()) | (df['Vendor'].isnull()) | (df['YEAR'].isnull()) | (df['SOURCE'].isnull())].shape[0] > 0:
        logging.warning("There are null values in the QUARTER, BU, Vendor, YEAR, or SOURCE columns of the allocation sheet")

    df['ALLOCATION_KEY'] = df['QUARTER'] + "|" + df['BU'].str.upper() + "|SHARED SERVICES|" + df['Vendor'].str.upper() + "|" + df['YEAR'] + "|" + df['SOURCE']

    # get the sum of the ALLOCATION column for each QUARTER, YEAR, Vendor, and SOURCE
    df_allo_total_by_Q = df.groupby(['QUARTER','YEAR','Vendor','SOURCE']).agg({'ALLOCATION':'sum'}).reset_index()
    # filter the data frame for rows where the ALLOCATION column is not equal to 1
    df_allo_total_by_Q = df_allo_total_by_Q.loc[df_allo_total_by_Q['ALLOCATION'] != 1]
    # group by YEAR, Vendor, and SOURCE and ALLOCATION and aggregate the QUARTER column
    df_allo_total_by_Q_sum = df_allo_total_by_Q.groupby(['YEAR','Vendor','SOURCE','ALLOCATION']).agg({'QUARTER':', '.join}).reset_index()
    df_allo_total_missing = df_allo_total_by_Q_sum.loc[df_allo_total_by_Q_sum['ALLOCATION'] == 0]
    
    # if there are rows in the data frame, print the rows
    if df_allo_total_by_Q_sum.shape[0] > 0:
        ERROR_ARRAY.append(df_allo_total_by_Q_sum)
        logging.warning("Sum of the ALLOCATION column for each QUARTER, YEAR, Vendor, and SOURCE where ALLOCATION does not equal one")
        logging.warning(df_allo_total_by_Q_sum.to_string(index=False))
        # if there are rows in the data frame, print the rows
        if df_allo_total_missing.shape[0] > 0:
            # if there are rows in df where the SOURCE is "FTE_AND_OPEN_ROLES"
            if df[df['SOURCE'] == 'FTE_AND_OPEN_ROLES'].shape[0] > 0:
                # store the sum of the ALLOCATION column in df where the SOURCE is "FTE_AND_OPEN_ROLES" in a variable
                FTE_ALLO_SUM_PRIOR = df[df['SOURCE'] == 'FTE_AND_OPEN_ROLES']['ALLOCATION'].sum()
                # for each Vendor in df_allo_total_missing, assign .5 to the
                # ALLOCATION column in df where the Vendor, Quarter, and Year is the same and the BU is
                # "CARE" or "CONNECT" and the SOURCE is "FTE_AND_OPEN_ROLES"
                # if the BU is "INSIGHTS" or "NETWORK", assign .0 to the ALLOCATION column
                for index, row in df_allo_total_missing.iterrows():
                    df.loc[(df['Vendor'] == row['Vendor']) & (df['QUARTER'] == row['QUARTER']) & (df['YEAR'] == row['YEAR']) & (df['SOURCE'] == 'FTE_AND_OPEN_ROLES') & (df['BU'].isin(['CARE','CONNECT'])), 'ALLOCATION'] = .5
                    df.loc[(df['Vendor'] == row['Vendor']) & (df['QUARTER'] == row['QUARTER']) & (df['YEAR'] == row['YEAR']) & (df['SOURCE'] == 'FTE_AND_OPEN_ROLES') & (df['BU'].isin(['INSIGHTS','NETWORK'])), 'ALLOCATION'] = 0   
                # store the sum of the ALLOCATION column in df where the SOURCE is "FTE_AND_OPEN_ROLES" in a variable
                FTE_ALLO_SUM_AFTER = df[df['SOURCE'] == 'FTE_AND_OPEN_ROLES']['ALLOCATION'].sum()
                logging.warning("After assigning .5 to CARE/CONNECT and 0 to INSIGHTS/NETWORK, the sum of the ALLOCATION column for FTE_AND_OPEN_ROLES went from " + str(FTE_ALLO_SUM_PRIOR) + " to " + str(FTE_ALLO_SUM_AFTER))
                    
        else:
            print("No rows have an ALLOCATION value of 0")
            print("")
    else:
        print("All rows have an ALLOCATION value of 1")
        print("")

    df = df[['ALLOCATION_KEY','ALLOCATION']]
    df = df.loc[df['ALLOCATION'].notnull()]

    # Group by ALLOCATION_KEY and average the ALLOCATION
    df = df.groupby(['ALLOCATION_KEY']).mean().reset_index()

    return df
# END SCRIPT