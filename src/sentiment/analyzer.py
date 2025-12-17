class SentimentAnalyzer:
    def __init__(self, model):
        self.model = model

    def analyze_sentiment(self, headlines):
        sentiments = []
        for headline in headlines:
            sentiment = self.model.predict(headline)
            sentiments.append(sentiment)
        return sentiments

    def compare_sentiments(self, sentiments_a, sentiments_b):
        comparison = {
            'positive': sum(1 for s in sentiments_a if s == 'positive') - sum(1 for s in sentiments_b if s == 'positive'),
            'negative': sum(1 for s in sentiments_a if s == 'negative') - sum(1 for s in sentiments_b if s == 'negative'),
            'neutral': sum(1 for s in sentiments_a if s == 'neutral') - sum(1 for s in sentiments_b if s == 'neutral'),
        }
        return comparison

    def sentiment_shift(self, sentiments_over_time):
        shift = {}
        for time_period, sentiments in sentiments_over_time.items():
            shift[time_period] = {
                'positive': sum(1 for s in sentiments if s == 'positive'),
                'negative': sum(1 for s in sentiments if s == 'negative'),
                'neutral': sum(1 for s in sentiments if s == 'neutral'),
            }
        return shift


def analyze_headlines(headlines):
    """Given a list of headline dicts with key 'headline', return list of dicts
    with sentiment score and label (POSITIVE/NEGATIVE/NEUTRAL). Uses
    transformers pipeline if available, else falls back to TextBlob polarity.
    """
    results = []
    try:
        from transformers import pipeline
        print('[*] Using transformers pipeline for sentiment')
        nlp = pipeline('sentiment-analysis')
        for h in headlines:
            text = h.get('headline')
            if not text:
                r = dict(h)
                r.update({'sentiment_score': 0.0, 'sentiment_label': 'NEUTRAL', 'confidence': 0.0})
                results.append(r)
                continue
            out = nlp(text[:512])[0]
            label = out['label']
            score = out.get('score', 0.0)
            # normalize to -1..1
            if label.upper().startswith('NEG'):
                norm = -score
                mapped = 'NEGATIVE'
            elif label.upper().startswith('POS'):
                norm = score
                mapped = 'POSITIVE'
            else:
                norm = 0.0
                mapped = 'NEUTRAL'
            r = dict(h)
            r.update({'sentiment_score': norm, 'sentiment_label': mapped, 'confidence': score})
            results.append(r)
        return results
    except Exception as e:
        print(f"[!] transformers pipeline failed: {e}")
        # fallback
        try:
            from textblob import TextBlob
            print('[*] Using TextBlob fallback for sentiment')
            for h in headlines:
                text = h.get('headline') or ''
                if not text:
                    r = dict(h)
                    r.update({'sentiment_score': 0.0, 'sentiment_label': 'NEUTRAL', 'confidence': 0.0})
                    results.append(r)
                    continue
                tb = TextBlob(text)
                pol = tb.sentiment.polarity
                if pol > 0.1:
                    mapped = 'POSITIVE'
                elif pol < -0.1:
                    mapped = 'NEGATIVE'
                else:
                    mapped = 'NEUTRAL'
                r = dict(h)
                r.update({'sentiment_score': pol, 'sentiment_label': mapped, 'confidence': abs(pol)})
                results.append(r)
            return results
        except Exception as e2:
            print(f"[!] TextBlob fallback failed: {e2}")
            print('[*] Using rule-based fallback for sentiment')
            # Rule-based fallback: simple keyword matching with weights
            negative_keywords = {
                'bomb': 1.0, 'blast': 1.0, 'attack': 1.0, 'killed': 0.9, 'dies': 0.9,
                'death': 1.0, 'murder': 1.0, 'fire': 0.8, 'crash': 0.8, 'accident': 0.7,
                'violence': 0.9, 'clash': 0.7, 'protest': 0.4, 'injured': 0.8, 'shooting': 1.0,
                'suffocating': 0.6, 'attack':1.0, 'terror':1.0
            }
            positive_keywords = {
                'win': 0.8, 'victory': 0.9, 'celebrated': 0.6, 'honours': 0.5, 'launch': 0.3,
                'introduced': 0.2, 'new': 0.1
            }
            def rule_score(text):
                if not text:
                    return 0.0
                low = text.lower()
                score = 0.0
                for kw, w in negative_keywords.items():
                    if kw in low:
                        score -= w
                for kw, w in positive_keywords.items():
                    if kw in low:
                        score += w
                # clamp
                if score > 1.0:
                    score = 1.0
                if score < -1.0:
                    score = -1.0
                return score

            for h in headlines:
                text = h.get('headline') or ''
                pol = rule_score(text)
                if pol > 0.1:
                    mapped = 'POSITIVE'
                elif pol < -0.1:
                    mapped = 'NEGATIVE'
                else:
                    mapped = 'NEUTRAL'
                r = dict(h)
                r.update({'sentiment_score': pol, 'sentiment_label': mapped, 'confidence': abs(pol)})
                results.append(r)
            return results