import os
from datetime import datetime
import re

def compile_scripts():
    """
    Reads all the files in the "scripts" folder and concatenates them into a
    single output file, ordered according to a predefined list. Only the piece
    of each script between "# START SCRIPT" and "# END SCRIPT" comments is
    included in the output. Import statements are moved to the top of the output
    file, and a logging configuration is added below the imports. The output
    file is saved in the "compiled_scripts" folder with a filename that includes
    the current date and time.
    """
    # Get the current date and time
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")
 
    # Define the input and output paths
    input_folder = "scripts"
    output_folder = "compiled_scripts"
    output_file = f"output_{dt_string}.py"
    output_path = os.path.join(output_folder, output_file)

    # Define the order in which the files should be compiled
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
        "setup_for_data_validation_fte.py",
        "setup_for_data_validation.py",
        "write_data.py",
        "main.py"
    ]

    # Loop over the files in the desired order and compile them
    output = ""
    imports = "from domomagic import *\n\n"
    for filename in file_order:
        filepath = os.path.join(input_folder, filename)
        if os.path.isfile(filepath):
            # Read the file contents
            with open(filepath, "r") as f:
                contents = f.read()

            # Extract the script between "# START SCRIPT" and "# END SCRIPT" comments
            start_index = contents.find("# START SCRIPT")
            end_index = contents.find("# END SCRIPT")
            if start_index >= 0 and end_index >= 0:
                script = contents[start_index+len("# START SCRIPT"):end_index]

                # Extract all import statements from the script
                lines = script.split("\n")
                import_lines = [line for line in lines if line.startswith("import") or line.startswith("from ")]
                imports += "\n".join(import_lines) + "\n"

                # Remove the import statements from the script
                script = "\n".join([line for line in lines if not (line.startswith("import") or line.startswith("from "))])

                output += script.strip() + "\n\n"

    # Write the output to a file in the output folder
    os.makedirs(output_folder, exist_ok=True)
    with open(output_path, "w") as f:
        output_final = imports + "\nimport logging\nlogging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)\n\n" + output + "main()"
        # replace more than one consecutive line break with a single line break in output_final
        output_final = re.sub(r'\n{2,}', '\n', output_final)
        f.write(output_final)

if __name__ == "__main__":
    # Call the function to compile the scripts
    compile_scripts()