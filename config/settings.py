import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
    BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
    
    RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
    RAPIDAPI_HOST = "rapid-translate-multi-traduction.p.rapidapi.com"
    
    BASE_URL = "https://elpais.com"
    OPINION_SECTION_URL = "https://elpais.com/opinion"
    
    OUTPUT_DIR = os.path.join(os.getcwd(), "output")

if not os.path.exists(Settings.OUTPUT_DIR):
    os.makedirs(Settings.OUTPUT_DIR)
