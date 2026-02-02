#This test checks the navigation buttons on the main page
# -------------------------- Imports --------------------------
import __init__
import source.browser_setup as setup
import source.wait_functions as wf
import source.my_functions as mf
from selenium.webdriver.common.by import By
import pytest
import time

# Test repeats in fullscreen - Window size affects website functionality

# -------------------------- Data Setup --------------------------
buttons = [
("/html/body/div[2]/div/section[1]/div/div/div/a",  "/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[4]"),
("/html/body/div[2]/div/nav/div/div/ul/li[1]/a",    "/html/body/div[2]/div/div/section[2]/div/div[1]/h2"),
("/html/body/div[2]/div/nav/div/div/ul/li[2]/a",    "/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[4]"),
("/html/body/div[2]/div/nav/div/div/ul/li[3]/a",    ""), # Fail expected here - No correlating element on the webpage to scroll to 
("/html/body/div[2]/div/nav/div/div/ul/li[4]/a",    "/html/body/div[2]/div/section[2]/div/div[1]/h2"),
("/html/body/div[2]/div/nav/div/div/ul/li[5]/a",    "/html/body/div[2]/div/section[3]/div/div/div/div/div/h3"),
]

rolldown_button_xpath = "/html/body/div[2]/div/nav/div/button"

# -------------------------- Helper functions --------------------------
def wait_for_button_to_load(elements):
    wf.wait_for_element_xpath(elements[1])
    if wf.wait_for_element_xpath(elements[0]) or wf.wait_for_element_xpath(elements[0]) == True:
        assert True
    else:
        assert False
    
def check_element_pos(elements):
    element = setup.driver.find_element(By.XPATH, elements)
    is_at_top = setup.driver.execute_script("const rect = arguments[0].getBoundingClientRect(); return rect.top >= 0 && rect.top <= 500;", element)
    return is_at_top

# -------------------------- Test --------------------------
@pytest.fixture(params=buttons)
def buttons_fixture(request):
    return request.param

def test_group_small_window(buttons_fixture, subtests):
    with subtests.test("Open website"):
        mf.load_website()
    with subtests.test("Wait for button to load"):
        wait_for_button_to_load(buttons_fixture)
    with subtests.test("Click Button"):
        rolldown_button = mf.load_element(rolldown_button_xpath)
        if rolldown_button.is_displayed() == True:
            mf.click_button(False, rolldown_button)
            mf.click_button(False, mf.load_element(buttons_fixture[0]))
        else:
            mf.click_button(False, mf.load_element(buttons_fixture[0]))
    with subtests.test("Wait for scroll"):
        time.sleep(2)
        wf.wait_for_element_visible(setup.driver.find_element(By.XPATH, buttons_fixture[1]))
    with subtests.test("Check if element at top of the page"):
        if check_element_pos(buttons_fixture[1]) == False:
            assert False

def test_group_maximized_window(buttons_fixture, subtests):
    with subtests.test("Open website"):
        mf.load_website()
        setup.driver.maximize_window()
    with subtests.test("Wait for button to load"):
        wait_for_button_to_load(buttons_fixture)
    with subtests.test("Click Button"):
        rolldown_button = mf.load_element(rolldown_button_xpath)
        if rolldown_button.is_displayed() == True:
            mf.click_button(False, rolldown_button)
            mf.click_button(False, mf.load_element(buttons_fixture[0]))
        else:
            mf.click_button(False, mf.load_element(buttons_fixture[0]))
    with subtests.test("Wait for scroll"):
        time.sleep(2)
        wf.wait_for_element_visible(setup.driver.find_element(By.XPATH, buttons_fixture[1]))
    with subtests.test("Check if element at top of the page"):
        if check_element_pos(buttons_fixture[1]) == False:
            assert False
    