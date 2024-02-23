import time
import random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()

# This instance will be used to log into LinkedIn
# Opening linkedIn's login page
driver.get("https://www.linkedin.com/login")
time.sleep(1)
username = driver.find_element(By.ID, "username")
username.send_keys("username")  
pword = driver.find_element(By.ID, "password")
pword.send_keys("password")        
driver.find_element(By.XPATH, "//button[@type='submit']").click()

job_list = []

#iterate through every job currently on page

def search_job_page(keywords):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    scroll_origin = ScrollOrigin.from_viewport(200, 500)
    
    for _ in range(3):
        ActionChains(driver)\
            .scroll_from_origin(scroll_origin, 0, 2000)\
            .perform()
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_listings = soup.find_all(
                    "div",
                    class_="job-card-list__entity-lockup artdeco-entity-lockup artdeco-entity-lockup--size-4 ember-view",
                )
     #encountered errors in finding element on page 5, attempt to bypass using try pass   
     try:
          driver.find_element(By.XPATH, f"//*[@id='{job_listings[-1].get('id')}']").click()
         except:
          pass
        time.sleep(0.2)
        
    job_listings = soup.find_all(
            "div",
            class_="job-card-list__entity-lockup artdeco-entity-lockup artdeco-entity-lockup--size-4 ember-view",
        )
    
    print(f'Numer of jobs detected on page: {len(job_listings)}')

    for job in job_listings:
        driver.find_element(By.XPATH, f"//*[@id='{job.get('id')}']").click()
        time.sleep(0.1)
        load_job_data(keywords)

#loads job description, company, date, etc on selected job

def load_job_data(keywords):
    soup = BeautifulSoup(driver.page_source, "html.parser")

    #needs to be adjusted based on screen size; this is calibrated for vertical monitor fullscreen
    scroll_origin = ScrollOrigin.from_viewport(500, 500)
    
    ActionChains(driver)\
        .scroll_from_origin(scroll_origin, 0, -200)\
        .perform()
    time.sleep(0.1)
    for _ in range(5):
        ActionChains(driver)\
            .scroll_from_origin(scroll_origin, 0, 1000)\
            .perform()
        time.sleep(0.1)
    
    timeout = 2
    try:
        element_present = EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[2]/div[2]/div/div[2]/div/div[1]/div/section/section/div[1]/div[2]'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    
    description = driver.find_element(By.XPATH, '//*[@id="job-details"]')
    time.sleep(0.5)
    for word in keywords:
        if word.lower() in description.text.lower():
            try:
                job_company = soup.find('a', {'class': 'ember-view link-without-visited-state inline-block t-black'}).text.strip()
            except:
                job_company = 'N/A'
            job_name = soup.find('span', {'class': 'job-details-jobs-unified-top-card__job-title-link'}).text.strip()
            job_link = driver.current_url

            job_list.append({"Company" : job_company, "Job Title" : job_name, "Link" : job_link})
            break
        else:
            pass

#scrapes all jobs, taking in parameter of job title, job location, and keywords to look for in description
def scrape_jobs(title, location, keywords):
    page = 0
    while True:
        driver.get(f"https://www.linkedin.com/jobs/search/?keywords={title}&location={location}&start={page*25}")
        try:
            driver.find_element(By.XPATH, "/html/body/div[4]/div[3]/div[4]/div/div[1]/div/div[1]")
            print("Search Complete.")
            break
        except:
            time.sleep(1)
            search_job_page(keywords)
            page += 1

scrape_jobs("engineer", "Remote", ["bachelor"])
print(job_list)
print(len(job_list))
