from constants import *
import logging
import pandas as pd


# START SCRIPT
def move_actuals_forward_one_quarter(df):
    df = df.copy()
    df["Q-budget"] = df["Q-budget"] + 1
    df.loc[df["Q-budget"] == 5, "Y-budget"] = df["Y-budget"] + 1
    df.loc[df["Q-budget"] == 5, "Q-budget"] = 1
    return df
# END SCRIPT