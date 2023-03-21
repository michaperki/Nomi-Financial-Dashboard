import os
import datetime
import logging

from domomagic import *

def compile_scripts():
    """
    This function reads all the Python script files in the 'scripts' folder, extracts the code between the
    '# START SCRIPT' and '# END SCRIPT' comments, concatenates them, and writes the result to a text file
    with the current date and time in the file name. The resulting file is saved in the 'compiled_scripts'
    folder.

    It also ensures that the import statements are moved to the top of the output and adds "from domomagic import *"
    to the import statements. Additionally, it adds "logging.basicConfig(format='%(levelname)s:%(message)s',
    level=logging.INFO)" after the import statements.

    At the end of the output text file, it adds a line "main()" and replaces any consecutive line breaks with
    a single line break.
    """
    # Set the source and destination folders
    src_folder = 'scripts'
    dst_folder = 'compiled_scripts'

    # Get the current date and time for the file name
    now = datetime.datetime.now()
    file_name = f'scripts_{now.strftime("%Y-%m-%d_%H-%M-%S")}.txt'

    # Read all the script files and concatenate their contents
    output = ''
    for file in sorted(os.listdir(src_folder)):
        if file.endswith('.py'):
            with open(os.path.join(src_folder, file), 'r') as f:
                script = f.read()
                start = script.find('# START SCRIPT')
                end = script.find('# END SCRIPT')
                if start != -1 and end != -1:
                    output += script[start + 14:end] + '\n'

    # Move import statements to the top
    imports = ''
    rest_of_output = ''
    for line in output.split('\n'):
        if line.startswith('import') or 'import' in line and 'from' in line:
            imports += line + '\n'
        else:
            rest_of_output += line + '\n'

    # Concatenate the imports and the rest of the output
    final_output = f'from domomagic import *\n{imports}logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)\n{rest_of_output}main()\n'

    # Replace consecutive line breaks with a single line break
    final_output = '\n'.join(filter(None, final_output.split('\n')))

    # Write the output to the destination file
    with open(os.path.join(dst_folder, file_name), 'w') as f:
        f.write(final_output)

compile_scripts()
