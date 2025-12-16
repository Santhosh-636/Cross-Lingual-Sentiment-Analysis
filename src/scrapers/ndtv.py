import requests
from bs4 import BeautifulSoup

def scrape_ndtv_headlines():
    url = 'https://www.ndtv.com/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    # NDTV uses h2 elements with class that may vary; search for common patterns
    for item in soup.find_all(['h2', 'h3', 'a']):
        text = item.get_text(strip=True)
        if not text or len(text) < 10:
            continue
        link = None
        a = item.find('a') if item.name != 'a' else item
        if a and a.has_attr('href'):
            link = a['href']
        headlines.append({'headline': text, 'link': link, 'language': 'en'})

    # Deduplicate while preserving order
    seen = set()
    filtered = []
    for h in headlines:
        if h['headline'] in seen:
            continue
        seen.add(h['headline'])
        filtered.append(h)

    return filtered[:20]


if __name__ == "__main__":
    for h in scrape_ndtv_headlines():
        print(h)