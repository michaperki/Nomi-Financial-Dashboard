from constants import *
import logging
from clean_data import clean_data
import pandas as pd
from remove_string_from_column import remove_string_from_column
from qt_get_quarters_from_file_name import get_quarters_from_file_name
from qt_get_latest_data_for_each_quarter import get_latest_data_for_each_quarter
from qt_move_actuals_forward_one_quarter import move_actuals_forward_one_quarter
from qt_main_function_no_actuals import main_function_no_actuals
from qt_main_function import main_function




# START SCRIPT
def format_quarterly_data(df_fte, df_orm, df_ftc, df_pro_serv, df_software, df_actuals, df_fte_allocation, df_ftc_allocation, df_pro_serv_allocation, df_software_allocation, df_name_map):

    # create a list of data frames
    df_list = [df_fte, df_orm, df_ftc, df_pro_serv, df_software, df_actuals]
    projections_list = [df_fte, df_orm, df_ftc, df_pro_serv, df_software]

    # create empty lists
    df_quarter_list = []
    df_annual_list = []

    # create a set of the unique values in the Y-budget column for all dataframes
    y_budget_set = set()

    # for each data frame in the list
    # get the quarter and year from the file name
    for df in projections_list:
        df = get_quarters_from_file_name(df)
        df = get_latest_data_for_each_quarter(df)
        y_budget_set.update(df["Y-budget"].unique())

    # move the actuals back one quarter
    df_actuals = get_quarters_from_file_name(df_actuals)
    df_actuals = get_latest_data_for_each_quarter(df_actuals)
    df_actuals = move_actuals_forward_one_quarter(df_actuals)
    y_budget_set.update(df_actuals["Y-budget"].unique())

    # These logging.debug statements are for debugging purposes only
    # logging.debug("unique values in df_actuals Y-budget column: ", df_actuals["Y-budget"].unique())
    # logging.debug("unique values in df_actuals Q-budget column: ", df_actuals["Q-budget"].unique())

    df_list = [df_fte, df_orm, df_ftc, df_pro_serv, df_software]

    # for each year in the set
    for year in y_budget_set:
        # This logging.debug statement is for debugging purposes only
        # logging.debug("Year: ", year)

        # define a counter to keep track of the number of quarters in each data frame
        q1_counter = 0
        q2_counter = 0
        q3_counter = 0
        q4_counter = 0
        # create a list of the counters
        counter_list = [q1_counter, q2_counter, q3_counter, q4_counter]

        q2_actuals_bool = False
        q3_actuals_bool = False
        q4_actuals_bool = False

        # for each quarter
        for quarter in range(1,5):
            # This logging.debug statement is for debugging purposes only
            # logging.debug("Quarter: ", quarter)

            df_actuals_2 = df_actuals[(df_actuals['Y-budget'] == year) & (df_actuals['Q-budget'] == quarter)]

            # for each data frame in the list
            for df in df_list:
                # filter the data frame to only include rows where Y-budget is equal to the year
                # and Q-budget is equal to the quarter
                df2 = df[(df['Y-budget'] == year) & (df['Q-budget'] == quarter)]

                # if the data frame is empty
                if df2.empty:
                    # logging.debug("...no data for ", year, "Q", quarter)
                    # if the quarter is 1
                    pass
                elif quarter == 1:
                    # increment the counter
                    q1_counter += 1
                    logging.debug("q1_counter: " + str(q1_counter))
                # if the quarter is 2
                elif quarter == 2:
                    # increment the counter
                    q2_counter += 1
                    logging.debug("q2_counter: " + str(q2_counter))
                    if not df_actuals_2.empty:
                        q2_actuals_bool = True
                        logging.debug("q2_actuals_bool: " + str(q2_actuals_bool))
                # if the quarter is 3
                elif quarter == 3:
                    # increment the counter
                    q3_counter += 1
                    logging.debug("q3_counter: " + str(q3_counter))
                    if not df_actuals_2.empty:
                        q3_actuals_bool = True
                        logging.debug("q3_actuals_bool: " + str(q3_actuals_bool))
                # if the quarter is 4
                elif quarter == 4:
                    # increment the counter
                    q4_counter += 1
                    logging.debug("q4_counter: " + str(q4_counter))
                    if not df_actuals_2.empty:
                        q4_actuals_bool = True
                        logging.debug("q4_actuals_bool: " + str(q4_actuals_bool))

        # if q1_counter is greater than or equal to 5, then run the main function on the data frames filtered for Q1 Data
        # NOTE Q1 uses 5 rather than 6 because there is no actuals data for Q1
        if q1_counter >= 5:
            logging.debug("Q1 Data is ready to be processed")

            # filter the data frames for Q1 Data
            df_software_q1 = df_software[df_software['Q-budget'] == 1]
            df_fte_q1 = df_fte[df_fte['Q-budget'] == 1]
            df_orm_q1 = df_orm[df_orm['Q-budget'] == 1]
            df_ftc_q1 = df_ftc[df_ftc['Q-budget'] == 1]
            df_pro_serv_q1 = df_pro_serv[df_pro_serv['Q-budget'] == 1]

            ## Need to run a version of main_function without actuals data

            df_q1 = main_function_no_actuals(
                df_software             = df_software_q1,
                df_software_allocation  = df_software_allocation,
                df_fte                  = df_fte_q1,
                df_fte_allocation       = df_fte_allocation,
                df_open_roles                  = df_orm_q1,
                df_ftc                  = df_ftc_q1,
                df_ftc_allocation       = df_ftc_allocation,
                df_pro_serv             = df_pro_serv_q1,
                df_pro_serv_allocation  = df_pro_serv_allocation,
                df_name_map=df_name_map,

                )

            # add a constant column called "Q-budget" that is equal to 1
            df_q1['Q-budget'] = 1

            # append the data frame to the list
            df_quarter_list.append(df_q1)

        # if q2_counter is greater than or equal to 6, then run the main function on the data frames filtered for Q2 Data
        if q2_counter >= 5 and q2_actuals_bool == True:
            logging.debug("Q2 Data is ready to be processed")

            # filter the data frames for Q2 Data
            df_software_q2 = df_software[df_software['Q-budget'] == 2]
            df_fte_q2 = df_fte[df_fte['Q-budget'] == 2]
            df_orm_q2 = df_orm[df_orm['Q-budget'] == 2]
            df_ftc_q2 = df_ftc[df_ftc['Q-budget'] == 2]
            df_pro_serv_q2 = df_pro_serv[df_pro_serv['Q-budget'] == 2]
            df_actuals_q2 = df_actuals[df_actuals['Q-budget'] == 2]

            df_q2 = main_function(
                df_software             = df_software_q2,
                df_software_allocation  = df_software_allocation,
                df_fte                  = df_fte_q2,
                df_fte_allocation       = df_fte_allocation,
                df_open_roles           = df_orm_q2,
                df_ftc                  = df_ftc_q2,
                df_ftc_allocation       = df_ftc_allocation,
                df_pro_serv             = df_pro_serv_q2,
                df_pro_serv_allocation  = df_pro_serv_allocation,
                df_name_map             = df_name_map,
            )

            # add a constant column called "Q-budget" that is equal to 2
            df_q2['Q-budget'] = 2

            # append the data frame to the list
            df_quarter_list.append(df_q2)

        # if q3_counter is greater than or equal to 6, then run the main function on the data frames filtered for Q3 Data
        if q3_counter >= 5 and q3_actuals_bool == True:
            logging.debug("Q3 Data is ready to be processed")

            # filter the data frames for Q3 Data
            df_software_q3 = df_software[df_software['Q-budget'] == 3]
            df_fte_q3 = df_fte[df_fte['Q-budget'] == 3]
            df_orm_q3 = df_orm[df_orm['Q-budget'] == 3]
            df_ftc_q3 = df_ftc[df_ftc['Q-budget'] == 3]
            df_pro_serv_q3 = df_pro_serv[df_pro_serv['Q-budget'] == 3]
            df_actuals_q3 = df_actuals[df_actuals['Q-budget'] == 3]

            df_q3 = main_function(
                df_software             = df_software_q3,
                df_software_allocation  = df_software_allocation,
                df_fte                  = df_fte_q3,
                df_fte_allocation       = df_fte_allocation,
                df_open_roles           = df_orm_q3,
                df_ftc                  = df_ftc_q3,
                df_ftc_allocation       = df_ftc_allocation,
                df_pro_serv             = df_pro_serv_q3,
                df_pro_serv_allocation  = df_pro_serv_allocation,
                df_name_map             = df_name_map
            )

            # add a constant column called "Q-budget" that is equal to 3
            df_q3['Q-budget'] = 3

            # append the data frame to the list
            df_quarter_list.append(df_q3)

        # if q4_counter is greater than or equal to 6, then run the main function on the data frames filtered for Q4 Data
        if q4_counter >= 5 and q4_actuals_bool == True:
            logging.debug("Q4 Data is ready to be processed")

            # filter the data frames for Q4 Data
            df_software_q4 = df_software[df_software['Q-budget'] == 4]
            df_fte_q4 = df_fte[df_fte['Q-budget'] == 4]
            df_orm_q4 = df_orm[df_orm['Q-budget'] == 4]
            df_ftc_q4 = df_ftc[df_ftc['Q-budget'] == 4]
            df_pro_serv_q4 = df_pro_serv[df_pro_serv['Q-budget'] == 4]
            df_actuals_q4 = df_actuals[df_actuals['Q-budget'] == 4]

            df_q4 = main_function(
                df_software             = df_software_q4,
                df_software_allocation  = df_software_allocation,
                df_fte                  = df_fte_q4,
                df_fte_allocation       = df_fte_allocation,
                df_open_roles           = df_orm_q4,
                df_ftc                  = df_ftc_q4,
                df_ftc_allocation       = df_ftc_allocation,
                df_pro_serv             = df_pro_serv_q4,
                df_pro_serv_allocation  = df_pro_serv_allocation,
                df_name_map             = df_name_map
            )

            # add a constant column called "Q-budget" that is equal to 4
            df_q4['Q-budget'] = 4

            # append the data frame to the list
            df_quarter_list.append(df_q4)

        # logging.debug the number of data frames in the list
        logging.debug("Number of data frames in the list: " + str(len(df_quarter_list)))

        # if the number of data frames in the list is greater than 0, then join the data frames together
        if len(df_quarter_list) > 0:
            # join the data frames together
            df_quarterly = pd.concat(df_quarter_list)
            df_quarterly["Y-budget"] = year

        else:
            df_quarterly = pd.DataFrame()

        # append the data frame to the list
        df_annual_list.append(df_quarterly)

    # join the data frames together
    df_quarterly = pd.concat(df_annual_list)

    # return the data frame
    return df_quarterly
# END SCRIPT