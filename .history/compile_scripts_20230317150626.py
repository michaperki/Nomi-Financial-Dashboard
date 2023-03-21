import datetime
import logging
import os

def compile_scripts():
    # Set up logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    # Get the current date and time
    now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Create the output file path
    output_dir = 'compiled_scripts'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'compiled_scripts_{now}.py')

    # Define the order of the files
    file_order = [
        'detect_environment.py', 
        'get_data_from_domo.py', 
        'get_data_from_local.py', 
        'get_data_from_either.py', 
        'print_columns.py', 
        'get_data.py', 
        'complete_data_import.py',
        'write_data.py',
        'main.py'
    ]

    # Concatenate the scripts in the specified order
    script_dir = 'scripts'
    scripts = []
    for file in file_order:
        file_path = os.path.join(script_dir, file)
        if os.path.isfile(file_path):
            logging.info(f'Reading script {file}')
            with open(file_path, 'r') as f:
                lines = f.read().split('\n')
                start_index = [i for i, line in enumerate(lines) if '# START SCRIPT' in line]
                end_index = [i for i, line in enumerate(lines) if '# END SCRIPT' in line]
                if start_index and end_index:
                    start_index = start_index[0] + 1
                    end_index = end_index[0]
                    scripts.append('\n'.join(lines[start_index:end_index]).strip())

    # Write the concatenated scripts to the output file
    logging.info(f'Writing {len(scripts)} scripts to {output_path}')
    with open(output_path, 'w') as f:
        f.write('from domomagic import *\n\n')
        for script in scripts:
            f.write(script)
            f.write('\n\n')
        f.write('main()')

    # Log success message
    logging.info(f'Compilation complete')
