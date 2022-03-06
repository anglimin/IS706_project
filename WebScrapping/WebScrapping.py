import pandas as pd
import numpy as np
import os
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests

class WebScrapping:

    def __init__(self):
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        self.driver = driver

    def string_similarity(self, string1, string2):
        """
        Purpose:
        If a certain threshold, the string will be similar
        """
        pass
    
    def search_information(self, deprecated_api):
        """
        Purpose: Scrape relevant deprecated api information from official documents

        Return:
        1) Pandas Dataframe of the deprecated api
        """
        driver = self.driver
        driver.get("http://www.google.com")
        driver.implicitly_wait(0.5)
        driver.find_element(By.NAME, "q").send_keys(deprecated_api + Keys.ENTER)
        # Tabulate the list of search results
        search_results = driver.find_elements(By.XPATH, '(//h3)/../../a')
        for result in search_results:
            result.click()
            current_url = driver.current_url
            current_page = requests.get(current_url)
            soup = BeautifulSoup(current_page.content, "html.parser")
            
            # go back to the search result page
            driver.execute_script("window.history.go(-1)")


if __name__ == "__main__":
    pass