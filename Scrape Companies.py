import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")
time.sleep(1)
username = driver.find_element(By.ID, "username")
username.send_keys("username")  
pword = driver.find_element(By.ID, "password")
pword.send_keys("password")        
driver.find_element(By.XPATH, "//button[@type='submit']").click()

companies = []

def scrape_companies(location="San Jose", keywords=[], startup=True):
    if startup:
        
        page = 1
        while True:
            driver.get(f'https://www.linkedin.com/search/results/companies/?companyHqGeo=%5B%22106233382%22%5D&companySize=%5B%22B%22%2C%22C%22%5D&location=San Jose&page={page}')

            soup = BeautifulSoup(driver.page_source, "html.parser")
            companies_list = soup.find_all(
                        "span",
                        class_="entity-result__title-text",
                    )
            if len(companies_list) == 0:
                break
            else:
                searchPage(keywords)
            
            page+=1



def searchPage(keywords):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    companies_list = soup.find_all(
                        "span",
                        class_="entity-result__title-text",
                    )

    for company in companies_list:

        driver.get(str(company).split('href="')[1].split('">')[0])
        
        driver.find_element(By.CLASS_NAME, "org-about-module__description").find_element(By.CLASS_NAME,"t-black--light").click()

        description = driver.find_element(By.CLASS_NAME, "lt-line-clamp__raw-line").text
        for word in keywords:
            if word.lower() in description.lower():
                companies.append(str(company).split('href="')[1].split('">')[0])
                break


keywords = ["machine learning", "ML", "artificial intelligence", "AI"]

scrape_companies(keywords=keywords)
