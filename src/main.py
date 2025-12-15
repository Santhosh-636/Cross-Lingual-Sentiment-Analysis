import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from datetime import datetime

print("\n" + "="*100)
print(" "*30 + "🌍 CROSS-LINGUAL SENTIMENT ANALYSIS 🌍")
print("="*100)
print(f"📅 Analysis Date: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}")
print("="*100 + "\n")

# Sample data instead of scraping
headlines = {
    'times_of_india': [
        {'text': 'Accident on highway kills 5', 'language': 'en', 'score': -0.8, 'label': 'NEGATIVE'},
        {'text': 'India wins cricket match', 'language': 'en', 'score': 0.9, 'label': 'POSITIVE'}
    ],
    'ndtv': [
        {'text': 'Highway accident claims lives', 'language': 'en', 'score': -0.7, 'label': 'NEGATIVE'},
        {'text': 'India cricket victory celebrated', 'language': 'en', 'score': 0.85, 'label': 'POSITIVE'}
    ],
    'vijaya_karnataka': [
        {'text': 'ಹೆದ್ದಾರಿಯಲ್ಲಿ ಅಪಘಾತ', 'language': 'kn', 'score': -0.75, 'label': 'NEGATIVE'},
        {'text': 'ಭಾರತ ಕ್ರಿಕೆಟ್ ಗೆಲ್ಪು', 'language': 'kn', 'score': 0.88, 'label': 'POSITIVE'}
    ],
    'dinamani': [
        {'text': 'பாதைபோக்கு விபத்து', 'language': 'ta', 'score': -0.72, 'label': 'NEGATIVE'},
        {'text': 'இந்தியா கிரிக்கெட் வெற்றி', 'language': 'ta', 'score': 0.90, 'label': 'POSITIVE'}
    ]
}

total_headlines = sum(len(h) for h in headlines.values())
print(f"✅ Data Status: Loaded {total_headlines} headlines from 4 news sources\n")

# Simple comparison
comparison_results = []
for source, articles in headlines.items():
    for idx, article in enumerate(articles):
        comparison_results.append({
            'source': source,
            'headline': article['text'],
            'language': article['language'],
            'sentiment_score': article['score'],
            'sentiment_label': article['label']
        })

df = pd.DataFrame(comparison_results)

# Display headlines table
print("\n" + "="*100)
print("📰 HEADLINE SENTIMENT ANALYSIS")
print("="*100)
print()

for source in df['source'].unique():
    print(f"\n🏢 {source.upper().replace('_', ' ')}")
    print("-" * 100)
    
    source_df = df[df['source'] == source]
    for idx, row in source_df.iterrows():
        emoji = "😔" if row['sentiment_label'] == 'NEGATIVE' else "😊" if row['sentiment_label'] == 'POSITIVE' else "😐"
        score_bar = "█" * int((row['sentiment_score'] + 1) * 25) + "░" * (50 - int((row['sentiment_score'] + 1) * 25))
        
        print(f"  {emoji} [{row['language'].upper()}] {row['headline']}")
        print(f"     Score: {score_bar} {row['sentiment_score']:+.2f} ({row['sentiment_label']})")
        print()

# Calculate and display bias analysis
print("\n" + "="*100)
print("📊 MEDIA BIAS ANALYSIS")
print("="*100 + "\n")

bias_data = []
for source in sorted(df['source'].unique()):
    source_data = df[df['source'] == source]
    avg_sentiment = source_data['sentiment_score'].mean()
    positive_count = (source_data['sentiment_label'] == 'POSITIVE').sum()
    negative_count = (source_data['sentiment_label'] == 'NEGATIVE').sum()
    
    bias_data.append({
        'Source': source.replace('_', ' ').title(),
        'Avg Sentiment': f"{avg_sentiment:+.3f}",
        'Positive': positive_count,
        'Negative': negative_count,
        'Bias Indicator': "↑ Positive Bias" if avg_sentiment > 0.05 else "↓ Negative Bias" if avg_sentiment < -0.05 else "→ Neutral"
    })

bias_df = pd.DataFrame(bias_data)
print(bias_df.to_string(index=False))

# print("\n" + "="*100)
# print("🎯 KEY FINDINGS")
# print("="*100 + "\n")

max_bias_source = bias_df.loc[bias_df['Avg Sentiment'].str.replace('+', '').astype(float).idxmax()]
min_bias_source = bias_df.loc[bias_df['Avg Sentiment'].str.replace('+', '').astype(float).idxmin()]

# print(f"  ✅ Most Positive Coverage: {max_bias_source['Source']} ({max_bias_source['Avg Sentiment']})")
# print(f"  ⚠️  Most Negative Coverage: {min_bias_source['Source']} ({min_bias_source['Avg Sentiment']})")
# print(f"  📈 Overall Average Sentiment: {df['sentiment_score'].mean():+.3f}")
# print(f"  🌐 Languages Analyzed: English, Kannada, Tamil")

# print("\n" + "="*100)
# print("✨ Analysis Complete! Check reports/ folder for detailed findings.")
# print("="*100 + "\n")