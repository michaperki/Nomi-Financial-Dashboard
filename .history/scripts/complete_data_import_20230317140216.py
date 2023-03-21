from print_columns import print_columns

# START SCRIPT
def complete_data_import(df):
    # This function completes the data import
    # It prints some information about the data frame
    # and stores some information about the data frame
    # to be used for validation later
    # if the data frame has a _FILE_NAME_ column, print the first value
    if '_FILE_NAME_' in df.columns:
        print("the file name is " + df['_FILE_NAME_'].iloc[0])
    else:
        print("the file name is not in the data frame, probably the NAME MAP")
    
    # print the dimensions of the data frame
    print("the dimensions of the data frame are " + str(df.shape[0]) + " rows and " + str(df.shape[1]) + " columns")
    print_columns(df)
# END SCRIPT