import requests
from bs4 import BeautifulSoup

def scrape_dinamani_headlines():
    url = 'https://www.dinamani.com/'
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to retrieve data from Dinamani")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    # Assuming headlines are contained in <h2> tags with a specific class
    for item in soup.find_all('h2', class_='headline-class'):  # Replace 'headline-class' with actual class
        headlines.append(item.get_text(strip=True))

    return headlines

def main():
    headlines = scrape_dinamani_headlines()
    for headline in headlines:
        print(headline)

if __name__ == "__main__":
    main()