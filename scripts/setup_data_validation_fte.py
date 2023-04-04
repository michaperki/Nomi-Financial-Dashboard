from imports import *

from constants import *

# START SCRIPT
def setup_data_validation_fte(df):
    # This function sets up the data validation for the FTE data
    # It returns a dictionary with the information needed for the validation

    # print the sum of all SPEND_COLS_W_BONUS formatted as a currency
    FTE_SPEND = df[SPEND_COLS_W_BONUS].sum().sum()
    logging.info("the total FTE spend is " + "${:,.0f}".format(FTE_SPEND))

    # print the sum of all SPEND_COLS_W_BONUS by YEAR formatted as a currency

    return {
        'SPEND': FTE_SPEND,
        'SPEND_COLS': SPEND_COLS_W_BONUS
    }
# END SCRIPT