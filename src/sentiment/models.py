from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

class SentimentModel(BaseEstimator, ClassifierMixin):
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.classifier = LogisticRegression()

    def fit(self, X, y):
        X_vectorized = self.vectorizer.fit_transform(X)
        self.classifier.fit(X_vectorized, y)
        return self

    def predict(self, X):
        X_vectorized = self.vectorizer.transform(X)
        return self.classifier.predict(X_vectorized)

    def evaluate(self, X, y):
        X_vectorized = self.vectorizer.transform(X)
        predictions = self.classifier.predict(X_vectorized)
        return classification_report(y, predictions)

def load_data(file_path):
    data = pd.read_csv(file_path)
    return data['headline'], data['sentiment']

def train_model(data_file):
    X, y = load_data(data_file)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = SentimentModel()
    model.fit(X_train, y_train)
    
    report = model.evaluate(X_test, y_test)
    print(report)
    
    return model