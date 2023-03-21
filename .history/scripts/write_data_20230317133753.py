# START SCRIPT
def write_data(df, RUNNING_IN_DOMO):
    if RUNNING_IN_DOMO:
        write_dataframe(df)
    else:
        df.to_csv("data/output/Output.csv")
# END SCRIPT