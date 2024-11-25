import os
import sys
import logging
import coloredlogs

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import json
import time
import sqlite3
from random import randint

DEBUG = False
#setup logging
logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)
coloredlogs.install(level='DEBUG', logger=logger,
                    fmt='%(asctime)s %(levelname)s %(message)s')

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the config module
from src import config

# Add the project root to sys.path
sys.path.append(config.get_root_dir())

from src.db import db_utils as db

##################
# Database setup #
##################
db_file = os.path.join(config.get_root_dir(), "algarve_events.db")
sqlDB = db.DB(db_file)

substring = "visitalgarve"
col_names, sources = sqlDB.get_sources_by_url_substring(substring)
logger.debug(f"DB columns: {col_names}")

# for source in sources:
#     sqlDB._logger.info(source)

##################
# Selenium setup #
##################
driver_path = "C:\\Users\\David Palecek\\Documents\\Python_projects\\algarve-webscrape\\geckodriver.exe"
firefox_binary_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"  # Update this path if necessary

options = Options()
options.binary_location = firefox_binary_path

service = Service(executable_path=driver_path)
driver = webdriver.Firefox(service=service, options=options)

"""
# first item on the page to scrape  
/html/body/div/div/main/div[1]/div/div[3]/section[1]/div/div[1]

# second item on the page to scrape
/html/body/div/div/main/div[1]/div/div[3]/section[1]/div/div[2]
"""
# iterate over sources
for source in sources[:1]:
    logger.info(f'source is {source}')
    # iterate over pages
    j = 0  # page counter
    url = source[col_names.index("url")]  # this updates until there are no more event)elements
    while True:
        driver.get(url)
        logger.info(driver.title)
        time.sleep(randint(2, 6))

        event_elements = driver.find_elements(By.CLASS_NAME, "common-items-card") # this finds all the events on the page
        if DEBUG:
            logger.info(f"Number of events: {len(event_elements)}")
            logger.info(f"Event elements: {event_elements}")
        
        if DEBUG:
            if j == 1:
                break
        else:
            if event_elements is None:
                break
        
        links = []
        for event in event_elements:
            link = event.find_element(By.TAG_NAME, "a").get_attribute("href")
            links.append(link)

        # TODO: check for duplicates in the DB before
        # match the link to the url in the events table


        # iterate over events
        for link in links[:3]:
            devent = {'source_id': col_names.index("id")}
            try:
                # link = event.find_element(By.TAG_NAME, "a").get_attribute("href")
                logger.debug(f"Link: {link}")
                devent['link'] = link
                logger.info(f"Event dict so far: {devent}")

            except AttributeError:
                # Skip events with missing data
                logger.error("Skipping event with missing data")
                continue

            try:
                driver.get(link)
                time.sleep(randint(2, 6))
                # Extract additional data
                # title
                try:
                    title = driver.find_element(By.CLASS_NAME, "page-event-header-title").text.strip()
                    devent['title'] = title
                    logger.info(f'event title: {title}')
                except:
                    devent['title'] = ""
                    logger.debug(f"Event dict so far: {devent}")
                
                # location
                try:
                    location = driver.find_element(By.CSS_SELECTOR, "div.text").text.strip()
                    devent['location'] = location
                    logger.info(f'event location: {location}')
                except:
                    devent['location'] = ""
                    logger.debug(f"Event dict so far: {devent}")

                # date
                try:
                    date = driver.find_element(By.XPATH, "/html/body/div/div/main/div[1]/div[2]/section[1]/div[2]/div[3]/div[1]/div[2]").text.strip()
                    devent['date'] = date
                    logger.info(f'event date: {date}')
                except:
                    devent['date'] = ""
                    logger.debug(f"Event dict so far: {devent}")

                # time
                try:
                    etime = driver.find_element(By.XPATH, "/html/body/div/div/main/div[1]/div[2]/section[1]/div[2]/div[3]/div[2]/div[2]").text.strip()
                    devent['time'] = etime
                    logger.info(f'event time: {etime}')
                except:
                    devent['time'] = ""
                    logger.debug(f"Event dict so far: {devent}")

            except Exception as e:
                logger.error(f"Error scraping event: {e}")
                logger.debug(f"Event dict so far: {devent}")
            
            driver.back()
            time.sleep(randint(2, 6))

            # insert event into the database
            sqlDB.insert_event(devent)

            # append to json too
            with open("eventLinks.json", "a", encoding="utf-8") as f:
                f.write(",\n")
                json.dump(devent, f, ensure_ascii=False, indent=4)
        j += 1
        # replace the url string "page1" with "page{j+1}"
        url = url.replace(f"page={j}", f"page={j+1}")

driver.quit()
