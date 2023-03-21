import os
from datetime import datetime

def compile_scripts():
    # Get the current date and time
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H-%M-%S")

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
                output += script.strip() + "\n\n"  # add an extra newline after each file

    # Write the output to a file in the output folder
    os.makedirs(output_folder, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(output)

if __name__ == "__main__":
    # Call the function to compile the scripts
    compile_scripts()
