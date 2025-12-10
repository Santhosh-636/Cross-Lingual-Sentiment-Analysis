import requests
from bs4 import BeautifulSoup

def scrape_vijaya_karnataka():
    url = "https://vijaykarnataka.indiatimes.com/"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to load page {url}")

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    for item in soup.find_all('h2', class_='title'):
        headline = item.get_text(strip=True)
        headlines.append(headline)

    return headlines

def main():
    headlines = scrape_vijaya_karnataka()
    for headline in headlines:
        print(headline)

if __name__ == "__main__":
    main()