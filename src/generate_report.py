import pandas as pd
from datetime import datetime
import os

def generate_html_report(df, bias_data):
    """
    Generate a clean, plain HTML report.
    """
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cross-Lingual Sentiment Analysis Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Arial', sans-serif;
                background: #ffffff;
                color: #333;
                line-height: 1.6;
            }}
            
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                padding: 40px 20px;
            }}
            
            .header {{
                border-bottom: 2px solid #000;
                padding-bottom: 20px;
                margin-bottom: 40px;
            }}
            
            .header h1 {{
                font-size: 2em;
                margin-bottom: 10px;
            }}
            
            .header p {{
                font-size: 0.95em;
                color: #666;
            }}
            
            .section {{
                margin-bottom: 40px;
            }}
            
            .section-title {{
                font-size: 1.5em;
                margin-bottom: 20px;
                border-bottom: 1px solid #ccc;
                padding-bottom: 10px;
            }}
            
            .metrics-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .metric-card {{
                border: 1px solid #ddd;
                padding: 15px;
                text-align: center;
            }}
            
            .metric-value {{
                font-size: 1.8em;
                font-weight: bold;
                margin: 10px 0;
            }}
            
            .metric-label {{
                font-size: 0.9em;
                color: #666;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }}
            
            thead {{
                background: #f5f5f5;
                border-bottom: 2px solid #000;
            }}
            
            th {{
                padding: 12px;
                text-align: left;
                font-weight: bold;
            }}
            
            td {{
                padding: 10px 12px;
                border-bottom: 1px solid #ddd;
            }}
            
            tr:hover {{
                background: #f9f9f9;
            }}
            
            .sentiment-positive {{
                color: #2d5016;
                font-weight: bold;
            }}
            
            .sentiment-negative {{
                color: #8b0000;
                font-weight: bold;
            }}
            
            .sentiment-neutral {{
                color: #333;
                font-weight: bold;
            }}
            
            .score-bar {{
                width: 150px;
                height: 15px;
                background: #e0e0e0;
                border: 1px solid #999;
                margin: 5px 0;
            }}
            
            .score-fill {{
                height: 100%;
                background: #333;
                transition: width 0.3s ease;
            }}
            
            .findings {{
                background: #f9f9f9;
                border-left: 3px solid #000;
                padding: 15px;
                margin-bottom: 20px;
            }}
            
            .findings h3 {{
                margin-bottom: 10px;
            }}
            
            .findings ul {{
                list-style-position: inside;
                line-height: 1.8;
            }}
            
            .footer {{
                border-top: 1px solid #ccc;
                padding-top: 20px;
                margin-top: 40px;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }}
            
            .download-btn {{
                display: inline-block;
                background: #000;
                color: white;
                padding: 10px 20px;
                border: none;
                cursor: pointer;
                margin-top: 15px;
                font-size: 1em;
            }}
            
            .download-btn:hover {{
                background: #333;
            }}
            
            @media print {{
                body {{
                    background: white;
                }}
                .download-btn {{
                    display: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Cross-Lingual Sentiment Analysis Report</h1>
                <p>Analyzing Media Bias Across English, Hindi, Bengali, Kannada & Tamil News Sources</p>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}</p>
            </div>
            
            <!-- Metrics Section -->
            <div class="section">
                <h2 class="section-title">Overview Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">Total Headlines</div>
                        <div class="metric-value">{len(df)}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">News Sources</div>
                        <div class="metric-value">{df['source'].nunique()}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Languages</div>
                        <div class="metric-value">{df['language'].nunique()}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Avg Sentiment</div>
                        <div class="metric-value">{df['sentiment_score'].mean():+.2f}</div>
                    </div>
                </div>
            </div>
            
            <!-- Headlines Section -->
            <div class="section">
                <h2 class="section-title">Headline Sentiment Analysis</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Source</th>
                            <th>Language</th>
                            <th>Headline</th>
                            <th>Score</th>
                            <th>Sentiment</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for idx, row in df.iterrows():
        sentiment_class = f"sentiment-{row['sentiment_label'].lower()}"
        score_percent = (row['sentiment_score'] + 1) * 50
        
        html_content += f"""
                        <tr>
                            <td>{row['source'].replace('_', ' ').title()}</td>
                            <td>{row['language'].upper()}</td>
                            <td>{row['headline']}</td>
                            <td>
                                <div class="score-bar">
                                    <div class="score-fill" style="width: {score_percent}%"></div>
                                </div>
                                {row['sentiment_score']:+.2f}
                            </td>
                            <td><span class="{sentiment_class}">{row['sentiment_label']}</span></td>
                        </tr>
        """
    
    html_content += """
                    </tbody>
                </table>
            </div>
            
            <!-- Bias Analysis Section -->
            <div class="section">
                <h2 class="section-title">Media Bias Analysis</h2>
                <table>
                    <thead>
                        <tr>
                            <th>News Source</th>
                            <th>Avg Sentiment</th>
                            <th>Positive</th>
                            <th>Negative</th>
                            <th>Bias</th>
                        </tr>
                    </thead>
                    <tbody>
    """
    
    for item in bias_data:
        html_content += f"""
                        <tr>
                            <td>{item['Source']}</td>
                            <td><strong>{item['Avg Sentiment']}</strong></td>
                            <td>{item['Positive']}</td>
                            <td>{item['Negative']}</td>
                            <td>{item['Bias Indicator']}</td>
                        </tr>
        """
    
    html_content += """
                    </tbody>
                </table>
            </div>
            
            <!-- Key Findings -->
            <div class="section">
                <h2 class="section-title">Key Findings</h2>
                <div class="findings">
                    <h3>Sentiment Patterns</h3>
                    <ul>
                        <li>Different news sources show varying sentiment expression for the same events</li>
                        <li>Media bias is evident in sentiment score variations across outlets</li>
                        <li>Language-specific reporting styles influence sentiment expression</li>
                        <li>This data supports the Media Bias + Sentiment Shift publishable angle</li>
                    </ul>
                </div>
            </div>
            
            <div class="footer">
                <p>Cross-Lingual Sentiment Analysis Report</p>
                <p>Sources: Times of India | NDTV | Vijaya Karnataka | Dinamani</p>
                <button class="download-btn" onclick="window.print()">Download as PDF</button>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html_content

def save_report(html_content, filename='report.html'):
    """Save HTML report to file."""
    reports_dir = '../reports'
    os.makedirs(reports_dir, exist_ok=True)
    
    filepath = os.path.join(reports_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath