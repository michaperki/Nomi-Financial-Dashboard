from imports import *

# START SCRIPT

def get_date_from_string(date_string):
    # This function converts a string containing
    # a month name into a date. Should also work for three letter month names

    month_str_to_int_dict = {month: index for index, month in enumerate(calendar.month_name) if month}
    short_month_str_to_int_dict = {month: index for index, month in enumerate(calendar.month_abbr) if month}

    # append the short month names to the dictionary
    month_str_to_int_dict.update(short_month_str_to_int_dict)

    for key, value in month_str_to_int_dict.items():
        # convert key to lowercase
        if key.lower() in date_string.lower():
            date_val = value
            break
    return date_val
# END SCRIPT