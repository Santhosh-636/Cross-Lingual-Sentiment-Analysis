import requests
from bs4 import BeautifulSoup

def scrape_times_of_india():
    url = 'https://timesofindia.indiatimes.com/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []

    # Collect possible headline tags and anchors
    for tag in soup.find_all(['h2', 'h3', 'a']):
        text = tag.get_text(strip=True)
        if not text or len(text) < 10:
            continue
        link = None
        a = tag.find('a') if tag.name != 'a' else tag
        if a and a.has_attr('href'):
            link = a['href']
        headlines.append({'headline': text, 'link': link, 'language': 'en'})

    # Deduplicate
    seen = set()
    out = []
    for h in headlines:
        if h['headline'] in seen:
            continue
        seen.add(h['headline'])
        out.append(h)

    return out[:20]


if __name__ == "__main__":
    for h in scrape_times_of_india():
        print(h)