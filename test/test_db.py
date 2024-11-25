
import sqlite3
# Database setup
db_file = "events_test.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
# Create table if it does not exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    link TEXT,
    date TEXT,
    time TEXT,
    location TEXT,
    description TEXT
)
               ''')
conn.commit()

# generate example dictionary of data to input into the database
event_data = {
    "title": "Example Event",
    "link": "https://example.com",
    "date": "2023-04-01",
    "time": "10:00",
    "location": "Example Location",
    "description": "This is an example event."
}
# Insert event data into the database
cursor.execute('''
INSERT INTO events (title, link, date, time, location, description)
               VALUES (?, ?, ?, ?, ?, ?)
               ''', (event_data["title"], event_data["link"], event_data["date"], event_data["time"], event_data["location"], event_data["description"]))
conn.commit()
# Retrieve event data from the database
cursor.execute('''
SELECT * FROM events
               ''')
rows = cursor.fetchall()
for row in rows:
    print(row)
# Close the database connection
conn.close()
