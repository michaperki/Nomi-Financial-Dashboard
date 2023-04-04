from imports import *

# import detect environment
from constants import *
from clean_allocation_sheet import clean_allocation_sheet
from clean_fte import clean_fte
from clean_orm import clean_orm
from clean_ftc import clean_ftc
from clean_pro_serv import clean_pro_serv
from clean_software import clean_software
from join_allocation_to_df import join_allocation_to_df
from format_final_df import format_final_df

# START SCRIPT
def main_function_no_actuals(df_fte, df_open_roles, df_ftc, df_pro_serv, df_software, df_fte_allocation, df_ftc_allocation, df_pro_serv_allocation, df_software_allocation, df_name_map):
    df_fte_allocation['SOURCE'] = 'FTE_AND_OPEN_ROLES'
    df_ftc_allocation['SOURCE'] = 'FTC'
    df_pro_serv_allocation['SOURCE'] = 'PRO_SERV'
    df_software_allocation['SOURCE'] = 'SOFTWARE'
    df_fte_allocation = clean_allocation_sheet(df_fte_allocation, df_name_map)
    df_ftc_allocation = clean_allocation_sheet(df_ftc_allocation, df_name_map)
    df_pro_serv_allocation = clean_allocation_sheet(df_pro_serv_allocation, df_name_map)
    df_software_allocation = clean_allocation_sheet(df_software_allocation, df_name_map)
    df_fte = clean_fte(df_fte)
    df_open_roles = clean_orm(df_open_roles)
    df_ftc = clean_ftc(df_ftc)
    df_pro_serv = clean_pro_serv(df_pro_serv)
    df_software = clean_software(df_software)
    df_fte = join_allocation_to_df(df_fte, df_fte_allocation)
    df_open_roles = join_allocation_to_df(df_open_roles, df_fte_allocation)
    df_ftc = join_allocation_to_df(df_ftc, df_ftc_allocation)
    df_pro_serv = join_allocation_to_df(df_pro_serv, df_pro_serv_allocation)
    df_software = join_allocation_to_df(df_software, df_software_allocation)
    df = pd.concat((df_fte, df_open_roles, df_software, df_pro_serv, df_ftc), ignore_index=True)
    df = format_final_df(df, 0)
    df['SEGMENT'] = "QUARTERLY"
    return df
# END SCRIPT