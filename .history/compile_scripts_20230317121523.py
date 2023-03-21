# this function is used to compile the scripts
# the scripts are located in the scripts folder
# the compiled scripts are located in the compiled_scripts folder
# the compiled scripts are used to run the scripts in Domo
# the compiled scripts output is a text file with the date and time of the run
# the output is a concatenation of all the files in the scripts folder
# separated by a new line
# only grab the portion of the file enclosed in the "# START SCRIPT" and "# END SCRIPT" comments

import os
import datetime

# get the current date and time
now = datetime.datetime.now()

def compile_scripts():
    # create the output file
    output_file = open("compiled_scripts\compiled_scripts_" + now.strftime("%Y-%m-%d_%H-%M-%S") + ".txt", "w")
    # get the list of files in the scripts folder
    files = os.listdir("scripts")
    # loop through the files
    for file in files:
        # open the file
        input_file = open("scripts\\" + file, "r")
        # read the file
        lines = input_file.readlines()
        # close the file
        input_file.close()
        # loop through the lines
        for line in lines:
            # check if the line is a comment
            if line.startswith("#"):
                # check if the line is the start of the script
                if line.startswith("# START SCRIPT"):
                    # write a new line to the output file
                    output_file.write("\n")
                # check if the line is the end of the script
                elif line.startswith("# END SCRIPT"):
                    # write a new line to the output file
                    output_file.write("\n")
            # check if the line is not a comment
            else:
                # write the line to the output file
                output_file.write(line)

        # write a new line to the output file
        output_file.write("\n")
    # close the output file
    output_file.close()

if __name__ == "__main__":
    compile_scripts()