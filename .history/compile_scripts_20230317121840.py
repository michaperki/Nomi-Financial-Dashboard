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

def compile_scripts():
    # get the current working directory
    cwd = os.getcwd()
    # get the scripts folder
    scripts_folder = os.path.join(cwd, "scripts")
    # get the compiled_scripts folder
    compiled_scripts_folder = os.path.join(cwd, "compiled_scripts")
    # get the list of files in the scripts folder
    scripts = os.listdir(scripts_folder)
    # create the output file name
    output_file_name = "compiled_scripts_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
    # create the output file path
    output_file_path = os.path.join(compiled_scripts_folder, output_file_name)
    # open the output file
    output_file = open(output_file_path, "w")
    # loop through the scripts
    for script in scripts:
        # get the script file path
        script_file_path = os.path.join(scripts_folder, script)
        # open the script file
        script_file = open(script_file_path, "r")
        # get the lines in the script file
        script_lines = script_file.readlines()
        # loop through the lines in the script file
        for line in script_lines:
            # check if the line is a comment
            if line.startswith("#"):
                # check if the line is the start of the script
                if line.startswith("# START SCRIPT"):
                    # write the line to the output file
                    output_file.write(line)
                # check if the line is the end of the script
                elif line.startswith("# END SCRIPT"):
                    # write the line to the output file
                    output_file.write(line)
                    # write a new line to the output file
                    output_file.write("\n")
                    break
            # check if the line is not a comment
            else:
                # write the line to the output file
                output_file.write(line)
        # close the script file
        script_file.close()
    # close the output file
    output_file.close()

if __name__ == "__main__":
    compile_scripts()

