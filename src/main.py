import sys
import os
import importlib
import html
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ---------------- CONFIG ----------------
MAX_HEADLINES_PER_SOURCE = 5
SHOW_NEUTRAL = True
# ----------------------------------------

# ---------------- HELPERS ----------------
def fix_text(text):
    """Decode HTML entities and strip."""
    if not text:
        return ""
    return html.unescape(text.strip())

def is_valid_headline(text):
    """Filter out short, single-word, or nav headlines."""
    if not text:
        return False
    text = text.strip()
    if len(text) < 15:
        return False
    if len(text.split()) < 3:
        return False
    bad_words = ('live', 'videos', 'photos', 'trending', 'home', 'latest', 'cities', 'topics')
    low = text.lower()
    return not any(low == bw or low.startswith(bw + ' ') for bw in bad_words)

def simple_emotion(score):
    """Convert numeric score to human-readable emotion."""
    if score <= -0.6:
        return "Sad"
    elif score < -0.2:
        return "Concerned"
    elif score <= 0.2:
        return "Neutral"
    elif score <= 0.6:
        return "Happy"
    else:
        return "Very Happy"

# ---------------- SCRAPER HANDLER ----------------
def try_scrape(module_name, candidates):
    """Try multiple scraping functions in a module."""
    lang_map = {
        'times_of_india': 'en',
        'ndtv': 'en',
        'vijaya_karnataka': 'kn',
        'dinamani': 'ta'
    }

    try:
        mod = importlib.import_module(f"scrapers.{module_name}")
    except Exception:
        return []

    for fn in candidates:
        if hasattr(mod, fn):
            try:
                return normalize_scraper_output(getattr(mod, fn)(), lang_map.get(module_name, 'en'))
            except Exception:
                pass

    for name in dir(mod):
        if name.startswith('scrape') and callable(getattr(mod, name)):
            try:
                return normalize_scraper_output(getattr(mod, name)(), lang_map.get(module_name, 'en'))
            except Exception:
                pass
    return []

def normalize_scraper_output(out, default_lang='en'):
    """Normalize scraper output to list of dicts with headline + language + link."""
    if not out:
        return []
    results = []
    if isinstance(out, dict):
        out = [out]
    for item in out:
        if isinstance(item, str):
            results.append({'headline': item, 'language': default_lang})
        elif isinstance(item, dict):
            headline = item.get('headline') or item.get('text') or item.get('title')
            if headline:
                results.append({
                    'headline': fix_text(headline),
                    'language': item.get('language', default_lang),
                    'link': item.get('link')
                })
    return results

# ---------------- LOAD TRANSLATION & SENTIMENT ----------------
from nlp.translators import translate_text, detect_language
from sentiment.analyzer import analyze_headlines

# ---------------- SOURCES ----------------
sources = [
    ('times_of_india', ['scrape_toi', 'scrape_times_of_india']),
    ('ndtv', ['scrape_ndtv', 'scrape_ndtv_headlines']),
    ('vijaya_karnataka', ['scrape_vijaya', 'scrape_vijaya_karnataka']),
    ('dinamani', ['scrape_dinamani', 'scrape_dinamani_headlines'])
]

# ---------------- SCRAPE ----------------
headlines = {}
for name, candidates in sources:
    items = try_scrape(name, candidates)
    if not items:
        print(f"[!] No headlines from {name}")
        continue
    # Filter valid headlines
    filtered = [h for h in items if is_valid_headline(h['headline'])]
    headlines[name] = filtered[:20]

# ---------------- SENTIMENT ----------------
enriched = {}
for src, items in headlines.items():
    prepared = []
    for it in items:
        text = it['headline']
        lang = it.get('language') or detect_language(text)
        if lang != 'en':
            try:
                translated = translate_text(text, 'en')
            except Exception:
                translated = text
        else:
            translated = text
        prepared.append({'headline': text, 'translated': translated})

    if not prepared:
        continue

    analyzed = analyze_headlines([{'headline': p['translated'], 'language': 'en'} for p in prepared])
    merged = []
    for p, a in zip(prepared, analyzed):
        merged.append({
            'headline': p['headline'],
            'translated': p['translated'],
            'sentiment_score': a.get('sentiment_score', 0.0)
        })
    enriched[src] = merged

# ---------------- OUTPUT ----------------
print("\n" + "="*80)
print("SCRAPED HEADLINES WITH EMOTION")
print("="*80 + "\n")

for source, items in enriched.items():
    print(f"--- {source.upper()} ---\n")
    count = 0
    for item in items:
        score = item['sentiment_score']
        emotion = simple_emotion(score)
        if not SHOW_NEUTRAL and emotion == "Neutral":
            continue
        print(f"Headline: {item['headline']}")
        if item['translated'] != item['headline']:
            print(f"(Translated) {item['translated']}")
        print(f"Emotion: {emotion} (Score: {score:+.2f})\n")
        count += 1
        if count >= MAX_HEADLINES_PER_SOURCE:
            break
    print()

print(f"Report generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
