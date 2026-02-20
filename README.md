# El Pais Automation (Selenium + BrowserStack)

This project automates scraping articles from the "Opinión" section of El País, translates their headers, and analyzes them for repeated words. It is designed to run both locally and on BrowserStack for cross-browser verification.

## 🚀 Key Features
- **Scraping**: Fetches the first 5 articles (Title, Content, and Images) using Selenium.
- **Translation**: Translates Spanish titles to English using RapidAPI.
- **Analysis**: Identifies words repeated more than twice across all translated headers.
- **Parallel Testing**: Runs across 5 browsers/devices simultaneously on BrowserStack.
- **Robustness**: Handles cookie banners and dynamic layouts with explicit waits.

## 📁 Project Structure
- `core/scraper.py`: Selenium logic for navigation and data extraction.
- `core/translator.py`: API integration for Spanish-to-English translation.
- `core/analyzer.py`: Text processing and word frequency analysis.
- `config/settings.py`: Centralized configuration (URLs, Directory paths).
- `config/browserstack.json`: Externalized browser capabilities for parallel testing.
- `browserstack_runner.py`: Multi-threaded runner for BrowserStack cloud execution.
- `main.py`: Entry point for local execution.

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Chrome WebDriver (for local runs)

### 2. Environment Variables
Create a `.env` file in the root directory:
```env
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
RAPIDAPI_KEY=your_rapidapi_key
```

### 3. Installation
```bash
pip install -r requirements.txt
```

## 🏃 How to Run

### Run Locally
```bash
python main.py
```

### Run on BrowserStack (Parallel)
```bash
python browserstack_runner.py
```

## 📊 Evaluation Criteria Met
- [x] Language check (ensures site is in Spanish).
- [x] Scrapes first 5 articles from Opinion section.
- [x] Downloads cover images.
- [x] Translates headers to English via API.
- [x] Analyzes word frequency (>2 occurrences).
- [x] Executes on 5 parallel threads in BrowserStack.
