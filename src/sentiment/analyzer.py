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