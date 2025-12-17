import pandas as pd
from sentiment.analyzer import analyze_sentiment
from nlp.translators import translate_to_english
import numpy as np

def compare_sentiment(original_sentiment, translated_sentiment):
    """
    Compare sentiment across different languages and media sources.

    Parameters:
    original_sentiment (dict): Sentiment scores in original languages
    translated_sentiment (dict): Sentiment scores in translated English

    Returns:
    pd.DataFrame: Comparison dataframe with sentiment shifts and bias metrics
    """
    comparison_results = []
    
    for source in original_sentiment.keys():
        orig_scores = original_sentiment[source]
        trans_scores = translated_sentiment[source]
        
        for idx, (orig, trans) in enumerate(zip(orig_scores, trans_scores)):
            sentiment_shift = trans['score'] - orig['score']
            comparison_results.append({
                'source': source,
                'headline_id': idx,
                'original_sentiment': orig['score'],
                'original_label': orig['label'],
                'translated_sentiment': trans['score'],
                'translated_label': trans['label'],
                'sentiment_shift': sentiment_shift,
                'language': orig.get('language', 'unknown')
            })
    
    return pd.DataFrame(comparison_results)

def calculate_source_bias(comparison_df):
    """
    Calculate media bias by comparing average sentiment across sources.

    Parameters:
    comparison_df (pd.DataFrame): Comparison dataframe

    Returns:
    dict: Bias metrics per source
    """
    bias_metrics = {}
    
    for source in comparison_df['source'].unique():
        source_data = comparison_df[comparison_df['source'] == source]
        
        bias_metrics[source] = {
            'avg_original_sentiment': source_data['original_sentiment'].mean(),
            'avg_translated_sentiment': source_data['translated_sentiment'].mean(),
            'avg_sentiment_shift': source_data['sentiment_shift'].mean(),
            'std_deviation': source_data['sentiment_shift'].std(),
            'positive_count': (source_data['translated_label'] == 'POSITIVE').sum(),
            'negative_count': (source_data['translated_label'] == 'NEGATIVE').sum(),
            'neutral_count': (source_data['translated_label'] == 'NEUTRAL').sum(),
        }
    
    return bias_metrics

def find_sentiment_divergence(comparison_df):
    
    divergence_threshold = 0.5
    high_divergence = comparison_df[
        abs(comparison_df['sentiment_shift']) > divergence_threshold
    ].sort_values('sentiment_shift', ascending=False)
    
    return high_divergence

def visualize_sentiment_comparison(comparison_df, bias_metrics):
    
    viz_data = {
        'comparison_df': comparison_df,
        'bias_metrics': bias_metrics,
        'source_names': list(bias_metrics.keys()),
        'avg_sentiments': [bias_metrics[s]['avg_translated_sentiment'] for s in bias_metrics.keys()],
        'sentiment_shifts': [bias_metrics[s]['avg_sentiment_shift'] for s in bias_metrics.keys()]
    }
    
    return viz_data

# Example usage
if __name__ == "__main__":
    headlines = {
        "Times of India": [
            {"text": "Accident on highway", "score": -0.7, "label": "NEGATIVE", "language": "en"},
            {"text": "Sports victory celebrated", "score": 0.8, "label": "POSITIVE", "language": "en"}
        ],
        "Vijaya Karnataka": [
            {"text": "Accident on highway", "score": -0.6, "label": "NEGATIVE", "language": "en"},
            {"text": "Sports victory celebrated", "score": 0.9, "label": "POSITIVE", "language": "en"}
        ]
    }
    
    comparison = compare_sentiment(headlines, headlines)
    bias = calculate_source_bias(comparison)
    divergence = find_sentiment_divergence(comparison)
    
    print(comparison)
    print("\nBias Metrics:")
    print(bias)