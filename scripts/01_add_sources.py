import sys
import os
import sqlite3
import json


# name of the database file
DB_NAME = "algarve_events.db"

# # Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.db import db_utils as db
from src import config

# TODO: This can probably be refactored to a DB method
# Database setup
print(config.get_root_dir())
db_file = os.path.join(config.get_root_dir(), DB_NAME)



# define DB file
sqlDB = db.DB(db_file)


# Run setup_db.py if the database does not exist
if not os.path.exists(db_file):
    sqlDB._logger.info('DB does not exist, running setup')
    db.run_setup(sqlDB.db_file)

else:
    sqlDB._logger.info('DB exists')


# read sources from a file
with open(os.path.join(config.get_root_dir(), "src\\db\\sources.json"), "r") as f:
    sources = json.load(f)


for i, source in enumerate(sources['sources']):
    # check of duplicates inside of insert_source, DB level
    sqlDB.insert_source(source)
