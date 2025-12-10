import requests
from bs4 import BeautifulSoup

def scrape_times_of_india():
    url = 'https://timesofindia.indiatimes.com/'
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}")

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []

    for item in soup.find_all('h2', class_='title'):
        headline = item.get_text(strip=True)
        headlines.append(headline)

    return headlines

if __name__ == "__main__":
    headlines = scrape_times_of_india()
    for headline in headlines:
        print(headline)