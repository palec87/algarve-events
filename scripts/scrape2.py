from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import json
import time
import sqlite3
from random import randint

driver_path = "C:\\Users\\David Palecek\\Documents\\Python_projects\\algarve-webscrape\\geckodriver.exe"
firefox_binary_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"  # Update this path if necessary

options = Options()
options.binary_location = firefox_binary_path

service = Service(executable_path=driver_path)
driver = webdriver.Firefox(service=service, options=options)

# URL to scrape
# this is a music category on visitalgarve.pt
url = "https://eventos.visitalgarve.pt/pt/agenda?category=1341"

driver.get(url)
print(driver.title)
time.sleep(randint(2, 6))


eventLinks = []
event_elements = driver.find_elements(By.CLASS_NAME, "common-items-card")  # Adjust class as per the actual HTML

for event in event_elements:
    try:
        link = event.find_element(By.TAG_NAME, "a").get_attribute("href")
        # title = event.find("h2", class_="event-title-class").text.strip()  # Adjust class
        # date = event.find("span", class_="event-date-class").text.strip()  # Adjust class
        # location = event.find("span", class_="event-location-class").text.strip()  # Adjust class
        # description = event.find("p", class_="event-description-class").text.strip()  # Adjust class

        eventLinks.append({
            "link": link,
            # "date": date,
            # "location": location,
            # "description": description,
        })
    except AttributeError:
        # Skip events with missing data
        print("Skipping event with missing data")
        continue

# section of going link by links to extract additional data
events = []
try:
    for link in eventLinks:
        driver.get(link['link'])
        time.sleep(randint(2, 6))
        # Extract additional data
        # title
        try:
            title = driver.find_element(By.CLASS_NAME, "page-event-header-title").text.strip()
        except:
            title = None
            #
        # date
        try:
            date = driver.find_element(By.CLASS_NAME, "text").text.strip()
            print(date)
        except:
            date = None
        # add to the event dictionary
        event = {
            "link": link,
            "title": title,
            "date": date,
        }
        events.append(event)
finally:
    driver.quit()

print(events)

# Insert events into the database
db_file = "events.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

for event in events:
    cursor.execute('''
    INSERT INTO events (link, title, date, description)
    VALUES (?, ?, ?, ?)
    ''', (event["link"], event['title'], event["date"]))
conn.commit()


# Close the database connection
conn.close()


# Save to JSON for now as well
output_file = "eventLinks.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(eventLinks, f, ensure_ascii=False, indent=4)

print(f"Scraped {len(eventLinks)} events. Saved to {output_file}.")