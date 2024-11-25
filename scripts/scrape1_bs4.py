import requests
from bs4 import BeautifulSoup
import json

# Dynamic sites cannot be scraped using BeautifulSoup, and visitalgarve is dynamic page

# URL to scrape
url = "https://eventos.visitalgarve.pt/pt/agenda?category=1341"

# Request the page
response = requests.get(url)
if response.status_code != 200:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    exit()

# Parse the page content
soup = BeautifulSoup(response.text, "html.parser")
# for child in soup.descendants:
#     if child.name:
#         print(child.name)

events = []
event_elements = soup.find_all("div", class_="common-items-card")  # Adjust class as per the actual HTML

for event in event_elements:
    try:
        link = event.find("a")["href"]  # Adjust class
        # title = event.find("h2", class_="event-title-class").text.strip()  # Adjust class
        # date = event.find("span", class_="event-date-class").text.strip()  # Adjust class
        # location = event.find("span", class_="event-location-class").text.strip()  # Adjust class
        # description = event.find("p", class_="event-description-class").text.strip()  # Adjust class

        events.append({
            "link": link,
            # "date": date,
            # "location": location,
            # "description": description,
        })
    except AttributeError:
        # Skip events with missing data
        print("Skipping event with missing data")
        continue

print(event_elements, events)

# save soup to a file
with open("visitalgarve.html", "w", encoding="utf-8") as f:
    f.write(str(soup))