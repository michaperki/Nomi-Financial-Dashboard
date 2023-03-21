
import os


def detect_environment():
    try:
        return os.environ['HOME'] == r"/home/domo"
    except KeyError:
        return False

def main():
    if detect_environment():
        print("Running in the Domo environment")
    else:
        print("Running in the local environment")

