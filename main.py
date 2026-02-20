from core.scraper import ElPaisScraper
from core.translator import TranslationService
from core.analyzer import DataAnalyzer
import sys

def main():
    print("Starting El Pais Automation (Local)...")
    
    scraper = ElPaisScraper()
    try:
        scraper.navigate_to_opinion()
        articles = scraper.get_first_five_articles()
    finally:
        scraper.close()
        
    if not articles:
        print("No articles found. Exiting.")
        return

    translator = TranslationService()
    titles_es = [a['title'] for a in articles]
    
    print("\nTranslating titles...")
    titles_en = translator.translate_texts(titles_es)
    
    for original, translated in zip(titles_es, titles_en):
        print(f"ES: {original}\nEN: {translated}\n")

    analyzer = DataAnalyzer()
    analyzer.analyze_headers(titles_en)

    print("\nExecution Complete.")

if __name__ == "__main__":
    main()
