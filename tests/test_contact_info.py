#This test checks the consistency of contact info on the main page
# -------------------------- Imports --------------------------
import __init__
import Selenium2_Test.source.my_functions as mf

# -------------------------- Test --------------------------
mf.load_website()

def test_address():
    mf.compare_object_text("/html/body/div[2]/div/section[2]/div/div[2]/div[2]/div/div/div[1]/div[2]/p", "/html/body/div[2]/div/footer/div/div[1]/div[2]/ul/li[1]")

def test_phone():
    mf.compare_object_text("/html/body/div[2]/div/section[2]/div/div[2]/div[2]/div/div/div[2]/div[2]/p", "/html/body/div[2]/div/footer/div/div[1]/div[2]/ul/li[2]")

def test_email():
    mf.compare_object_text("/html/body/div[2]/div/section[2]/div/div[2]/div[2]/div/div/div[3]/div[2]/p", "/html/body/div[2]/div/footer/div/div[1]/div[2]/ul/li[3]")