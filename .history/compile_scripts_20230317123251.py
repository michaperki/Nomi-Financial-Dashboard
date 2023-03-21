# this function is used to compile the scripts
# the scripts are located in the scripts folder
# the compiled scripts are located in the compiled_scripts folder
# the compiled scripts are used to run the scripts in Domo
# the compiled scripts output is a text file with the date and time of the run
# the output is a concatenation of all the files in the scripts folder separated by a new line
# only grab the portion of each file that is enclosed in the "# START SCRIPT" and "# END SCRIPT" comments

import os
import datetime

# get the current date and time
now = datetime.datetime.now()
dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")

def compile_scripts():
    # Define the input and output paths
    input_folder = "scripts"
    output_folder = "compiled_scripts"
    output_file = f"output_{dt_string}.txt"
    output_path = os.path.join(output_folder, output_file)

    # Loop over all the files in the input folder
    output = ""
    for filename in os.listdir(input_folder):
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
                output += script.strip() + "\n"

    # Write the output to a file in the output folder
    os.makedirs(output_folder, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(output)

if __name__ == "__main__":
    compile_scripts()

