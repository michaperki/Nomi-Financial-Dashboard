from setup_data_validation_fte import setup_val_fte

def setup_for_data_validation(ACTUAL_FILE_DATE):
    # This function sets up the data validation
    # It runs the data validation setup functions
    # and returns a dictionary with the information needed for the validation

    # set up the data validation for the FTE data
    val_fte = setup_val_fte()

    # # set up the data validation for the ORM data
    # val_orm = setup_val_orm()

    # # set up the data validation for the FTC data
    # val_ftc = setup_val_ftc()

    # # set up the data validation for the PRO_SERV data
    # val_pro_serv = setup_val_pro_serv()

    # # set up the data validation for the SOFTWARE data
    # val_software = setup_val_software()

    # # set up the data validation for the ACTUALS data
    # val_actuals = setup_val_actuals(ACTUAL_FILE_DATE)

    return {
        'FTE': val_fte,
        # 'ORM': val_orm,
        # 'FTC': val_ftc,
        # 'PRO_SERV': val_pro_serv,
        # 'SOFTWARE': val_software,
        # 'ACTUALS': val_actuals
    }