#This test fills out the contact form with the data given to it in the 'clients' list
# -------------------------- Imports ----------------------
import __init__
import datetime
import source.my_functions as mf

# -------------------------- Functions --------------------------

def verify_default_dates(check_in_field, check_out_field):
    if datetime.datetime.today().strftime("%d/%m/%Y") != check_in_field.get_attribute("value") and (datetime.datetime.today() + datetime.timedelta(days = 1)).strftime("%d/%m/%Y") != check_out_field.get_attribute("value"):
        assert False

# -------------------------- Test --------------------------
mf.load_website()
check_in_field = mf.load_element("/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[1]/div[1]/div/input")
check_out_field = mf.load_element("/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[2]/div/div/input")

def test_default_date_field_value():
    verify_default_dates(check_in_field, check_out_field)

# --- Check In ---
def test_date_selection_check_in():
    mf.check_date(False)
def test_change_month_check_in():
    mf.change_month(False, -2)
    mf.change_month(False, 2)
def test_change_day_check_in():
    mf.change_day(False, 10)
def test_date_after_changes_check_in():
    mf.check_date(False)

# --- Check Out ---
def test_date_selection_check_out():
    mf.check_date(True)
def test_change_month_check_out():
    mf.change_month(True, 2)
    mf.change_month(True, -2)
def test_change_day_check_out():
    mf.change_day(True, 10)
def test_date_after_changes_check_out():
    mf.check_date(True)
