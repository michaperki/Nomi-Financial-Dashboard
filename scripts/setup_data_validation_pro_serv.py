from imports import *

from constants import *

# START SCRIPT
def setup_data_validation_pro_serv(df):
    # This function sets up the data validation for the PRO_SERV data
    # It returns a dictionary with the information needed for the validation

    # print the sum of all SPEND_COLS formatted as a currency
    PRO_SERV_SPEND = df[SPEND_COLS].sum().sum()
    logging.info("the total PRO_SERV spend is " + "${:,.0f}".format(PRO_SERV_SPEND))
    
    return {
        'SPEND': PRO_SERV_SPEND,
        'SPEND_COLS': SPEND_COLS
    }
# END SCRIPT