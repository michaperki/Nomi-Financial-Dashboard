# this is another test script

# import detect environment
from detect_environment import detect_environment

# START SCRIPT
def main():
    if detect_environment():
        print("Running in the Domo environment")
    else:
        print("Running in the local environment")
# END SCRIPT

if __name__ == "__main__":
    main()