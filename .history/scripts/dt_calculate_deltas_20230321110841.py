from constants import *
import logging
import pandas as pd
from clean_actuals import clean_actuals
from clean_data import clean_data
from dt_clean_software_for_deltas import clean_software_for_deltas
from dt_clean_ftc_for_deltas import clean_ftc_for_deltas
from dt_clean_pro_serv_for_deltas import clean_pro_serv_for_deltas
from dt_clean_fte_for_deltas import clean_fte_for_deltas


# START SCRIPT
def calculate_deltas(df_fte, df_ftc, df_pro_serv, df_software, df_actuals, ACTUAL_FILE_DATE, df_name_map):

    models = [df_software, df_ftc, df_pro_serv, df_fte]
    df_actuals = clean_actuals(df_actuals, ACTUAL_FILE_DATE, df_name_map)
    df_actuals = df_actuals.loc[
        (df_actuals['EXPENSE_BUCKET'] == "SOFTWARE") | 
        (df_actuals['EXPENSE_BUCKET'] == "FTC") |
        (df_actuals['EXPENSE_BUCKET'] == "PRO_SERV") |
        (df_actuals['EXPENSE_BUCKET'] == "FTE")
    ]
    df_software['Paid by Credit Card (Y/N)'].fillna('N', inplace=True)
    df_software_paid_by_cc = df_software.loc[df_software['Paid by Credit Card (Y/N)'] == "Y"]
    df_software_paid_by_cc = df_software_paid_by_cc[['Vendor', 'Paid by Credit Card (Y/N)']]
    df_software_paid_by_cc = df_software_paid_by_cc.drop_duplicates()
    df_software_paid_by_cc = df_software_paid_by_cc.rename(columns={"Paid by Credit Card (Y/N)": "PAID_BY_CC"})
    df_software_paid_by_cc['PAID_BY_CC'] = 1
    
    # this will convert Inc to Inc. 
    df_software_paid_by_cc = clean_data(df_software_paid_by_cc)

    # convert the vendor names to upper case
    df_software_paid_by_cc['Vendor'] = df_software_paid_by_cc['Vendor'].str.upper()
    df_software = clean_software_for_deltas(df_software)
    df_ftc = clean_ftc_for_deltas(df_ftc)
    df_proserv = clean_pro_serv_for_deltas(df_proserv)
    df_fte = clean_fte_for_deltas(df_fte)
    
    df = pd.concat([df_ftc, df_software, df_proserv, df_fte], ignore_index=True)

    return df
# END SCRIPT