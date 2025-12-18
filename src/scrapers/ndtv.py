import requests
import xml.etree.ElementTree as ET

def scrape_ndtv_headlines():
    url = "https://feeds.feedburner.com/ndtvnews-top-stories"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("NDTV RSS request failed:", e)
        return []

    headlines = []
    root = ET.fromstring(response.content)
    for item in root.findall('.//item')[:20]:
        title = item.find('title').text
        link = item.find('link').text
        headlines.append({'headline': title, 'link': link, 'language': 'en'})
    return headlines

if __name__ == "__main__":
    for h in scrape_ndtv_headlines():
        print(h)
