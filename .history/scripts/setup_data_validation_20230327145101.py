from setup_data_validation_fte import setup_data_validation_fte
from setup_data_validation_orm import setup_data_validation_orm
from setup_data_validation_ftc import setup_data_validation_ftc
from setup_data_validation_pro_serv import setup_data_validation_pro_serv
from setup_data_validation_software import setup_data_validation_software
from setup_data_validation_actuals import setup_data_validation_actuals

# START SCRIPT
def setup_data_validation(ACTUAL_FILE_DATE, FILE_DICT):
    # This function sets up the data validation
    # It runs the data validation setup functions
    # and returns a dictionary with the information needed for the validation

    # get the FTE data
    FTE = FILE_DICT['FTE']
    ORM = FILE_DICT['ORM']
    FTC = FILE_DICT['FTC']
    PRO_SERV = FILE_DICT['PRO_SERV']
    SOFTWARE = FILE_DICT['SOFTWARE']
    ACTUALS = FILE_DICT['ACTUALS']

    # set up the data validation for the FTE data
    val_fte = setup_data_validation_fte(FTE)

    # set up the data validation for the ORM data
    val_orm = setup_data_validation_orm(ORM)

    # set up the data validation for the FTC data
    val_ftc = setup_data_validation_ftc(FTC)

    # set up the data validation for the PRO_SERV data
    val_pro_serv = setup_data_validation_pro_serv(PRO_SERV)

    # set up the data validation for the SOFTWARE data
    val_software = setup_data_validation_software(SOFTWARE)

    # set up the data validation for the ACTUALS data
    val_actuals = setup_data_validation_actuals(ACTUALS, ACTUAL_FILE_DATE)

    return {
        'FTE': val_fte,
        'ORM': val_orm,
        'FTC': val_ftc,
        'PRO_SERV': val_pro_serv,
        'SOFTWARE': val_software,
        'ACTUALS': val_actuals
    }
# END SCRIPT