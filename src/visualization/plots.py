import matplotlib.pyplot as plt
import pandas as pd

def plot_sentiment_distribution(sentiment_data):
    """
    Plots the distribution of sentiment scores across different languages.
    
    Parameters:
    sentiment_data (DataFrame): A pandas DataFrame containing sentiment scores and corresponding languages.
    """
    plt.figure(figsize=(10, 6))
    sentiment_data.groupby('language')['sentiment_score'].mean().plot(kind='bar', color='skyblue')
    plt.title('Average Sentiment Score by Language')
    plt.xlabel('Language')
    plt.ylabel('Average Sentiment Score')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def plot_sentiment_trends(sentiment_trends):
    """
    Plots sentiment trends over time for different languages.
    
    Parameters:
    sentiment_trends (DataFrame): A pandas DataFrame containing date, sentiment scores, and languages.
    """
    plt.figure(figsize=(12, 6))
    for language in sentiment_trends['language'].unique():
        subset = sentiment_trends[sentiment_trends['language'] == language]
        plt.plot(subset['date'], subset['sentiment_score'], marker='o', label=language)
    
    plt.title('Sentiment Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sentiment Score')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def plot_media_bias(bias_data):
    """
    Plots the detected media bias based on sentiment analysis.
    
    Parameters:
    bias_data (DataFrame): A pandas DataFrame containing media sources and their corresponding bias scores.
    """
    plt.figure(figsize=(10, 6))
    bias_data.set_index('media_source')['bias_score'].plot(kind='bar', color='salmon')
    plt.title('Media Bias Scores')
    plt.xlabel('Media Source')
    plt.ylabel('Bias Score')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()