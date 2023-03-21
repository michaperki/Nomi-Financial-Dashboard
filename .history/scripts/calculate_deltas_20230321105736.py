from constants import *
import logging
from clean_actuals import clean_actuals

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
    return df
# END SCRIPT