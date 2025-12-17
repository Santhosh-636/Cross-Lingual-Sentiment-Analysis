import sys
import os
import importlib
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd

# Configuration: change to True to show neutral headlines as well
# User requested sentiment/emotion for all available headlines, enable by default
SHOW_NEUTRAL = True
# minimum absolute confidence/score to consider non-neutral (0..1)
CONFIDENCE_THRESHOLD = 0.15


def try_scrape(module_name, candidates):
    """Import scraper module and try candidate functions. If none found,
    try any callable in the module starting with 'scrape'. Normalize
    output to a list of dicts with at least 'headline' and 'language'."""
    lang_map = {
        'times_of_india': 'en',
        'ndtv': 'en',
        'vijaya_karnataka': 'kn',
        'dinamani': 'ta'
    }

    try:
        mod = importlib.import_module(f"scrapers.{module_name}")
    except Exception:
        return None

    # Try explicit candidate names first
    for fn in candidates:
        if hasattr(mod, fn):
            try:
                out = getattr(mod, fn)()
                return normalize_scraper_output(out, lang_map.get(module_name, 'en'))
            except Exception:
                continue

    # Fallback: find any callable starting with 'scrape'
    for name in dir(mod):
        if name.startswith('scrape') and callable(getattr(mod, name)):
            try:
                out = getattr(mod, name)()
                return normalize_scraper_output(out, lang_map.get(module_name, 'en'))
            except Exception:
                continue

    return None


def normalize_scraper_output(out, default_lang='en'):
    """Convert various scraper return types into a list of dicts.
    Accepts list[str], list[dict], single dict, or None."""
    if not out:
        return None

    results = []
    if isinstance(out, dict):
        out = [out]

    if isinstance(out, (list, tuple)):
        for item in out:
            if isinstance(item, str):
                results.append({'headline': item, 'language': default_lang})
            elif isinstance(item, dict):
                # Ensure headline key exists
                headline = item.get('headline') or item.get('text') or item.get('title')
                if not headline:
                    continue
                row = {'headline': headline, 'language': item.get('language', default_lang)}
                if 'link' in item:
                    row['link'] = item['link']
                results.append(row)
    return results


def is_meaningful_headline(text):
    """Heuristic filter to exclude nav links, single-word places, and very short items."""
    if not text or len(text.strip()) < 8:
        return False
    low = text.lower()
    # exclude obvious nav items
    for bad in ('live', 'live videos', 'videos', 'photos', 'latest', 'more', 'home'):
        if low.strip() == bad or low.startswith(bad + ' '):
            return False
    # require at least 3 words or contain event keywords
    words = [w for w in low.split() if w.isalpha()]
    if len(words) >= 3 or len(text) >= 30:
        return True
    event_keywords = ('bomb','blast','attack','killed','dies','death','murder','fire','crash','accident','violence','clash','protest','win','victory','dead','injured','shooting')
    for kw in event_keywords:
        if kw in low:
            return True
    return False


def infer_emotion(headline, sentiment_score):
    """Map sentiment score + headline keywords to human-readable emotion label."""
    low = headline.lower()
    event_keywords_fear = ('bomb','blast','attack','shooting','explosion')
    if sentiment_score <= -0.5:
        base = 'Sad'
    elif sentiment_score < -0.15:
        base = 'Sad'
    elif sentiment_score <= 0.15:
        base = 'Neutral'
    elif sentiment_score <= 0.5:
        base = 'Happy'
    else:
        base = 'Very Happy'

    for kw in event_keywords_fear:
        if kw in low and base != 'Very Happy':
            return base + '/Fear'
    return base


def has_event_keyword(text):
    if not text:
        return False
    low = text.lower()
    event_keywords = ('bomb','blast','attack','killed','dies','death','murder','fire','crash','accident','violence','clash','protest','injured','shooting','explosion','blast','terror')
    return any(kw in low for kw in event_keywords)

