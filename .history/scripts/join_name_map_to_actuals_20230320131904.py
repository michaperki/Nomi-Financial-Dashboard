from constants import *
import logging
from clean_data import clean_data
from remove_string_from_column import remove_string_from_column
from format_cash_view import format_cash_view

# START SCRIPT
def join_name_map_to_actuals(df_actuals, df_name_map):
    # function that joins the name map to the actuals file

    df_actuals = df_actuals.copy(deep=True)
    df_name_map = df_name_map.copy(deep=True)

    # Rename Function to Function (New)
    df_name_map.rename(columns={'Function':'Function (New)'}, inplace=True)

    # Drop the columns that are not needed
    try:
        df_name_map.drop(['Expense Bucket'], axis=1, inplace=True)
    except KeyError:
        pass

    # if the Prepaid Vendor column is not "X", then it is null
    df_name_map.loc[df_name_map['Prepaid Vendor'] != 'X', 'Prepaid Vendor'] = np.nan

    # filter the data frame for rows where Prepaid Vendor is not null and get a list of the unique values in the Vendor column
    prepaid_vendor_list = df_name_map[df_name_map['Prepaid Vendor'].notnull()]['Entity (New)'].unique()
    print("Prepaid Vendors:", prepaid_vendor_list)

    df = df_actuals.merge(df_name_map, how='left', on='Entity').copy(deep=True)

    # For vendors missing from name map, use vendor name in actuals file
    df['Entity (New)'].fillna(df['Entity'], inplace=True)

    # Rows without vendor in the actuals file receive '# NO VENDOR'
    df['Entity (New)'].fillna("# NO VENDOR", inplace=True)

    # Fill the Function (New) column with the 'Function' column if it is blank for FTE rows
    df.loc[    (df['EXPENSE_BUCKET'] == 'FTE'), 'Function (New)'] = df['FTE Function 2']

    # Drop the columns that are not needed
    df.drop(['Entity', 'FTE Function 2', 'Function'], axis=1, inplace=True)

    # Rename Entity (New) to Vendor
    df.rename(columns={'Entity (New)':'Vendor', 'Function (New)':'Function', 'Amount':'AMOUNT'}, inplace=True)

    # For rows where the Vendor is in the prepaid_vendor_list, set the Prepaid Vendor column to 'X'
    df.loc[df['Vendor'].isin(prepaid_vendor_list), 'Prepaid Vendor'] = 'X'

    # Fill the NA values in the 'Function' column with 'NO FUNCTION'
    df['Function'].fillna('# NO FUNCTION', inplace=True)
    
    # Sort the data frame by Vendor and Function
    df.sort_values(by=['Vendor', 'Function'], inplace=True)

    return df
# END SCRIPT