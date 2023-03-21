# this is a test script
# print "Hello World"

import os

# START SCRIPT
def detect_environment():
    try:
        return os.environ['HOME'] == r"/home/domo"
    except KeyError:
        return False
# END SCRIPT

if __name__ == "__main__":
    print(detect_environment())