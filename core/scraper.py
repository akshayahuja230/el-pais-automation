import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.settings import Settings

class ElPaisScraper:
    def __init__(self, driver=None):
        self.driver = driver
        if not self.driver:
             # Default to local Chrome if no driver provided
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=options)

    def navigate_to_opinion(self):
        print(f"Navigating to {Settings.BASE_URL}...")
        self.driver.get(Settings.BASE_URL)
        
        try:
            print("Checking for cookie banner...")
            accept_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "didomi-notice-agree-button"))
            )
            accept_button.click()
            print("Cookie banner accepted.")
        except TimeoutException:
            print("No cookie banner found or already accepted.")

        print("Navigating to Opinion section...")
        try:
             opinion_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Opinión"))
             )
             opinion_link.click()
        except Exception as e:
            print(f"Could not click link, falling back to direct URL: {e}")
            self.driver.get(Settings.OPINION_SECTION_URL)
            
    def get_first_five_articles(self, filename_prefix="article"):
        print("Fetching articles...")
        articles_data = []
        
        try:

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "article"))
            )
            
            articles = self.driver.find_elements(By.TAG_NAME, "article")
            print(f"Found {len(articles)} articles. Processing first 5...")
            
            for i, article in enumerate(articles[:5]):
                print(f"--- Processing Article {i+1} ---")
                data = {}
                
                try:
                    title_element = article.find_element(By.TAG_NAME, "h2")
                    data['title'] = title_element.text.strip()
                except NoSuchElementException:
                    data['title'] = "No Title Found"
                
                try:
                    content_element = article.find_element(By.TAG_NAME, "p")
                    data['content'] = content_element.text.strip()
                except NoSuchElementException:
                    data['content'] = "No Content Found"
                    
                try:
                    img_element = article.find_element(By.TAG_NAME, "img")
                    img_url = img_element.get_attribute("src")
                    data['image_url'] = img_url
                    
                    if img_url:
                        safe_prefix = f"{filename_prefix}_{i+1}"
                        self.download_image(img_url, safe_prefix)
                except NoSuchElementException:
                    data['image_url'] = None
                
                print(f"Title: {data['title']}")
                print(f"Content: {data['content'][:50]}...")
                articles_data.append(data)
                
        except Exception as e:
            print(f"Error extracting articles: {e}")
            
        return articles_data

    def download_image(self, url, filename_prefix):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                # extension
                ext = "jpg"
                if "png" in url: ext = "png"
                elif "webp" in url: ext = "webp"
                
                filename = f"{filename_prefix}.{ext}"
                filepath = os.path.join(Settings.OUTPUT_DIR, filename)
                
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                print(f"Saved image to {filepath}")
        except Exception as e:
            print(f"Failed to download image: {e}")

    def close(self):
        if self.driver:
            self.driver.quit()
