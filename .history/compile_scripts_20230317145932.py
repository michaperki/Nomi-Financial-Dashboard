import os
import re
import logging
from datetime import datetime

def compile_scripts():
    """
    Compiles all Python scripts in the 'scripts' folder into a single text file in the 'compiled_scripts' folder.
    Each script should have a '# START SCRIPT' and '# END SCRIPT' comment, and only the code between those comments
    will be included in the output. The import statements will be moved to the top of the output file, and consecutive
    line breaks in the output will be replaced with a single line break.

    Example usage:
        compile_scripts()

    """
    # Set up logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # Set the input and output folder names
    input_folder = "scripts"
    output_folder = "compiled_scripts"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get the current date and time
    date_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Create the output file name with the current date and time
    output_file_name = f"{output_folder}/compiled_scripts_{date_string}.txt"

    # Concatenate all the scripts in the input folder
    output_content = ""
    import_content = ""
    for filename in os.listdir(input_folder):
        if filename.endswith(".py"):
            script_path = os.path.join(input_folder, filename)
            with open(script_path) as script_file:
                script_content = script_file.read()

                # Extract the script content between the "# START SCRIPT" and "# END SCRIPT" comments
                script_content = re.search("# START SCRIPT\n(.+)\n# END SCRIPT", script_content, re.DOTALL)
                if script_content:
                    script_content = script_content.group(1)
                    output_content += script_content.strip() + "\n\n"

                    # Extract import statements and move them to the top of the output file
                    import_statements = re.findall("^(import .+)$|^(from .+)$", script_content, re.MULTILINE)
                    for statement in import_statements:
                        if statement[0]:
                            import_content += statement[0] + "\n"
                        elif statement[1]:
                            import_content += statement[1] + "\n"

    # Remove consecutive line breaks
    output_content = re.sub("\n{2,}", "\n", output_content)

    # Write the concatenated script content to the output file
    with open(output_file_name, "w") as output_file:
        output_file.write(f"from domomagic import *\n{import_content}\nimport os\nimport re\nimport logging\n{output_content}\nmain()")

    # Log success message
    logging.info(f"Compiled scripts written to {output_file_name}")
