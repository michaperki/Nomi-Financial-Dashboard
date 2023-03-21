# this function is used to compile the scripts
# the scripts are located in the scripts folder
# the compiled scripts are located in the compiled_scripts folder
# the compiled scripts are used to run the scripts in Domo
# the compiled scripts output is a text file with the date and time of the run
# the output is a concatenation of all the files in the scripts folder

import os
import datetime

# get the current date and time
now = datetime.datetime.now()

def compile_scripts():
    # get the current working directory
    cwd = os.getcwd()
    # get the scripts folder
    scripts_folder = os.path.join(cwd, 'scripts')
    # get the compiled_scripts folder
    compiled_scripts_folder = os.path.join(cwd, 'compiled_scripts')
    # get the list of files in the scripts folder
    files = os.listdir(scripts_folder)
    # create the output file name
    output_file_name = 'output_' + now.strftime('%Y-%m-%d_%H-%M-%S') + '.txt'
    # create the output file path
    output_file_path = os.path.join(compiled_scripts_folder, output_file_name)
    # open the output file
    output_file = open(output_file_path, 'w')
    # loop through the files in the scripts folder
    for file in files:
        # get the file path
        file_path = os.path.join(scripts_folder, file)
        # open the file
        file = open(file_path, 'r')
        # read the file
        file_content = file.read()
        # write the file content to the output file
        output_file.write(file_content)
        # close the file
        file.close()
    # close the output file
    output_file.close()

if __name__ == '__main__':
    compile_scripts()