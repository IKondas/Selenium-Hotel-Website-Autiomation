# -------------------------- Imports --------------------------
import source.browser_setup as setup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

# -------------------------- General Wait Functions -------------------------- 
def wait_for_element_id(element_id):
    try:
        WebDriverWait(setup.driver, setup.delay).until(EC.presence_of_element_located((By.ID, element_id)))
    except TimeoutException:
        print ("Element " + str(element_id) + " could not be loaded within ", setup.delay, " seconds")
        assert False

def wait_for_element_xpath(element_xpath):
    try:
        WebDriverWait(setup.driver, setup.delay).until(EC.presence_of_element_located((By.XPATH, element_xpath)))
        return True
    except TimeoutException:
        print ("Element " + str(element_xpath) + " could not be loaded within ", setup.delay, " seconds")
        assert False

def wait_for_element_visible(WebElement):
    try:
        WebDriverWait(setup.driver, setup.delay).until(EC.visibility_of(WebElement))
        return True
    except TimeoutException:
        print ("Element " + str(WebElement) + " could not be loaded within ", setup.delay, " seconds")
        assert False

def wait_for_element_visible_xpath(element_xpath):
    try:
        WebDriverWait(setup.driver, setup.delay).until(EC.visibility_of(By.XPATH, element_xpath))
        return True
    except TimeoutException:
        print ("Element " + str(By.XPATH, element_xpath) + " could not be loaded within ", setup.delay, " seconds")
        assert False
