import logging
import pandas as pd

from constants import *
from clean_data import clean_data
from clean_projections import clean_projections
from duplicate_df_for_shared_services import duplicate_df_for_shared_services

# START SCRIPT
def join_allocation_to_df(df, df_allocation):
    # function that joins the allocation data to the df
    # first, duplicate the df for the shared services

    # create a new column EXPENSE_BUCKET_2
    df['EXPENSE_BUCKET_2'] = df['EXPENSE_BUCKET']
    df.loc[((df['EXPENSE_BUCKET']=='FTE') | (df['EXPENSE_BUCKET']=='OPEN_ROLES')), 'EXPENSE_BUCKET_2'] = 'FTE_AND_OPEN_ROLES'

    # if the PROJ_ACT column is PROJECTION and the EXPENSE_BUCKET_2 column is FTE_AND_OPEN_ROLES,
    # use the function column instead of the Vendor column to calculate df_sum
    if df.loc[(df['PROJ_ACT']=='PROJECTION') & (df['EXPENSE_BUCKET_2']=='FTE_AND_OPEN_ROLES')].shape[0] > 0:
        df_sum = df.groupby(['EXPENSE_BUCKET_2', 'Function', 'YEAR'])['AMOUNT'].sum().reset_index()
        # rename the Function column to Vendor
        df_sum.rename(columns={'Function': 'Vendor'}, inplace=True)
    else:
        df_sum = df.groupby(['EXPENSE_BUCKET_2', 'Vendor', 'YEAR'])['AMOUNT'].sum().reset_index()

    df = duplicate_df_for_shared_services(df)

    # filter df_allocation to remove rows where the ALLOCATION_KEY is null or the ALLOCATION is null or the ALLOCATION is 0
    df_allocation = df_allocation.loc[~df_allocation['ALLOCATION_KEY'].isnull()]
    df_allocation = df_allocation.loc[~df_allocation['ALLOCATION'].isnull()]
    df_allocation = df_allocation.loc[df_allocation['ALLOCATION'] != 0]    
    
    df = df.merge(df_allocation, how='left', left_on='ALLOCATION_KEY', right_on='ALLOCATION_KEY')
    df['ALLOCATION'] = df['ALLOCATION'].fillna(0).replace('', 0)
    # if the ALLO_TYPE is NOT SHARED SERVICES, then the ALLOCATION should be 1
    df.loc[(df['ALLO_TYPE']=='NOT SHARED SERVICES'), 'ALLOCATION'] = 1
    # if the PROJ_ACT is ACTUAL and the EXPENSE_BUCKET_2 is FTE_AND_OPEN_ROLES, then the ALLOCATION should be 1
    df.loc[(df['PROJ_ACT']=='ACTUAL') & (df['EXPENSE_BUCKET_2']=='FTE_AND_OPEN_ROLES'), 'ALLOCATION'] = 1

    # if there are rows where Vendor is "# NO VENDOR" and the ALLOCATION is 0,
    # then replace the ALLOCATION with .5 for CARE and CONNECT
    # print the number of rows where Vendor is "# NO VENDOR" and the ALLOCATION is 0
    logging.debug("number of rows where Vendor is # NO VENDOR and the ALLOCATION is 0: " + str(df.loc[(df['Vendor']=='# NO VENDOR') & (df['ALLOCATION']==0)].shape[0]))
    # print the number of rows where ALLOCATION is 0
    logging.debug("number of rows where ALLOCATION is 0: " + str(df.loc[df['ALLOCATION']==0].shape[0]))
    logging.debug("allocating .5 to # NO VENDOR for CARE and CONNECT")
    # print the number of rows where Vendor is "# NO VENDOR" and the ALLOCATION is 0 and the SOURCE is not "FTE_AND_OPEN_ROLES"
    logging.debug("number of rows where Vendor is # NO VENDOR and the ALLOCATION is 0 and the SOURCE is not FTE_AND_OPEN_ROLES: " + str(df.loc[(df['Vendor']=='# NO VENDOR') & (df['ALLOCATION']==0) & (df['EXPENSE_BUCKET_2']!='FTE_AND_OPEN_ROLES')].shape[0]))
    df.loc[(df['Vendor']=='# NO VENDOR') & (df['ALLOCATION']==0) & (df['BU']=='CARE') & (df['EXPENSE_BUCKET_2']!='FTE_AND_OPEN_ROLES'), 'ALLOCATION'] = .5
    df.loc[(df['Vendor']=='# NO VENDOR') & (df['ALLOCATION']==0) & (df['BU']=='CONNECT') & (df['EXPENSE_BUCKET_2']!='FTE_AND_OPEN_ROLES'), 'ALLOCATION'] = .5
    logging.debug("after adjusting # NO VENDOR, the number of rows where ALLOCATION is 0 is: " + str(df.loc[df['ALLOCATION']==0].shape[0]))

    df['ALLOCATION'] = df['ALLOCATION'].astype(float)
    df['ALLOCATED_AMOUNT'] = df['AMOUNT'] * df['ALLOCATION']

    # if Amount is null, then fill it with 0
    df['AMOUNT'] = df['AMOUNT'].fillna(0)
    # if Allocated Amount is null, then fill it with 0
    df['ALLOCATED_AMOUNT'] = df['ALLOCATED_AMOUNT'].fillna(0)

    # if Amount is not 0 then Allocated Amount should not be 0
    # This happens because the ALLOCATION is 0
    # Replace the ALLOCATION for these

    # are there rows where AMOUNT is not null and the AMOUNT is not 0
    # and ALLOCATED_AMOUNT is null or 0?
    df_missing_spend = df.loc[(df['AMOUNT'] != 0) & ((df['ALLOCATED_AMOUNT'] == 0)) & ((df['PROJ_ACT'] == "ACTUAL"))]
    # print the unique values of BU
    logging.debug("The unique values of BU are: " + str(df_missing_spend['BU'].unique()))
    # filter out rows where BU is "NETWORK" or "INSIGHTS"
    df_missing_spend = df_missing_spend.loc[(df_missing_spend['BU'] != 'NETWORK') & (df_missing_spend['BU'] != 'INSIGHTS')]
    # print the unique values of BU
    logging.debug("The unique values of BU are: " + str(df_missing_spend['BU'].unique()))
    # filter out rows where Vendor is "# NO VENDOR"
    df_missing_spend = df_missing_spend.loc[df_missing_spend['Vendor'] != '# NO VENDOR']

    if df_missing_spend.shape[0] > 0:
        # print "before the fix" and give the total spend in df
        logging.debug("Before the fix, the total spend is: " + str(df['ALLOCATED_AMOUNT'].sum()))
        logging.debug("There are rows where spend is missing:")
        logging.debug(df_missing_spend.to_string())
        # print the count of unique BUs for each Vendor and EXPENSE_BUCKET_2 where AMOUNT is not null and the AMOUNT is not 0
        logging.debug("The count of unique BUs for each Vendor and EXPENSE_BUCKET_2 where AMOUNT is not null and the AMOUNT is not 0:")
        logging.debug(df_missing_spend.groupby(['Vendor', 'EXPENSE_BUCKET_2'])['BU'].nunique().to_string())
        # divide 1 by the count of unique BUs for each Vendor and EXPENSE_BUCKET_2 where AMOUNT is not null and the AMOUNT is not 0
        # and use that as the ALLOCATION
        df_missing_spend['ALLOCATION'] = 1 / df_missing_spend.groupby(['Vendor', 'EXPENSE_BUCKET_2'])['BU'].transform('nunique')
        # recalculate the ALLOCATED_AMOUNT
        df_missing_spend['ALLOCATED_AMOUNT'] = df_missing_spend['AMOUNT'] * df_missing_spend['ALLOCATION']
        # replace the ALLOCATION and ALLOCATED_AMOUNT in the original df
        df.loc[df_missing_spend.index, 'ALLOCATION'] = df_missing_spend['ALLOCATION']
        df.loc[df_missing_spend.index, 'ALLOCATED_AMOUNT'] = df_missing_spend['ALLOCATED_AMOUNT']
        # print "after the fix" and give the total spend in df
        logging.debug("After the fix, the total spend is: " + str(df['ALLOCATED_AMOUNT'].sum()))
        
    else:
        logging.debug("There are no rows with missing spend")

    # remove rows where the ALLOCATED_AMOUNT is null or 0
    df = df.loc[~df['ALLOCATED_AMOUNT'].isnull()]
    df = df.loc[df['ALLOCATED_AMOUNT'] != 0]
    logging.debug("PART 3 : The first 15 rows of df where the Vendor is Calendly LLC:")
    logging.debug(df.loc[df['Vendor']=='Calendly LLC'].head(100).to_string(index=False))
    # are there any rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 0?
    # print the BU, Vendor, EXPENSE_BUCKET_2, ALLO_TYPE, ALLOCATION, ALLOCATION_KEY, and ALLOCATED_AMOUNT for the first 15 rows
    if df.loc[(df['ALLO_TYPE']=='SHARED SERVICES') & (df['ALLOCATION']==0)].shape[0] > 0:
        logging.debug("The first 15 rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 0:")
        logging.debug(df.loc[(df['ALLO_TYPE']=='SHARED SERVICES') & (df['ALLOCATION']==0)].head(15))
    else:
        logging.debug("There are no rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 0")

        # are there any rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 1?
        # print the BU, Vendor, EXPENSE_BUCKET_2, ALLO_TYPE, ALLOCATION, ALLOCATION_KEY, and ALLOCATED_AMOUNT for the first 15 rows
        if df.loc[(df['ALLO_TYPE']=='SHARED SERVICES') & (df['ALLOCATION']==1)].shape[0] > 0:
            logging.debug("The first 15 rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 1:")
            logging.debug(df.loc[(df['ALLO_TYPE']=='SHARED SERVICES') & (df['ALLOCATION']==1)].head(15))
        else:
            logging.debug("There are no rows where ALLO_TYPE is SHARED SERVICES and the ALLOCATION is 1")

        # print the sum of ALLOCATED_AMOUNT for each EXPENSE_BUCKET_2
        logging.debug("The sum of ALLOCATED_AMOUNT for each EXPENSE_BUCKET_2:")
        logging.debug(df.groupby('EXPENSE_BUCKET_2')['ALLOCATED_AMOUNT'].sum().to_string())
    
    logging.debug("PART 4 : The first 15 rows of df where the Vendor is Calendly LLC:")
    logging.debug(df.loc[df['Vendor']=='Calendly LLC'].head(100).to_string(index=False))
    # print the head of df
    logging.debug("The values after allocating")
    # if the EXPENSE_BUCKET_2 has one unique value and that value is "FTE AND "
    if df.loc[(df['PROJ_ACT']=='PROJECTION') & (df['EXPENSE_BUCKET_2']=='FTE_AND_OPEN_ROLES')].shape[0] > 0:
        df_sum_2 = df.groupby(['EXPENSE_BUCKET_2', 'Function', 'YEAR'])['ALLOCATED_AMOUNT'].sum().reset_index()
        # rename the columns
        df_sum_2.rename(columns={'Function': 'Vendor'}, inplace=True)
    else:
        df_sum_2 = df.groupby(['EXPENSE_BUCKET_2', 'Vendor', 'YEAR'])['ALLOCATED_AMOUNT'].sum().reset_index()

    # get sum of AMOUNT for each EXPENSE_BUCKET_2 and Vendor and join to df_sum from earlier
    try:
        # merge df_sum_2 with df_sum
        df_sum = pd.merge(df_sum, df_sum_2, how='outer', on=['EXPENSE_BUCKET_2', 'YEAR', 'Vendor'])

        df_sum['ALLOCATED_AMOUNT'] = df_sum['ALLOCATED_AMOUNT'].fillna(0)
        df_sum['ALLOCATED_AMOUNT'] = df_sum['ALLOCATED_AMOUNT'].astype(float)
        df_sum['AMOUNT'] = df_sum['AMOUNT'].astype(float)
        df_sum['DIFFERENCE'] = df_sum['AMOUNT'] - df_sum['ALLOCATED_AMOUNT']
        df_sum['PERCENT_DIFFERENCE'] = df_sum['DIFFERENCE'] / df_sum['AMOUNT']
        df_sum['PERCENT_DIFFERENCE'] = df_sum['PERCENT_DIFFERENCE'].fillna(0)
        df_sum['PERCENT_DIFFERENCE'] = df_sum['PERCENT_DIFFERENCE'].astype(float)
        df_sum['PERCENT_DIFFERENCE'] = df_sum['PERCENT_DIFFERENCE'] * 100
        df_sum['PERCENT_DIFFERENCE'] = df_sum['PERCENT_DIFFERENCE'].apply(lambda x: round(x, 4))
        df_sum['PERCENT_DIFFERENCE'] = df_sum['PERCENT_DIFFERENCE'].apply(lambda x: str(x) + '%')

        # filter for rows where the absolute value of PERCENT_DIFFERENCE is greater than .1
        df_sum = df_sum.loc[abs(df_sum['PERCENT_DIFFERENCE'].astype(float)) > .1]
        # sort by the PERCENT_DIFFERENCE column
        df_sum = df_sum.sort_values(by='PERCENT_DIFFERENCE', ascending=False)

        # if there are any rows in df_sum
        if df_sum.shape[0] > 0:
            # print the first 15 rows of df_sum
            logging.debug("The first 15 rows where pre-allocation and post-allocation don't match:")
            logging.debug(df_sum.head(15).to_string())
        else:
            logging.debug("Pre-allocation and post-allocation match for all rows.")
    
    except:
        logging.debug("There was an error merging the pre and post allocation dataframes.")

    # filter for rows where the ALLO_TYPE is SHARED SERVICES
    df_checking = df.loc[df['ALLO_TYPE']=='SHARED SERVICES']

    # what is the sum of ALLOCATED_AMOUNT for each Vendor, BU, Quarter, Year, and EXPENSE_BUCKET_2?
    logging.debug("The sum of ALLOCATION for each Vendor, BU, Quarter, Year, and EXPENSE_BUCKET_2:")
    df_allo_total = df_checking.groupby(['Vendor', 'QUARTER', 'YEAR', 'EXPENSE_BUCKET_2'])['ALLOCATION'].sum()
    logging.debug("The number of rows for each Vendor, Quarter, Year, and EXPENSE_BUCKET_2:")
    df_rows_total = df_checking.groupby(['Vendor', 'QUARTER', 'YEAR', 'EXPENSE_BUCKET_2']).size()
    # how many unique BU values are there for each Vendor, Quarter, Year, and EXPENSE_BUCKET_2?
    df_bu_total = df_checking.groupby(['Vendor', 'QUARTER', 'YEAR', 'EXPENSE_BUCKET_2'])['BU'].nunique()

    df_allo_check = df_allo_total / df_rows_total
    df_allo_check = df_allo_check.reset_index()
    df_allo_check = df_allo_check.merge(df_bu_total, how='left', left_on=['Vendor', 'QUARTER', 'YEAR', 'EXPENSE_BUCKET_2'], right_on=['Vendor', 'QUARTER', 'YEAR', 'EXPENSE_BUCKET_2'])
    df_allo_check = df_allo_check.rename(columns={'BU': 'BU_COUNT'})
    df_allo_check = df_allo_check.loc[df_allo_check['BU_COUNT']!=2]
    
    # what is the sum of ALLOCATED_AMOUNT for each Vendor, BU, Quarter, Year, and EXPENSE_BUCKET_2 divided by the number of rows for each Vendor, Quarter, Year, and EXPENSE_BUCKET_2?
    logging.debug("The sum of ALLOCATION for each Vendor, BU, Quarter, Year, and EXPENSE_BUCKET_2 divided by the number of rows for each Vendor, Quarter, Year, and EXPENSE_BUCKET_2:")
    logging.debug(df_allo_check.to_string())

    return df

# END SCRIPT