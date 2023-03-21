import logging

# START SCRIPT
def validate(expected, actual):
    # this function takes an expected value and an actual value
    # it rounds to the nearest whole number and prints if they are the same
    # it returns True if they are the same and False if they are not

    # round to the nearest whole number
    expected = round(expected)
    actual = round(actual)

    # print if they are the same (or within .01% of each other)
    # print the numbers as currency with commas and no decimals
    # if there is a difference, print the difference as a currency and percentage
    if abs(expected - actual) <= (expected * .0001):
        logging.info("the spend is within .01% of the expected spend")
        print()
        return True
    else:
        logging.warning("the expected spend is " + "${:,.0f}".format(expected))
        logging.warning("the actual spend is " + "${:,.0f}".format(actual))
        logging.warning("the spend is not within .01% of the expected spend")
        logging.warning("the difference is " + "${:,.0f}".format(actual - expected))
        logging.warning("the difference is " + "{:.2%}".format((actual - expected) / expected))
        return False

# END SCRIPT