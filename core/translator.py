import requests
import time
from config.settings import Settings

class TranslationService:
    def translate_texts(self, texts, target_lang="en"):
        """
        Translates a list of texts using Rapid Translate Multi Traduction API.
        Url: https://rapidapi.com/sibaridev/api/rapid-translate-multi-traduction
        """
        if not texts:
            return []
            
        if not Settings.RAPIDAPI_KEY:
            print("[WARNING] RAPIDAPI_KEY missing. Returning MOCK translations.")
            return [f"[MOCK] {t}" for t in texts]

        url = f"https://{Settings.RAPIDAPI_HOST}/t"
        
        payload = {
            "from": "es",
            "to": target_lang,
            "q": texts # The API accepts a list of strings directly
        }
        
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": Settings.RAPIDAPI_KEY,
            "X-RapidAPI-Host": Settings.RAPIDAPI_HOST
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Translation API Error: {e}")
            return [f"[ERROR] {t}" for t in texts]
