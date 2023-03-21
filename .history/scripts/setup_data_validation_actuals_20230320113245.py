from constants import *
import logging

# START SCRIPT
def setup_data_validation_software(df):
    # This function sets up the data validation for the SOFTWARE data
    # It returns a dictionary with the information needed for the validation

    # print the sum of all SPEND_COLS formatted as a currency
    SOFTWARE_SPEND = df[SPEND_COLS].sum().sum()
    logging.info("the total SOFTWARE spend is " + "${:,.0f}".format(SOFTWARE_SPEND))

    return {
        'SPEND': SOFTWARE_SPEND,
        'SPEND_COLS': SPEND_COLS
    }
# END SCRIPT