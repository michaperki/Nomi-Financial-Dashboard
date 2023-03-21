import os
import datetime
import logging

from domomagic import *


def compile_scripts():
    """
    Reads all the files in the 'scripts' folder and outputs a concatenated text
    file with the current date and time in the file name. The output is a
    concatenation of all the scripts, with import statements moved to the top,
    and each script separated by a new line. The script is saved in the
    'compiled_scripts' folder. At the end of the output text file, 'main()' is
    added.
    """
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    files = [f for f in os.listdir('scripts') if os.path.isfile(os.path.join('scripts', f))]

    now = datetime.datetime.now()
    output_filename = 'compiled_scripts/{}_{}.txt'.format(now.strftime('%Y-%m-%d_%H-%M-%S'), 'compiled')
    with open(output_filename, 'w') as outfile:
        outfile.write('from domomagic import *\n')
        imports = []
        for file in files:
            if file.endswith('.py'):
                logging.info(f"Processing file {file}")
                with open(os.path.join('scripts', file)) as infile:
                    content = infile.read()
                    lines = content.split('\n')
                    for line in lines:
                        if line.startswith('import') or line.startswith('from'):
                            if line not in imports:
                                imports.append(line)
                        elif '# START SCRIPT' in line:
                            outfile.write('\n')
                            outfile.write(f'# {file} - START\n')
                            break
                    for line in lines:
                        if '# END SCRIPT' in line:
                            outfile.write(f'# {file} - END\n')
                            outfile.write('\n')
                            break
                        elif '# START SCRIPT' not in line:
                            outfile.write(line + '\n')
        for imp in imports:
            outfile.write(imp + '\n')
        outfile.write('\nmain()\n')

    with open(output_filename, 'r') as outfile:
        content = outfile.read()
        content = content.replace('\n\n\n', '\n\n')
    with open(output_filename, 'w') as outfile:
        outfile.write(content)