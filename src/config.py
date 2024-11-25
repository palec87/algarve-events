import os

# Define the root directory of the package
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_root_dir():
    return ROOT_DIR