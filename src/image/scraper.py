import os
from urllib import parse

from fastapi import HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class ImageScraper:
    def get_urls(self, search: str, size: int = 10) -> list[str]:
        browser = self._get_browser()
        browser.get("https://www.freeimages.com/")

        self._search_for_photos(browser, search)
        self._change_to_results_tab(browser)
        photos = self._get_photo_urls(browser, search, size)

        browser.quit()
        return photos

    def _get_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        if os.getenv("Environment", "production") == "production":
            chrome_options.add_argument("--headless")
        return chrome_options

    def _get_browser(self):
        return webdriver.Chrome(options=self._get_options())

    def _search_for_photos(self, browser: WebDriver, search: str):
        try:
            search_button = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "search-input")))
        except Exception as exc:
            raise HTTPException(500, "Could not find the search button.") from exc

        search_button.send_keys(search)
        search_button.send_keys(Keys.ENTER)

        try:
            WebDriverWait(browser, 10).until(EC.number_of_windows_to_be(2))
        except Exception as exc:
            raise HTTPException(500, "The search was not successful.") from exc

    def _change_to_results_tab(self, browser: WebDriver):
        for window_handle in browser.window_handles:
            if window_handle != browser.current_window_handle:
                browser.switch_to.window(window_handle)
                break

    def _get_photo_urls(self, browser: WebDriver, search: str, size: int):
        photos: list[str] = []
        current_pange = 1
        while len(photos) < size:
            try:
                photos_in_grid = WebDriverWait(browser, 10).until(
                    EC.visibility_of_all_elements_located((By.CLASS_NAME, "yGh0CfFS4AMLWjEE9W7v"))
                )
            except Exception as exc:
                raise HTTPException(500, "Could not find the photos grid.") from exc

            urls = [photo.get_property("src") for photo in photos_in_grid if isinstance(photo.get_property("src"), str)]
            photos.extend(urls[:size - len(photos)])  # type: ignore

            if len(photos) < size:
                next_page_url = f"https://www.istockphoto.com/br/search/2/image?mediatype=photography&page={current_pange + 1}&phrase={parse.quote(search)}"
                browser.get(next_page_url)
                self._wait_until_page_has_loaded(browser)
                current_pange += 1

        return photos

    def _wait_until_page_has_loaded(self, browser: WebDriver):
        WebDriverWait(browser, 10).until(lambda _: browser.execute_script("return document.readyState;") == "complete")
