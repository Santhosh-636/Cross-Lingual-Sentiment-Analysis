import os
from scrapers.times_of_india import scrape_times_of_india
from scrapers.vijaya_karnataka import scrape_vijaya_karnataka
from scrapers.ndtv import scrape_ndtv
from scrapers.dinamani import scrape_dinamani
from sentiment.analyzer import SentimentAnalyzer
from nlp.translators import translate_text
from database.db_handler import DatabaseHandler
from analysis.comparison import compare_sentiment
from visualization.plots import plot_sentiment_analysis

def main():
    # Create a database handler instance
    db_handler = DatabaseHandler()

    # Scrape news headlines from different sources
    toi_headlines = scrape_times_of_india()
    vk_headlines = scrape_vijaya_karnataka()
    ndtv_headlines = scrape_ndtv()
    dinamani_headlines = scrape_dinamani()

    # Store scraped headlines in the database
    db_handler.store_headlines('Times of India', toi_headlines)
    db_handler.store_headlines('Vijaya Karnataka', vk_headlines)
    db_handler.store_headlines('NDTV', ndtv_headlines)
    db_handler.store_headlines('Dinamani', dinamani_headlines)

    # Initialize the sentiment analyzer
    sentiment_analyzer = SentimentAnalyzer()

    # Analyze sentiment for each source
    toi_sentiment = sentiment_analyzer.analyze_sentiment(toi_headlines)
    vk_sentiment = sentiment_analyzer.analyze_sentiment(vk_headlines)
    ndtv_sentiment = sentiment_analyzer.analyze_sentiment(ndtv_headlines)
    dinamani_sentiment = sentiment_analyzer.analyze_sentiment(dinamani_headlines)

    # Compare sentiment across different languages and media sources
    comparison_results = compare_sentiment(toi_sentiment, vk_sentiment, ndtv_sentiment, dinamani_sentiment)

    # Plot the sentiment analysis results
    plot_sentiment_analysis(comparison_results)

if __name__ == "__main__":
    main()