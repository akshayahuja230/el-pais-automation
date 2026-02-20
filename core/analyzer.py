from collections import Counter
import re

class DataAnalyzer:
    def analyze_headers(self, headers):
        print("\n--- Analyzing Headers ---")
        
        text = " ".join(headers)
        print(text)
        
        words = re.findall(r'\b\w+\b', text.lower())
        
        counts = Counter(words)
        
        repeated = {word: count for word, count in counts.items() if count > 2}
        
        print(f"Repeated words (appearing > 2 times):")
        if not repeated:
            print("None found.")
        
        for word, count in repeated.items():
            print(f"- '{word}': {count}")
            
        return repeated
