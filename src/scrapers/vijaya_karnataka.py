import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_vijaya_karnataka():
    url = "https://vijaykarnataka.indiatimes.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = 'utf-8'  # Ensure UTF-8 decoding
    except Exception as e:
        print("Request failed:", e)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = []
    seen = set()

    # Scrape meaningful headlines (skip too short links)
    for a in soup.find_all('a', href=True):
        text = a.get_text(strip=True)
        if not text or len(text) < 15:
            continue

        link = urljoin(url, a['href'])

        if text not in seen:
            seen.add(text)
            headlines.append({
                'headline': text,
                'link': link,
                'language': 'kn'
            })

        if len(headlines) == 20:  # Get top 20 headlines
            break

    return headlines


if __name__ == "__main__":
    for h in scrape_vijaya_karnataka():
        print(h['headline'], h['link'])
