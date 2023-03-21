from constants import *

# START SCRIPT
def setup_data_validation_ftc(df):
    # This function sets up the data validation for the FTC data
    # It returns a dictionary with the information needed for the validation

    # print the sum of all SPEND_COLS formatted as a currency
    FTC_SPEND = df[SPEND_COLS].sum().sum()
    print("the total FTC spend is " + "${:,.0f}".format(FTC_SPEND))
    print()

    return {
        'SPEND': FTC_SPEND,
        'SPEND_COLS': SPEND_COLS
    }
# END SCRIPT