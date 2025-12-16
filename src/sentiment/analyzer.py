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
        nlp = pipeline('sentiment-analysis')
        for h in headlines:
            text = h.get('headline')
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
    except Exception:
        # fallback
        try:
            from textblob import TextBlob
            for h in headlines:
                text = h.get('headline')
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
        except Exception:
            # last resort: neutral
            for h in headlines:
                r = dict(h)
                r.update({'sentiment_score': 0.0, 'sentiment_label': 'NEUTRAL', 'confidence': 0.0})
                results.append(r)
            return results