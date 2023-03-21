import logging

# START SCRIPT
def print_columns(df):
    # This function prints the columns of the data frame
    # This is useful for debugging

    # are there more than 10 columns?
    if len(df.columns) > 10:
        # log the columns
        logging.info("There are more than 10 columns...")
        # split the columns into groups of 10
        for i in range(0, len(df.columns), 10):
            # print the columns in each group as a string, separated by a comma
            logging.info("..." + ", ".join(df.columns[i:i+10]))
    else:
        logging.info(",".join(df.columns))
    print()
# END SCRIPT