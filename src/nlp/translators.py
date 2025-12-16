def translate_text(text, target_language):
    try:
        from googletrans import Translator
        translator = Translator()
        res = translator.translate(text, dest=target_language)
        return res.text
    except Exception:
        # fallback: return original text if translation fails
        return text

def translate_headlines(headlines, target_language):
    translated_headlines = []
    for headline in headlines:
        translated_headline = translate_text(headline, target_language)
        translated_headlines.append(translated_headline)
    return translated_headlines

def detect_language(text):
    try:
        from googletrans import Translator
        translator = Translator()
        res = translator.detect(text)
        return res.lang
    except Exception:
        return 'en'

def translate_to_all_languages(headlines):
    languages = ['en', 'hi', 'bn', 'kn']  # English, Hindi, Bengali, Kannada
    translated_results = {}
    
    for lang in languages:
        translated_results[lang] = translate_headlines(headlines, lang)
    
    return translated_results