# -------------------------- Imports --------------------------
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait

# -------------------------- Browser Options --------------------------
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-notifications")
#chrome_options.add_argument("disable-popup-blocking")
#chrome_options.add_argument("--disable-notifications")
    
service = Service(executable_path="/home/akondas/python/Selenium2_Test/source/chromedriver", chrome_options=chrome_options)

driver = webdriver.Chrome(service=service)
#driver.maximize_window()
delay = 5 # seconds - Time till Timeout Exception
wait = WebDriverWait(driver, timeout=delay)