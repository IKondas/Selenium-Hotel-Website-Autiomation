# -------------------------- Imports --------------------------
import __init__
import source.browser_setup as setup
import source.wait_functions as wf
from selenium.webdriver.common.by import By
import datetime
from dateutil.relativedelta import relativedelta


# -------------------------- General Test Functions --------------------------
def load_website(URL = None):
    if URL == None:
        setup.driver.get("https://automationintesting.online/")
    else:
        setup.driver.get(URL)

def load_element(xpath):
    wf.wait_for_element_xpath(xpath)
    element = setup.driver.find_element(By.XPATH, xpath)
    return element

def click_button(Scroll, element): 
    if Scroll == True:
        setup.driver.execute_script("arguments[0].scrollIntoView();", element)
        wf.wait_for_element_visible(element)
        setup.driver.execute_script("arguments[0].click();", element)
    else:
        setup.driver.execute_script("arguments[0].click();", element)

def compare_objects_text(element1_xpath, element2_xpath):
    element1 = load_element(element1_xpath)
    element2 = load_element(element2_xpath)
    if element1.text == element2.text:
        assert True
    else:
        assert False


def calendar_select_date(element, calendar_matrix_pos):
    element.click()
    xpath_base = "/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div["

    if element == load_element("/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[1]/div[1]/div/input"):
        xpath_base = xpath_base + "1" + "]/div[2]/div[2]/div/div/div/div"
        load_element(xpath_base)
    elif element == load_element("/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[2]/div[1]/div/input"):
        xpath_base = xpath_base + "2" + "]/div[2]/div[2]/div/div/div/div"
        load_element(xpath_base)
    else:
        assert False

    date_xpath = xpath_base + "/div[2]/div[2]/div[" + str(calendar_matrix_pos[0]) + "]/div[" + str(calendar_matrix_pos[1]) + "]"
    click_button(False, date_xpath)
    
def compare_dates(check_in, check_out):
        date1 = str(check_in.get_attribute("value"))
        date_split = date1.split("/", 2)
        datetime1 = datetime(int(date_split[2]), int(date_split[1]), int(date_split[0]))
        date2 = str(check_out.get_attribute("value"))
        date_split = date2.split("/", 2)
        datetime2 = datetime(int(date_split[2]), int(date_split[1]), int(date_split[0]))
        if datetime2 > datetime1:
            assert True
        else:
            assert False

# -------------------------- Date Selection Test Functions --------------------------

def check_date(is_check_out):
    check_in_field = load_element("/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[1]/div[1]/div/input")
    check_out_field = load_element("/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[2]/div/div/input")
    div = str(int(is_check_out) + 1)
    button_to_click = None
    calendar = "/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[" + div + "]/div[2]/div[2]"
    month = "/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[" + div + "]/div[2]/div[2]/div/div/div/div/div[1]/h2"

    check_in_field_date =  check_in_field.get_attribute("value")
    check_out_field_date = check_out_field.get_attribute("value")

    if is_check_out == False:
        button_to_click = "/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[1]/div[1]/div/input"
        check_m_y = datetime.datetime.strptime(check_in_field_date, ("%d/%m/%Y"))
    else:
        button_to_click = "/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[2]/div/div/input"
        check_m_y = datetime.datetime.strptime(check_out_field_date, ("%d/%m/%Y"))

    # --- Month ---
    button_to_click = load_element(button_to_click)
    click_button(True, button_to_click)
    load_element(calendar)
    default_month = load_element(month).text
    if default_month != check_m_y.strftime("%B %Y"):
        assert False

    # --- Day ---
    days_list = setup.driver.find_elements(By.XPATH, "/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[" + div +"]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[/*]/div[/*]")
    for day in days_list:
        dayclass = day.get_attribute("class")
        if "react-datepicker__day--selected" in dayclass:
            if day.text != check_m_y.strftime("%d"):
                assert False

def change_month(is_check_out, how_many_months):
    div = str(int(is_check_out) + 1)
    button_left = "/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[" + div + "]/div[2]/div[2]/div/div/div/button[1]"
    button_right = "/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[" + div + "]/div[2]/div[2]/div/div/div/button[2]"
    current_month = load_element("/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[" + div + "]/div[2]/div[2]/div/div/div/div/div[1]/h2")

    if how_many_months < 0:
        for i in range(abs(how_many_months)):
            previous_month = (datetime.datetime.strptime(current_month.text, "%B %Y") - relativedelta(months = 1)).strftime("%B %Y")
            click_button(True, load_element(button_left))
            if current_month.text != previous_month:
                assert False
    elif how_many_months > 0:
        for i in range(abs(how_many_months)):
            next_month = (datetime.datetime.strptime(current_month.text, "%B %Y") + relativedelta(months = 1)).strftime("%B %Y")
            click_button(True, load_element(button_right))
            if current_month.text != next_month:
                assert False

