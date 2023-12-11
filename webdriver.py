from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

chromedriver_autoinstaller.install()

def Chrome(url):
    service = Service(executable_path= '/user/bin/chromedrive')
    driver = webdriver.Chrome(service = service)
    driver.get(url)

def ChromeHeadless(url, actions = None):
    options = webdriver.ChromeOptions()
    chromedriver_autoinstaller.install()
    # driver = webdriver.Chrome()
    options.add_argument('--disable-gpu')
    options.add_argument("--headless=new")  
    # service = Service(executable_path= '/user/bin/chromedrive')
    driver = webdriver.Chrome(options= options)
    driver.get(url)
    return driver

def ChromeFullPageLoad(url):
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    driver.get(url)
    current_scroll = 0
    scroll_step = 500


    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(6)  # Adjust sleep time as needed
        
        # Look for the "show more" button
        # show_more_button = driver.find_element(By.CLASS_NAME, "items-center.justify-center.h-100.ph5")
        
        # # Click the "show more" button
        # show_more_button.click()
        # time.sleep(4)  # Adjust sleep time as needed
        
        # # Scroll back up to the previous position
        # current_scroll = driver.execute_script("return window.scrollY;")
        # driver.execute_script(f"window.scrollTo(0, {current_scroll - scroll_step});")
        
        try:
            # Look for the "show more" button again to check if it's still present
            show_more_button = driver.find_element(By.CLASS_NAME, "items-center.justify-center.h-100.ph5")
             # Click the "show more" button
            show_more_button.click()
            time.sleep(6)  # Adjust sleep time as needed
        except NoSuchElementException:
            # If "show more" button is not found, break out of the loop
            break

            
        # Scroll to the very bottom of the page
        # WebDriverWait(driver, 10).until(
        #     driver.execute_script(f"window.scrollTo(0, {total_height});")
        # )
    page_source = driver.page_source 
    driver.close()
    return page_source

def click_by_class(driver, name):
    button = driver.find_element(By.CLASS_NAME, "spec-highlight__button")
    button.click()

def click_by_id(driver, name):
    button = driver.find_element(By.ID, "spec-highlight__button")
    button.click()

def GetChromeDriver(url):
    options = webdriver.ChromeOptions()
    # options.add_argument('--disable-gpu')
    # options.add_argument("--headless=new")  
    service = Service(executable_path= '/user/bin/chromedrive')
    driver = webdriver.Chrome(service = service , options= options)
    driver.get(url)
    

    return driver