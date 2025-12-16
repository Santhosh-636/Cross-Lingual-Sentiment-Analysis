import requests
from bs4 import BeautifulSoup

def scrape_dinamani_headlines():
    url = 'https://www.dinamani.com/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    headlines = []

    for tag in soup.find_all(['h2', 'h3', 'a']):
        text = tag.get_text(strip=True)
        if not text or len(text) < 8:
            continue
        link = None
        a = tag.find('a') if tag.name != 'a' else tag
        if a and a.has_attr('href'):
            link = a['href']
        headlines.append({'headline': text, 'link': link, 'language': 'ta'})

    seen = set()
    out = []
    for h in headlines:
        if h['headline'] in seen:
            continue
        seen.add(h['headline'])
        out.append(h)

    return out[:20]


if __name__ == "__main__":
    for h in scrape_dinamani_headlines():
        print(h)