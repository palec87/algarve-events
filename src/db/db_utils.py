import sqlite3
import logging

import coloredlogs


coloredlogs.install(level='DEBUG',
                    fmt='%(asctime)s %(levelname)s %(message)s')

class DB():
    def __init__(self, db_file):
        # Set up logging
        self._logger = logging.getLogger(db_file.split('.')[0])
        logging.basicConfig(level=logging.INFO)
        self.db_file = db_file

    def connect(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def get_sources(self):
        self.connect()
        self.cursor.execute("SELECT * FROM sources")
        sources = self.cursor.fetchall()
        self.close()
        return sources
    
    def insert_source(self, source):
        self.connect()
        # Define default values
        default_values = {
            "url": "",
            "tags": "",
            "scrape": None,
            "robots": "",
            "dynamic": None,
            "last_scrape": None,
            "last_check": None
        }

        # Ensure the source tuple has six elements
        source = {key: source.get(key, default_values[key]) for key in default_values.keys()}
        source_tuple = (source["url"],
                        source["tags"],
                        source["scrape"],
                        source["robots"],
                        source["dynamic"],
                        source["last_scrape"],
                        source["last_check"],
                        )
        self._logger.debug(f"Inserting source {source['url']}")

        # Insert the source after checking for duplicates
        if not self.check_duplicate_source(source['url']):
            self.cursor.execute("INSERT INTO sources (url, tags, scrape, robots, dynamic, last_scrape, last_check) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                source_tuple)
            self.conn.commit()
        else:

            self._logger.info(f"Source {source['url']} already exists in the database")

        self.close()

    # method to check a duplicate source
    def check_duplicate_source(self, url):
        self.connect()
        self.cursor.execute("SELECT * FROM sources WHERE url = ?", (url,))
        result = self.cursor.fetchone()
        return result is not None
    
    # Method to retrieve sources by URL substring
    def get_sources_by_url_substring(self, substring):
        self.connect()
        self.cursor.execute("SELECT * FROM sources WHERE url LIKE ?", ('%' + substring + '%',))
        sources = self.cursor.fetchall()

        # Retrieve column names
        self.cursor.execute("PRAGMA table_info(sources)")
        columns_info = self.cursor.fetchall()
        column_names = [info[1] for info in columns_info]

        self.close()
        return column_names, sources
    
    def insert_event(self, event):
        self.connect()

        # Define default values
        default_values = {
            "source_id": None,
            "title": "",
            "link": "",
            "date": "",
            "time": "",
            "location": "",
            "tags": "",
            "description": ""
        }

        # Ensure the event dictionary has all required keys
        event = {key: event.get(key, default_values[key]) for key in default_values.keys()}
        event_tuple = (event["source_id"], event["title"], event["link"], event["date"],
                       event["time"], event["location"], event["tags"], event["description"])

        self._logger.debug(f"Inserting event {event['title']}")

        self.cursor.execute("INSERT INTO events (source_id, title, link, date, time, location, tags, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            event_tuple)
        self.conn.commit()
        self.close()



######################
# Setup the database #
######################
def run_setup(db_file):
    # Database setup
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sources (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        tags TEXT,
        scrape BOOLEAN,
        robots TEXT,
        dynamic BOOLEAN,
        last_scrape TEXT,
        last_check TEXT
    )
    ''')

    # Create table 'events' if it does not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id INTEGER,
        title TEXT,
        link TEXT,
        date TEXT,
        time TEXT,
        location TEXT,
        tags TEXT,
        description TEXT,
        FOREIGN KEY (source_id) REFERENCES sources(id)
    )
    ''')

    conn.commit()
    conn.close()