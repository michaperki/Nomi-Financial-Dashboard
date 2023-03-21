from constants import *
import logging
import pandas as pd

# START SCRIPT
def calculate_top_five(df, col_name, CASH_VIEW_ONLY=False):

    df_pivot = df.pivot_table(index=['YEAR', 'QUARTER', 'MONTH_NAME','MONTH','Vendor', 'BU', 'Function', 'IS Grouping','EXPENSE_BUCKET'], values='ALLOCATED_AMOUNT', columns='PROJ_ACT', aggfunc='sum')
    df_pivot.reset_index(inplace=True)

    df_sum = df_pivot.groupby(['YEAR','Vendor','EXPENSE_BUCKET'], as_index=False).sum()
    df_sum['MONTH_NAME']='ALL'
    df_sum['MONTH']="999"

    df_top_5 = df_sum.loc[(df_sum['Vendor']!="# NO VENDOR")].sort_values(by=['ACTUAL'], ascending=False).head(5)
    TOP_5_ARRAY = df_top_5["Vendor"].values
    # convert the array to a string, then remove the brackets and single quotes
    TOP_5_ARRAY_STR = str(TOP_5_ARRAY).replace("[", "").replace("]", "").replace("'", "")
    logging.debug("here is the top 5 array as a string: " + TOP_5_ARRAY_STR)
    df = df_sum.append(df_pivot)
    df[col_name] = 0
    for V in TOP_5_ARRAY:
        df[col_name] = np.where(df['Vendor']==V, 1, df[col_name])
    return df
# END SCRIPT