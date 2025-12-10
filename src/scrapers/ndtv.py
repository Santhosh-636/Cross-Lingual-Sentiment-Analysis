import requests
from bs4 import BeautifulSoup

def scrape_ndtv_headlines():
    url = 'https://www.ndtv.com/'
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}")

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    for item in soup.find_all('h2', class_='newsHdng'):
        headline = item.get_text(strip=True)
        link = item.find('a')['href']
        headlines.append({'headline': headline, 'link': link})

    return headlines

def scrape_ndtv_metadata():
    # This function can be expanded to scrape additional metadata if needed
    return None

if __name__ == "__main__":
    headlines = scrape_ndtv_headlines()
    for headline in headlines:
        print(headline)