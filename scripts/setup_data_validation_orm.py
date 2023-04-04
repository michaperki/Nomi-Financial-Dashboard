from imports import *

from constants import *

# START SCRIPT
def setup_data_validation_orm(df):
    # This function sets up the data validation for the ORM data
    # It returns a dictionary with the information needed for the validation

    # print the sum of all SPEND_COLS formatted as a currency
    ORM_SPEND = df[ORM_COLS].sum().sum()
    logging.info("the total ORM spend is " + "${:,.0f}".format(ORM_SPEND))

    return {
        'SPEND': ORM_SPEND,
        'SPEND_COLS': ORM_COLS
    }
# END SCRIPT