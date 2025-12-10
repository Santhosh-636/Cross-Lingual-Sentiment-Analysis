from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_distances
import numpy as np

class BiasDetector:
    def __init__(self, headlines):
        self.headlines = headlines
        self.vectorizer = CountVectorizer()
        self.vectorized_data = self.vectorizer.fit_transform(headlines)

    def detect_bias(self):
        # Calculate pairwise distances between headlines
        distances = pairwise_distances(self.vectorized_data.toarray(), metric='cosine')
        bias_scores = np.mean(distances, axis=1)
        return bias_scores

    def analyze_bias(self):
        bias_scores = self.detect_bias()
        bias_analysis = {headline: score for headline, score in zip(self.headlines, bias_scores)}
        return bias_analysis

    def get_biased_headlines(self, threshold=0.5):
        bias_analysis = self.analyze_bias()
        biased_headlines = {headline: score for headline, score in bias_analysis.items() if score > threshold}
        return biased_headlines