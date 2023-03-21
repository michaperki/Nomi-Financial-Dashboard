import os
import logging


def detect_environment():
    try:
        return os.environ['HOME'] == r"/home/domo"
    except KeyError:
        return False

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def main():
    RUNNING_LOCALLY = detect_environment()
    logging.info(f"Running locally: {RUNNING_LOCALLY}")

