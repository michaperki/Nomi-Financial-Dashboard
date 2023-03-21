# this is another test script

# import detect environment
from detect_environment import detect_environment

# START SCRIPT
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

def main():
    if detect_environment():
        logging.info("Running in the Domo environment")
    else:
        logging.info("Running in the local environment")
# END SCRIPT

if __name__ == "__main__":
    main()