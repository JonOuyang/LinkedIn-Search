
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
#IMPORTANT: Webdriver requires chrome driver, which is put into the system PATH

# Creating a webdriver instance
driver = webdriver.Chrome()
 
# Opening linkedIn's login page
driver.get("https://www.linkedin.com/login")
 
# waiting for the page to load
time.sleep(3)
 
# entering username
username = driver.find_element(By.ID, "username")
 
# In case of an error, try changing the element
# tag used here.
 
# Enter Your Email Address
username.send_keys("")  
 
# entering password
pword = driver.find_element(By.ID, "password")
# In case of an error, try changing the element 
# tag used here.
 
# Enter Your Password
pword.send_keys("")        
 
# Clicking on the log in button
# Format (syntax) of writing XPath --> 
# //tagname[@attribute='value']
driver.find_element(By.XPATH, "//button[@type='submit']").click()
# In case of an error, try changing the
# XPath used here.

#iterate through every job

job_list = []

def search_job_page(keywords):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    scroll_origin = ScrollOrigin.from_viewport(200, 500)
    
    for _ in range(5):
        ActionChains(driver)\
            .scroll_from_origin(scroll_origin, 0, 1000)\
            .perform()
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        job_listings = soup.find_all(
                    "div",
                    class_="job-card-list__entity-lockup artdeco-entity-lockup artdeco-entity-lockup--size-4 ember-view",
                )
        element = driver.find_element(By.XPATH, f"//*[@id='{job_listings[-1].get('id')}']")
        element.click()
        time.sleep(0.4)
        
    #time.sleep(2)

    job_listings = soup.find_all(
            "div",
            class_="job-card-list__entity-lockup artdeco-entity-lockup artdeco-entity-lockup--size-4 ember-view",
        )
    
    #job-card-list__entity-lockup artdeco-entity-lockup artdeco-entity-lockup--size-4 ember-view
    #flex-grow-1 artdeco-entity-lockup__content ember-view
    
    print(f'Numer of jobs detected on page: {len(job_listings)}')

    for job in job_listings:

        element = driver.find_element(By.XPATH, f"//*[@id='{job.get('id')}']")
        element.click()
        time.sleep(0.1)
        load_job_data(keywords)

#individual job function
job_list = []

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
    
    timeout = 5
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
                #job_company = soup.find('div', {'class': 'artdeco-entity-lockup__title ember-view t-20'}).text.strip()
                job_company = soup.find('a', {'class': 'ember-view link-without-visited-state inline-block t-black'}).text.strip()
            except:
                job_company = 'N/A'
            job_name = soup.find('span', {'class': 'job-details-jobs-unified-top-card__job-title-link'}).text.strip()
            #job_time = soup.find('span', {'class': 'tvm__text tvm__text--positive'}).text.strip()
            job_link = driver.current_url

            job_list.append({"Company" : job_company, "Job Title" : job_name, "Link" : job_link})
            break
        else:
            pass

def scrape_jobs(title, location, keywords):
    driver.get(f"https://www.linkedin.com/jobs/search/?keywords={title}&location={location}")
    time.sleep(1)
    search_job_page(keywords)

scrape_jobs("engineer", "Remote", ["bachelor"])
print(job_list)


