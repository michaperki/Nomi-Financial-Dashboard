from validate import validate
import pandas as pd
import logging
from constants import *

# START SCRIPT
def validate_headcounts(df_main, df_headcounts):
    # Validate headcounts against main df
    # print the head of both dfs
    
    print(df_main.head.to_string())
    print(df_headcounts.head.to_string())

# END SCRIPT