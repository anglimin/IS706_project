import pandas as pd
import numpy as np
import os
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from bs4 import BeautifulSoup
import requests


class WebScrapping:

    def __init__(self):
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        self.driver = driver
    
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
            