def change_day(is_check_out, which_day):
    div = str(int(is_check_out) + 1)
    days_list = setup.driver.find_elements(By.XPATH, "/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[" + div +"]/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[/*]/div[/*]")

    for day in days_list:
        if day.text == str(which_day):
            click_button(True, day)
            break

# -------------------------- Form Text Fields Test Functions  --------------------------

def wait_for_form_elements_to_load(text_fields):
    if setup.driver.current_url.startswith("https://automationintesting.online/reservation/"):
        for name in text_fields:
           load_element("/html/body/div[2]/div/div[2]/div/div[2]/div/div/form/div[" + str(text_fields.index(name) + 1) + "]/input")  
    else:
        for id in text_fields:
            wf.wait_for_element_id(getattr(id, "name"))  

def verify_form_success(logins):
    if setup.driver.current_url.startswith("https://automationintesting.online/reservation/"):
        wf.wait_for_element_xpath("/html/body/div[2]/div/div[2]/div/div[2]/div/div")
        ConfirmationElementList = setup.driver.find_elements(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div/*")
        if ConfirmationElementList[0].text == "Booking Confirmed":
            assert True
        if ConfirmationElementList[1].text == "Your booking has been confirmed for the following dates:":
            assert True
    else:
        wf.wait_for_element_xpath("/html/body/div[2]/div/section[3]/div/div/div/div/div/p[2]")
        ConfirmationElementList = setup.driver.find_elements(By.XPATH, "/html/body/div[2]/div/section[3]/div/div/div/div/div/*")
        if ConfirmationElementList[0].text == "Thanks for getting in touch " + getattr(logins, "name") + "!":
            assert True
        if ConfirmationElementList[1].text == "We'll get back to you about":
            assert True
        if ConfirmationElementList[2].text == getattr(logins, "subject"):
            assert True
        if ConfirmationElementList[3].text == "as soon as possible.":
            assert True

def verify_form_failure(error_list):
    element = None
    ErrorElementList = None

    if setup.driver.current_url.startswith("https://automationintesting.online/reservation/"):
        element = load_element("/html/body/div[2]/div/div[2]/div/div[2]/div/div/form/div[5]/ul/li[1]")
        wf.wait_for_element_visible(element)
        ErrorElementList = setup.driver.find_elements(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div/form/div[5]/ul/*")

    else:
        element = load_element("/html/body/div[2]/div/section[3]/div/div/div/div/div/div/p[1]")
        wf.wait_for_element_visible(element)
        ErrorElementList = setup.driver.find_elements(By.XPATH, "/html/body/div[2]/div/section[3]/div/div/div/div/div/div/*")

    for element in ErrorElementList:
        any_matches = False
        for error in error_list:
            if str(error) == element.text:
                any_matches = True
                error_list.remove(error)
        if any_matches == False:
            assert False

def populate_text_fields(text_fields, logins):
    if setup.driver.current_url.startswith("https://automationintesting.online/reservation/"):
        for id in text_fields:
            text_box = load_element("/html/body/div[2]/div/div[2]/div/div[2]/div/div/form/div[" + str(text_fields.index(id) + 1) + "]/input")  
            text_box.send_keys(getattr(logins, getattr(id, "name")))
    else:
        for id in text_fields:
            text_box = setup.driver.find_element(By.ID, getattr(id, "name")) 
            text_box.send_keys(getattr(logins, getattr(id, "name")))

def check_text(text_fields, logins):
    if setup.driver.current_url.startswith("https://automationintesting.online/reservation/"):
        for id in text_fields:
            text_box = load_element("/html/body/div[2]/div/div[2]/div/div[2]/div/div/form/div[" + str(text_fields.index(id) + 1) + "]/input")
            text_box.get_attribute("value") == getattr(logins, getattr(id, "name"))
    else:
        for id in text_fields:
            text_box = setup.driver.find_element(By.ID, getattr(id, "name")) 
            text_box.get_attribute("value") == getattr(logins, getattr(id, "name"))

def verify_data(text_fields, logins):
    errors = []
    for id in text_fields:
        text = id.verify_validity(getattr(logins, getattr(id, "name")))
        if text == None:
            pass
        elif isinstance(text, list):
            for item in text:
                errors.append(item)
        else:
            errors.append(text)
    return errors
