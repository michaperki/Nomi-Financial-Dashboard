from imports import *

from constants import *

# START SCRIPT
def clean_headcounts(df):
    df = df.copy(deep=True)

    df['EXPENSE_BUCKET_2'] = "FTE_AND_OPEN_ROLES"

    df = df[ALL_HC_PROJ_COLS]

    df.loc[df['Termination Date'].isnull(), 'Termination Date'] = pd.Timestamp("01-01-2200")
    df.loc[df['Company Seniority Date'].isnull(), 'Company Seniority Date'] = pd.Timestamp("01-01-2200")
    df['Join_Month'] = pd.to_datetime(df["Company Seniority Date"], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m'))
    df['Depart_Month'] = pd.to_datetime(df["Termination Date"], format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m'))

    # convert company seniority date to datetime
    df['Company Seniority Date'] = pd.to_datetime(df['Company Seniority Date'], format='%Y-%m-%d')
    # convert termination date to datetime
    df['Termination Date'] = pd.to_datetime(df['Termination Date'], format='%Y-%m-%d')

    def compare_months(row, month):
        date_val = CURR_YEAR_STR + month + "01"
        date_val = pd.to_datetime(date_val)
        # go forward one month
        date_val = date_val + relativedelta(months=1)
        # go back one day to get last day of previous (ie current) month
        date_val = date_val - timedelta(days=1)
        return int((row['Company Seniority Date'] <= date_val) & ((row['Termination Date'] > date_val) | pd.isnull(row['Termination Date'])))

    for key in MONTH_DICT.keys():
        df[key+"|HC"] = df.apply(lambda row: compare_months(row, key), axis=1)

    def compare_join_months(row, month):
        date_val = CURR_YEAR_STR + "-" + month
        return int((row['Join_Month'] == date_val))

    for key in MONTH_DICT.keys():
        df[key+"|HC_JOIN"] = df.apply(lambda row: compare_join_months(row, key), axis=1)

    def compare_departure_months(row, month):
        date_val = CURR_YEAR_STR + "-" + month
        return int((row['Depart_Month'] == date_val))

    for key in MONTH_DICT.keys():
        df[key+"|HC_DEPART"] = df.apply(lambda row: compare_departure_months(row, key), axis=1)

    df = pd.melt(
        df,
        id_vars=HC_FTE_COLS,
        value_vars=SPEND_COLS_W_BONUS_AND_HC,
        var_name='MONTH',
        value_name='AMOUNT'
    )

    df['MONTH'].replace(HC_DICT_W_BONUS, inplace=True)
    df[['MONTH', 'CATEGORY']] = df['MONTH'].str.split("|", expand=True)
    df['YEAR'] = CURR_YEAR

    MONTH_TO_QUART = {
        "01":1,"02":1,"03":1,
        "04":2,"05":2,"06":2,
        "07":3,"08":3,"09":3,
        "10":4,"11":4,"12":4,
                    }
    
    df['QUARTER'] = df['MONTH'].replace(MONTH_TO_QUART)
    df['PROJ_ACT'] = "PROJECTION"

    return df
# END SCRIPT