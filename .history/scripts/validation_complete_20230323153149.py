from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validation_complete(val_dict, df):
    FTE_SUM_C0 = val_dict['FTE']['SPEND']
    OPEN_ROLES_SUM_C0 = val_dict['ORM']['SPEND']
    FTC_SUM_C0 = val_dict['FTC']['SPEND']
    PRO_SERV_SUM_C0 = val_dict['PRO_SERV']['SPEND']
    SOFTWARE_SUM_C0 = val_dict['SOFTWARE']['SPEND']
    ACTUALS_SUM_C0 = val_dict['ACTUALS']['SPEND']
    ACTUALS_SUM_DETAIL_C0 = val_dict['ACTUALS']['SPEND_DETAIL']

    FTE_SUM_C2 = df[(df['EXPENSE_BUCKET'] == 'FTE') & (df['PROJ_ACT'] == 'PROJECTION')]['ALLOCATED_AMOUNT'].sum()
    PRO_SERV_SUM_C2 = df[(df['EXPENSE_BUCKET'] == 'PRO SERV') & (df['PROJ_ACT'] == 'PROJECTION')]['ALLOCATED_AMOUNT'].sum()
    SOFTWARE_SUM_C2 = df[(df['EXPENSE_BUCKET'] == 'SOFTWARE') & (df['PROJ_ACT'] == 'PROJECTION')]['ALLOCATED_AMOUNT'].sum()
    FTC_SUM_C2 = df[(df['EXPENSE_BUCKET'] == 'FTC') & (df['PROJ_ACT'] == 'PROJECTION')]['ALLOCATED_AMOUNT'].sum()
    OPEN_ROLES_SUM_C2 = df[(df['EXPENSE_BUCKET'] == 'OPEN ROLES') & (df['PROJ_ACT'] == 'PROJECTION')]['ALLOCATED_AMOUNT'].sum()
    ACTUALS_SUM_C2 = df[(df['PROJ_ACT'] == 'ACTUAL')]['ALLOCATED_AMOUNT'].sum()

    # filter df for PROJ_ACT = ACTUAL
    # group by EXPENSE_BUCKET, MONTH, and YEAR
    # sum the ALLOCATED_AMOUNT
    # join the ALLOCATED_AMOUNT to the ACTUALS_SUM_DETAIL_C0
    # on EXPENSE_BUCKET, MONTH, and YEAR
    # calculate the difference between the ACTUALS_SUM_DETAIL_C0 and the ACTUALS_SUM_DETAIL_C2
    # print the result
    ACTUALS_SUM_DETAIL_C2 = df[(df['PROJ_ACT'] == 'ACTUAL')].groupby(['EXPENSE_BUCKET', 'MONTH', 'YEAR'])['ALLOCATED_AMOUNT'].sum().reset_index()
    # rename the ALLOCATED_AMOUNT column to ALLOCATED_AMOUNT column to VAL_ACTUAL and the EXPENSE_BUCKET column to VAL_MODEL
    ACTUALS_SUM_DETAIL_C2 = ACTUALS_SUM_DETAIL_C2.rename(columns={'ALLOCATED_AMOUNT': 'VAL_ACTUAL', 'EXPENSE_BUCKET': 'VAL_MODEL'})
    # join the ACTUALS_SUM_DETAIL_C2 to the ACTUALS_SUM_DETAIL_C0
    logging.debug(ACTUALS_SUM_DETAIL_C2.head(10).to_string())
    logging.debug("type: " + str(type(ACTUALS_SUM_DETAIL_C2)))
    logging.debug(ACTUALS_SUM_DETAIL_C0.head(10).to_string())
    logging.debug("type: " + str(type(ACTUALS_SUM_DETAIL_C0)))

    # add a leading zero to the MONTH column in ACTUALS_SUM_DETAIL_C0
    ACTUALS_SUM_DETAIL_C0['MONTH'] = ACTUALS_SUM_DETAIL_C0['MONTH'].apply(lambda x: '{0:0>2}'.format(x))
    # replace the "_" with " " in the VAL_MODEL column in ACTUALS_SUM_DETAIL_C0
    ACTUALS_SUM_DETAIL_C0['VAL_MODEL'] = ACTUALS_SUM_DETAIL_C0['VAL_MODEL'].apply(lambda x: x.replace('_', ' '))

    # join the ACTUALS_SUM_DETAIL_C2 to the ACTUALS_SUM_DETAIL_C0
    ACTUALS_SUM_DETAIL_C2 = pd.merge(ACTUALS_SUM_DETAIL_C0, ACTUALS_SUM_DETAIL_C2, how='left', on=['VAL_MODEL', 'MONTH', 'YEAR'])

    # log the first 10 rows of ACTUALS_SUM_DETAIL_C2 where YEAR is CURR_YEAR
    logging.debug(ACTUALS_SUM_DETAIL_C2[ACTUALS_SUM_DETAIL_C2['YEAR'] == CURR_YEAR].head(10).to_string())

    c2_fte_valid = validate(FTE_SUM_C0, FTE_SUM_C2)
    c2_pro_serv_valid = validate(PRO_SERV_SUM_C0, PRO_SERV_SUM_C2)
    c2_software_valid = validate(SOFTWARE_SUM_C0, SOFTWARE_SUM_C2)
    c2_ftc_valid = validate(FTC_SUM_C0, FTC_SUM_C2)
    c2_open_roles_valid = validate(OPEN_ROLES_SUM_C0, OPEN_ROLES_SUM_C2)
    c2_actuals_valid = validate(ACTUALS_SUM_C0, ACTUALS_SUM_C2)

    # Create a data frame with the results of the data validation
    # Where the data frame has 6 rows and 5 columns, with the following column names:
    # VAL_CHECKPOINT, VAL_MODEL, VAL_ACTUAL, VAL_EXPECTED, VAL_VALID
    df_data_validation = pd.DataFrame(
        {
            'VAL_CHECKPOINT': ['MAIN', 'MAIN', 'MAIN', 'MAIN', 'MAIN', 'MAIN'], 
            'VAL_MODEL': ['FTE', 'PRO SERV', 'SOFTWARE', 'FTC', 'OPEN ROLES', 'ACTUALS'],
            'VAL_ACTUAL': [FTE_SUM_C2, PRO_SERV_SUM_C2, SOFTWARE_SUM_C2, FTC_SUM_C2, OPEN_ROLES_SUM_C2, ACTUALS_SUM_C2],
            'VAL_EXPECTED': [FTE_SUM_C0, PRO_SERV_SUM_C0, SOFTWARE_SUM_C0, FTC_SUM_C0, OPEN_ROLES_SUM_C0, ACTUALS_SUM_C0],
            'VAL_VALID': [c2_fte_valid, c2_pro_serv_valid, c2_software_valid, c2_ftc_valid, c2_open_roles_valid, c2_actuals_valid]
        }
    )

    return df_data_validation
# END SCRIPT