from constants import *
import logging
import pandas as pd


# START SCRIPT
def get_latest_data_for_each_quarter(df):
    # create an empty list
    quarter_list = []

    # for each unique value in Y-budget
    for year in df["Y-budget"].unique():
        dfy = df[df['Y-budget'] == year]

        # for each Q-budget, print the count of unique _BATCH_ID_ values
        for quarter in dfy["Q-budget"].unique():
            # filter the data frame to only include rows where Q-budget is equal to the quarter
            # and print the count of unique _BATCH_ID_ values
            df2 = dfy[dfy['Q-budget'] == quarter]

            if df2[df2['Q-budget'] == quarter]['_BATCH_ID_'].nunique() != 1:
                print("...multiple batch_ids detected for the same quarter")
                # get the greatest batch ID
                max_batch_id = df2[df2['Q-budget'] == quarter]['_BATCH_ID_'].max()
                # add a boolean column called "Q-curr" that is 1 if the batch ID is equal to the greatest batch ID
                # and 0 otherwise
                df2['Q-curr'] = np.where(df2['_BATCH_ID_'] == max_batch_id, 1, 0)

            else:
                # add a boolean column called "Q-curr" that is 1
                df2['Q-curr'] = 1

            # append the data frame to the list
            quarter_list.append(df2)

    # concatenate the list of data frames into one data frame
    df = pd.concat(quarter_list, ignore_index=True)

    # filter the data frame to only include rows where Q-curr is equal to 1
    df = df[df['Q-curr'] == 1]

    # drop the Q-curr column
    df = df.drop(columns=['Q-curr'])

    return df
# END SCRIPT