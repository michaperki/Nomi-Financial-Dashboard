from imports import *
from constants import *

# START SCRIPT

def format_headcounts(df):
    df = df.copy(deep=True)

    # print the number of rows where MONTH is 99
    logging.debug("Number of rows where MONTH is 99: " + str(len(df.loc[df['MONTH']=="99"])))

    df['ALLOCATED_AMOUNT'] = df['AMOUNT'] * df['ALLOCATION']
    # store the number of rows in the df
    df_len = len(df)
    df = df.loc[(df['ALLOCATED_AMOUNT']!=0) | (df['MONTH']=="99")]
    # if the number of rows in the df has changed, print a message
    if df_len != len(df):
        logging.debug("Removed rows with 0 allocated amount")
        logging.debug(str(df_len - len(df)) + " rows removed")
        # print rows remaining
        logging.debug(str(len(df)) + " rows remaining")

    df['BU'] = df['BU'].str.upper()
    df['Engineering'] = df['Engineering'].str.upper()
    df['Function'] = df['Function'].str.upper()

    df['EXPENSE_BUCKET'] = df['EXPENSE_BUCKET'].str.replace("_"," ")
    df['EXPENSE_BUCKET_2'] = df['EXPENSE_BUCKET_2'].str.replace("_"," ")
    df['MONTH_NAME'] = df['MONTH'].replace(MONTH_DICT)

    # Get today's month
    CURR_MONTH = datetime.datetime.now().strftime("%m")
    df['CURRENT'] = np.where(df['MONTH'] <= CURR_MONTH, 1, 0)

    # Get the last day of the current month as a datetime object
    CURR_MONTH_LAST_DAY = datetime.datetime.now().replace(day=calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1])

    # Add a PnL YtD Join columm where the CATEGORY is PNL MONTHLY and the Company Seniority Date is less than or equal to the last day of the current month and
    # the Termination Date is greater than or equal to the last day of the current month
    df['PnL_YTD_JOIN'] = np.where(
        (df['CATEGORY'] == 'PNL MONTHLY') &
        (df['Company Seniority Date'] <= CURR_MONTH_LAST_DAY) &
        (df['Company Seniority Date'].dt.year == CURR_YEAR) &

        (df['Termination Date'] >= CURR_MONTH_LAST_DAY) &
        (df['YEAR'] == CURR_YEAR),
        1, 0)

    # Add a PnL YtD Depart columm where the CATEGORY is PNL MONTHLY and the Termination Date is less than or equal to the last day of the current month
    df['PnL_YTD_DEPART'] = np.where(
        (df['CATEGORY'] == 'PNL MONTHLY') &
        (df['Termination Date'] <= CURR_MONTH_LAST_DAY) &
        (df['Termination Date'].dt.year == CURR_YEAR),
        1, 0)

    # add a YEAR column
    df['YEAR'] = CURR_YEAR

    return df
# END SCRIPT