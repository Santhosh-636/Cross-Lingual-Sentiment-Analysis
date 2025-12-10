# Cross-Lingual Sentiment Analysis

## Overview
The Cross-Lingual Sentiment Analysis project aims to explore and compare sentiment patterns in news headlines across different languages, specifically English, Hindi, Bengali, and Kannada. By analyzing how various media outlets express sentiment for the same news events, such as accidents, crimes, and sports results, this project seeks to uncover potential media biases and shifts in sentiment.

## Project Structure
The project is organized into several directories and files:

- **src/**: Contains the source code for scraping, sentiment analysis, natural language processing, database handling, analysis, and visualization.
  - **scrapers/**: Scripts to scrape news headlines from various sources.
    - `times_of_india.py`
    - `vijaya_karnataka.py`
    - `ndtv.py`
    - `dinamani.py`
  - **sentiment/**: Contains the sentiment analysis logic.
    - `analyzer.py`
    - `models.py`
  - **nlp/**: Functions for text translation and preprocessing.
    - `translators.py`
    - `preprocessor.py`
  - **database/**: Manages database interactions.
    - `db_handler.py`
  - **analysis/**: Compares sentiment across languages and detects media bias.
    - `comparison.py`
    - `bias_detector.py`
  - **visualization/**: Functions for visualizing analysis results.
    - `plots.py`
  - `main.py`: The entry point for the application.

- **data/**: Contains directories for raw and processed data.
  - **raw/**: Stores raw scraped data.
  - **processed/**: Stores processed data ready for analysis.

- **reports/**: Contains documentation of findings from the analysis.
  - `findings.md`

- **requirements.txt**: Lists the dependencies required for the project.

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd cross-lingual-sentiment-analysis
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure you have access to the necessary APIs or web scraping permissions for the news sources.

## Usage Guidelines
- To run the entire analysis pipeline, execute the `main.py` file:
  ```
  python src/main.py
  ```

- The scrapers will collect news headlines, which will then be processed and analyzed for sentiment. The results will be visualized and documented in the `reports/findings.md` file.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.