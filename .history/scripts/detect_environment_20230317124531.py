# this is a test script
# print "Hello World"

import os

# START SCRIPT
def detect_environment():
    return os.environ['HOME'] == r"/home/domo"
# END SCRIPT

if __name__ == "__main__":
    print(detect_environment())