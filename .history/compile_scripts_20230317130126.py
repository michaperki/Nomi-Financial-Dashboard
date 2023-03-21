"""
This script reads all the files in the "scripts" folder and outputs a text file
with the current date and time in the file name. The output is a concatenation
of all the scripts. Each script will have a "# START SCRIPT" and "# END SCRIPT"
comment. The script between these comments for each file will be captured and
concatenated in the output file. Each script in the output should be separated
by a new line. The output file will be saved in the "compiled_scripts" folder.
"""

import os
from datetime import datetime

import os
from datetime import datetime

def compile_scripts():
    # Get the current date and time
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")

    # Define the input and output paths
    input_folder = "scripts"
    output_folder = "compiled_scripts"
    output_file = f"output_{dt_string}.py"
    output_path = os.path.join(output_folder, output_file)

    # Define the order in which the files should be compiled
    file_order = ["script1.py", "script2.py", "script3.py"]  # replace with your own list

    # Loop over the files in the desired order and compile them
    output = ""
    imports = ""  # will store all import statements
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

                output += script.strip() + "\n\n"  # add an extra newline after each file

    # Write the output to a file in the output folder
    os.makedirs(output_folder, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(imports + "\n\n" + output)

if __name__ == "__main__":
    # Call the function to compile the scripts
    compile_scripts()