"""
Calling specific scraping scripts
"""

import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the config module
from src import config

# Add the project root to sys.path
sys.path.append(config.get_root_dir())

# here I want to try except call all the scraping scripts one by one locally
try:
    exec(open("scripts/scrape_visitalgarve.py").read())
except Exception as e:
    print("Error in scrape_visitalgarve.py:", e)
