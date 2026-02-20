import concurrent.futures
import time
from selenium import webdriver
from config.settings import Settings
from core.scraper import ElPaisScraper
from core.translator import TranslationService
from core.analyzer import DataAnalyzer

BUILD_NAME = f"El Pais Build - {int(time.time())}"

def run_session(capability):
    """
    Runs the scraper session on BrowserStack with the given capability.
    """
    browserstack_url = f"https://{Settings.BROWSERSTACK_USERNAME}:{Settings.BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
    
    capability['project'] = 'El Pais Automation'
    capability['build'] = BUILD_NAME
    capability['name'] = f"Test on {capability.get('browser', capability.get('browserName'))} {capability.get('os', capability.get('osVersion'))}"

    print(f"[{capability['name']}] Starting session...")
    
    driver = None
    try:
        driver = webdriver.Remote(
            command_executor=browserstack_url,
            options=capability_to_options(capability) 
        )
        
        scraper = ElPaisScraper(driver=driver)
        scraper.navigate_to_opinion()
        
        thread_prefix = f"{capability.get('browserName', 'unknown')}_{capability.get('os', 'mobile')}"
        thread_prefix = "".join(c for c in thread_prefix if c.isalnum() or c in ('_','-'))
        
        articles = scraper.get_first_five_articles(filename_prefix=thread_prefix)
        print(f"[{capability['name']}] Retrieved {len(articles)} articles.")
        
        if articles:
            translator = TranslationService()
            titles_es = [a['title'] for a in articles]
            titles_en = translator.translate_texts(titles_es)
            
            analyzer = DataAnalyzer()
            print(f"[{capability['name']}] Analysis Result:")
            analyzer.analyze_headers(titles_en)
        
        driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Scraping and Translation successful"}}')
        driver.quit()
        return f"Success: {capability['name']}"
    except Exception as e:
        # Mark test as failed
        if driver:
            try:
                driver.execute_script(f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"failed", "reason": "{str(e)}"}} }}')
            except:
                pass
            driver.quit()
        return f"Failed: {capability['name']} - {str(e)}"

def capability_to_options(cap):
    """
    Helper to convert dict caps to Selenium Options.
    """
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.safari.options import Options as SafariOptions
    from selenium.webdriver.edge.options import Options as EdgeOptions
    
    browser_name = cap.get('browserName', '').lower()
    
    if 'chrome' in browser_name:
        options = ChromeOptions()
    elif 'firefox' in browser_name:
        options = FirefoxOptions()
    elif 'safari' in browser_name:
        options = SafariOptions()
    elif 'edge' in browser_name:
        options = EdgeOptions()
    else:
        options = ChromeOptions()
        
    for k, v in cap.items():
        options.set_capability(k, v)
        
    return options

def main():
    import json
    import os
    
    config_path = os.path.join("config", "browserstack.json")
    with open(config_path, "r") as f:
        caps = json.load(f)
    
    print(f"Starting BrowserStack Parallel Execution. Build Name: {BUILD_NAME}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(caps)) as executor:
        results = list(executor.map(run_session, caps))
        
    print("\n--- Execution Summary ---")
    for res in results:
        print(res)

if __name__ == "__main__":
    main()
