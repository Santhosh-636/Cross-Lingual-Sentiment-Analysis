import requests
import xml.etree.ElementTree as ET

def scrape_times_of_india():
    url = "https://timesofindia.indiatimes.com/rssfeedstopstories.cms"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print("TOI RSS request failed:", e)
        return []

    headlines = []
    root = ET.fromstring(response.content)
    for item in root.findall('.//item')[:20]:
        title = item.find('title').text
        link = item.find('link').text
        headlines.append({'Headline': title, 'Link': link, 'Language': 'en'})

    return headlines

if __name__ == "__main__":
    for h in scrape_times_of_india():
        print(h)