# Attempt to scrape; fall back to sample data if scraper missing/failing
headlines = {}
sources = [
    ('times_of_india', ['scrape_toi', 'scrape_times_of_india']),
    ('ndtv', ['scrape_ndtv', 'scrape_ndtv_headlines']),
    ('vijaya_karnataka', ['scrape_vijaya', 'scrape_vijaya_karnataka']),
    ('dinamani', ['scrape_dinamani', 'scrape_dinamani_headlines'])
]

# default sample fallback (kept for offline/demo)
sample_fallback = {
    'times_of_india': [
        {'headline': 'Accident on highway kills 5', 'language': 'en'} ,
        {'headline': 'India wins cricket match', 'language': 'en'}
    ],
    'ndtv': [
        {'headline': 'Highway accident claims lives', 'language': 'en'},
        {'headline': 'India cricket victory celebrated', 'language': 'en'}
    ],
    'vijaya_karnataka': [
        {'headline': 'ಹೆದ್ದಾರಿಯಲ್ಲಿ ಅಪಘಾತ', 'language': 'kn'},
        {'headline': 'ಭಾರತ ಕ್ರಿಕೆಟ್ ಗೆಲ್ಪು', 'language': 'kn'}
    ],
    'dinamani': [
        {'headline': 'பாதைபோக்கு விபத்து', 'language': 'ta'},
        {'headline': 'இந்தியா கிரிக்கெட் வெற்றி', 'language': 'ta'}
    ]
}

raw_outputs = {}
for name, candidates in sources:
    out = try_scrape(name, candidates)
    if not out:
        print(f"[!] Scraper '{name}' returned no results; using fallback sample")
        out = sample_fallback.get(name, [])
        used_fallback = True
    else:
        print(f"[+] Scraper '{name}' returned {len(out)} items")
        used_fallback = False
    # store raw output and the fallback flag for inspection
    raw_outputs[name] = {'items': out, 'used_fallback': used_fallback}
    headlines[name] = out

# save raw outputs for debugging
import json
reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
os.makedirs(reports_dir, exist_ok=True)
raw_path = os.path.join(reports_dir, 'raw_headlines.json')
with open(raw_path, 'w', encoding='utf-8') as rf:
    json.dump(raw_outputs, rf, ensure_ascii=False, indent=2)
print(f"Saved raw scraper outputs to: {os.path.abspath(raw_path)}")

# Build dataframe (expect scrapers to return list of dicts with 'text' or 'headline')
rows = []
for source, items in headlines.items():
    for i, it in enumerate(items):
        text = it.get('text') or it.get('headline') or str(it)
        score = it.get('score', 0.0)
        label = it.get('label', 'NEUTRAL')
        lang = it.get('language', it.get('lang', 'en'))
        rows.append({'source': source, 'headline': text, 'language': lang, 'sentiment_score': score, 'sentiment_label': label})

df = pd.DataFrame(rows)
from nlp.translators import translate_text, detect_language
from sentiment.analyzer import analyze_headlines

# If headlines are not yet analyzed, translate non-English and analyze sentiment
enriched = {}
for src, items in headlines.items():
    # items are list of dicts with 'headline' and 'language'
    to_analyze = []
    for it in items:
        h = dict(it)
        # ensure language detection if missing
        lang = h.get('language') or detect_language(h.get('headline', ''))
        h['language'] = lang
        if lang != 'en':
            # translate to English for sentiment analysis
            try:
                h['translated_headline'] = translate_text(h['headline'], 'en')
            except Exception:
                h['translated_headline'] = h['headline']
        else:
            h['translated_headline'] = h['headline']
        to_analyze.append(h)
    # analyze sentiment on translated text
    # prepare input with translated headline in 'headline' key for analyzer
    analyzer_input = [{'headline': t['translated_headline'], 'language': t['language']} for t in to_analyze]
    analyzed = analyze_headlines(analyzer_input)
    # merge back sentiment into original items
    merged = []
    for orig, a in zip(to_analyze, analyzed):
        merged_item = dict(orig)
        merged_item.update({'sentiment_score': a.get('sentiment_score', 0.0), 'sentiment_label': a.get('sentiment_label', 'NEUTRAL'), 'confidence': a.get('confidence', 0.0)})
        merged.append(merged_item)
    enriched[src] = merged

