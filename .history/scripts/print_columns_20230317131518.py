# START SCRIPT
def print_columns(df):
    # This function prints the columns of the data frame
    # This is useful for debugging

    # are there more than 10 columns?
    if len(df.columns) > 10:
        print("the column names are...")
        # split the columns into groups of 10
        for i in range(0, len(df.columns), 10):
            # print the columns in each group as a string, separated by a comma
            print("..." + ", ".join(df.columns[i:i+10]))
    else:
        print(",".join(df.columns))
    print()
# END SCRIPT