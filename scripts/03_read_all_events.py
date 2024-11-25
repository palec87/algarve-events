"""
Script to read all events from the database
"""

import os
import sys
import logging
import coloredlogs
# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# Import the config module
from src import config
# Add the project root to sys.path
sys.path.append(config.get_root_dir())
from src.db import db_utils as db

# setup logging
logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)
coloredlogs.install(level='DEBUG', logger=logger,
                    fmt='%(asctime)s %(levelname)s %(message)s')

# Database setup
db_file = os.path.join(config.get_root_dir(), "algarve_events.db")
sqlDB = db.DB(db_file)
# read events table
sqlDB.connect()
sqlDB.cursor.execute("SELECT * FROM events")
events = sqlDB.cursor.fetchall()
sqlDB.close()

# print the events
for event in events:
    logger.info(event)

# print the number of events
logger.info(f"Number of events: {len(events)}")

# print the number of unique events
unique_events = set(events)
logger.info(f"Number of unique events: {len(unique_events)}")

