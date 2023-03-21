from constants import *

# START SCRIPT
def setup_data_validation_software(df):
    # This function sets up the data validation for the SOFTWARE data
    # It returns a dictionary with the information needed for the validation

    # print the sum of all SPEND_COLS formatted as a currency
    SOFTWARE_SPEND = df[SPEND_COLS].sum().sum()
    print("the total SOFTWARE spend is " + "${:,.0f}".format(SOFTWARE_SPEND))
    print()

    return {
        'SPEND': SOFTWARE_SPEND,
        'SPEND_COLS': SPEND_COLS
    }
# END SCRIPT