import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Scraper:
    def _get_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        if os.getenv("Environment", "production") == "production":
            chrome_options.add_argument("--headless")
        return chrome_options

    def _get_browser(self):
        return webdriver.Chrome(options=self._get_options())

    def run(self) -> list[str]:
        browser = self._get_browser()

        browser.get("https://www.google.com")
        url = browser.current_url

        browser.quit()
        return [url]