# rebuild dataframe from enriched data
rows = []
for source, items in enriched.items():
    for r in items:
        rows.append({'source': source, 'headline': r.get('headline'), 'translated_headline': r.get('translated_headline'), 'language': r.get('language'), 'sentiment_score': r.get('sentiment_score', 0.0), 'sentiment_label': r.get('sentiment_label', 'NEUTRAL'), 'confidence': r.get('confidence', 0.0), 'link': r.get('link')})

df = pd.DataFrame(rows)

# Terminal-only formatted output (no web page, no browser)
print("\n" + "="*80)
print("CROSS-LINGUAL SENTIMENT ANALYSIS — TERMINAL REPORT")
print("Generated:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print("="*80 + "\n")

print("HEADLINES\n" + "-"*80)
for src in df['source'].unique():
    print(f"\n{src.replace('_',' ').upper()}")
    print("-"*40)
    sub = df[df['source'] == src]
    # filter to meaningful headlines for display and remove neutral/noisy items
    rows_list = list(sub.to_dict('records'))
    filtered = []
    for r in rows_list:
        text = (r.get('translated_headline') or r.get('headline') or '').strip()
        if not is_meaningful_headline(text):
            continue
        score = r.get('sentiment_score', 0.0)
        conf = abs(score)
        # include if strong sentiment or contains event keyword, or if SHOW_NEUTRAL enabled
        if SHOW_NEUTRAL or conf >= CONFIDENCE_THRESHOLD or has_event_keyword(text):
            filtered.append(r)

    if not filtered:
        print("  No strong emotion-bearing headlines found.")
    else:
        for r in filtered:
            orig = r.get('headline')
            trans = r.get('translated_headline')
            score = r.get('sentiment_score', 0.0)
            label = r.get('sentiment_label', 'NEUTRAL')
            emotion = infer_emotion(trans or orig, score)
            # concise output
            print(f"  - {orig}")
            if trans and trans != orig:
                print(f"     (Translated) {trans}")
            print(f"     People emotions: {emotion}  — Score: {score:+.2f}")
    print()

print("\n" + "="*80)
print("MEDIA BIAS SUMMARY\n" + "-"*80)
for src in sorted(df['source'].unique()):
    sub = df[df['source'] == src]
    avg = sub['sentiment_score'].mean()
    pos = (sub['sentiment_label'] == 'POSITIVE').sum()
    neg = (sub['sentiment_label'] == 'NEGATIVE').sum()
    print(f"{src.replace('_',' ').title():25} Avg: {avg:+.3f}   +:{pos}  -:{neg}")

print("\n" + "="*80)
print("KEY METRICS")
print("- Total headlines:", len(df))
print("- Sources:", df['source'].nunique())
print("- Languages:", ', '.join(sorted(df['language'].unique())))
print("- Overall average sentiment:", f"{df['sentiment_score'].mean():+.3f}")
print("="*80 + "\n")

# Optional: save a plain text summary file
out_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
os.makedirs(out_dir, exist_ok=True)
summary_path = os.path.join(out_dir, 'terminal_report.txt')
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write("Cross-Lingual Sentiment Analysis — Terminal Report\n")
    f.write("Generated: " + datetime.now().isoformat() + "\n\n")
    f.write(df.to_string(index=False))
    f.write("\n\nMedia bias summary\n")
    for src in sorted(df['source'].unique()):
        sub = df[df['source'] == src]
        avg = sub['sentiment_score'].mean()
        pos = (sub['sentiment_label'] == 'POSITIVE').sum()
        neg = (sub['sentiment_label'] == 'NEGATIVE').sum()
        f.write(f"{src}: Avg {avg:+.3f}  +:{pos}  -:{neg}\n")

print(f"Plain-text summary saved to: {os.path.abspath(summary_path)}")