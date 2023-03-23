import os
import re
import pandas as pd

def compile_scripts():
    """
    Reads all the files in the "scripts" folder and creates a data frame with the script name and the number of lines.
    Also include the count of "import" statements in each script, a count of print statements, and a count of logging statements.
    Print the data frame to the console.
    """

    # Define the input path
    input_folder = "scripts"

    file_order = [
        "constants.py",
        "detect_environment.py",
        "get_data_from_local.py",
        "get_data_from_domo.py",
        "get_data_from_either.py",
        "print_columns.py",
        "get_data.py",
        "complete_data_import.py",
        "get_date_from_string.py",
        "get_actuals_date.py",
        "setup_data_validation_fte.py",
        "setup_data_validation_orm.py",
        "setup_data_validation_ftc.py",
        "setup_data_validation_pro_serv.py",
        "setup_data_validation_software.py",
        "setup_data_validation_actuals.py",
        "setup_data_validation.py",
        "clean_data.py",
        "clean_allocation_sheet.py",
        "remove_string_from_column.py",
        "format_cash_view.py",
        "join_name_map_to_actuals.py",
        "clean_actuals_fte.py",
        "clean_actuals.py",
        "clean_projections.py",
        "clean_fte.py",
        "clean_orm.py",
        "clean_ftc.py",
        "clean_pro_serv.py",
        "clean_software.py",
        "validate.py",
        "validation_checkpoint.py",
        "duplicate_df_for_shared_services.py",
        "join_allocation_to_df.py",
        "format_final_df.py",
        "validation_complete.py",
        "hc_clean_fte_for_hc.py",
        "hc_clean_orm_for_hc.py",
        "hc_clean_headcounts.py",
        "hc_format_headcounts.py",
        "hc_calculate_headcount.py",
        "dt_clean_software_for_deltas.py",
        "dt_clean_ftc_for_deltas.py",
        "dt_clean_pro_serv_for_deltas.py",
        "dt_clean_fte_for_deltas.py",
        "dt_calculate_deltas.py",
        "qt_get_quarters_from_file_name.py",
        "qt_get_latest_data_for_each_quarter.py",
        "qt_move_actuals_forward_one_quarter.py",
        "qt_main_function_no_actuals.py",
        "qt_main_function.py",
        "qt_format_quarterly_data.py",
        "qm_calculate_qm_diff.py",
        "write_data.py",
        "_main_.py"
    ]

    # create an empty list to store the results
    results = []

    # loop through the files in the input folder
    for file in file_order:
        # Define the input path
        input_path = os.path.join(input_folder, file)

        # Open the file
        with open(input_path, "r") as f:
            # Read the file
            file_content = f.read()

            # Get the number of lines
            num_lines = len(file_content.splitlines())

            # Get the number of import statements
            num_imports = len(re.findall("import", file_content))

            # Get the number of logging statements
            num_loggings = len(re.findall("logging", file_content))

            # Get the number of logging statements
            num_dfs = len(re.findall("to_string", file_content))

            # Print the results
            results.append([file, num_lines, num_imports, num_loggings, num_dfs])

    # convert the results to a data frame
    df = pd.DataFrame(results, columns=["file", "num_lines", "num_imports", "num_loggings", "num_dfs"])

    # sort the data frame by the number of print statements
    df = df.sort_values(by="num_loggings", ascending=False)

    # Print the data frame
    print(df.head(10))



            


if __name__ == "__main__":
    # Call the function to compile the scripts
    compile_scripts()