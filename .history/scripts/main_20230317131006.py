# this is another test script

# import detect environment
from detect_environment import detect_environment

# START SCRIPT
import logging

#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def main():
    RUNNING_LOCALLY = detect_environment()
    logging.info(f"Running locally: {RUNNING_LOCALLY}")
    # END SCRIPT

if __name__ == "__main__":
    main()