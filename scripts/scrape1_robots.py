import requests
from bs4 import BeautifulSoup

# URL of the website to check
url = "https://eventos.visitalgarve.pt/"

# Function to check robots.txt
def check_robots_txt(base_url):
    robots_url = base_url + "/robots.txt"
    try:
        response = requests.get(robots_url, timeout=10)
        if response.status_code == 200:
            print(f"robots.txt found at {robots_url}:\n")
            print(response.text)
            # Check for any 'Disallow' rules
            if "Disallow: /" in response.text:
                print("Site explicitly disallows all scraping in robots.txt.")
            elif "Disallow:" in response.text:
                print("robots.txt has some disallowed paths. Review it for specific rules.")
            else:
                print("robots.txt does not disallow scraping.")
        else:
            print(f"No robots.txt found or inaccessible. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error accessing robots.txt: {e}")

# Function to test scraping
def test_scraping(target_url):
    try:
        response = requests.get(target_url, timeout=10)
        if response.status_code == 200:
            print(f"Successfully accessed the page: {target_url}")
            # Use BeautifulSoup to parse and check content
            soup = BeautifulSoup(response.text, "html.parser")
            if soup.find("noscript") and "You need to enable JavaScript" in soup.find("noscript").text:
                print("JavaScript rendering detected. BeautifulSoup alone may not work.")
            else:
                print("Page content is accessible with BeautifulSoup.")
        else:
            print(f"Failed to access the page. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error testing scraping: {e}")

# Main script
if __name__ == "__main__":
    base_url = "https://eventos.visitalgarve.pt"
    print("Checking robots.txt...\n")
    check_robots_txt(base_url)
    print("\nTesting page scraping...\n")
    test_scraping(url)
