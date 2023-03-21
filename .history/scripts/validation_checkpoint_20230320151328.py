from validate import validate

# START SCRIPT
def validation_checkpoint(val_dict, df_fte, df_orm, df_ftc, df_pro_serv, df_software, df_actuals):
    FTE_SUM_C0 = val_dict['FTE']['SPEND']
    PRO_SERV_SUM_C0 = val_dict['PRO_SERV']['SPEND']
    SOFTWARE_SUM_C0 = val_dict['SOFTWARE']['SPEND']
    FTC_SUM_C0 = val_dict['FTC']['SPEND']
    OPEN_ROLES_SUM_C0 = val_dict['ORM']['SPEND']
    ACTUALS_SUM_C0 = val_dict['ACTUALS']['SPEND']
    ACTUALS_SUM_DETAIL_C0 = val_dict['ACTUALS']['SPEND_DETAIL']

    FTE_SUM_C1 = df_fte['AMOUNT'].sum()
    PRO_SERV_SUM_C1 = df_pro_serv['AMOUNT'].sum()
    SOFTWARE_SUM_C1 = df_software['AMOUNT'].sum()
    FTC_SUM_C1 = df_ftc['AMOUNT'].sum()
    OPEN_ROLES_SUM_C1 = df_open_roles['AMOUNT'].sum()
    ACTUALS_SUM_C1 = df_actuals['AMOUNT'].sum()

    c1_fte_valid = validate(FTE_SUM_C0, FTE_SUM_C1)
    c1_open_roles_valid = validate(OPEN_ROLES_SUM_C0, OPEN_ROLES_SUM_C1)
    c1_ftc_valid = validate(FTC_SUM_C0, FTC_SUM_C1)
    c1_pro_serv_valid = validate(PRO_SERV_SUM_C0, PRO_SERV_SUM_C1)
    c1_software_valid = validate(SOFTWARE_SUM_C0, SOFTWARE_SUM_C1)
    c1_actuals_valid = validate(ACTUALS_SUM_C0, ACTUALS_SUM_C1)

# END SCRIPT