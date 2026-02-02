#This test fills out the contact form with the data given to it in the 'clients' list
# -------------------------- Imports ----------------------
import __init__
import pytest
import Selenium2_Test.source.wait_functions as wf
import Selenium2_Test.source.my_functions as mf
from Selenium2_Test.tests.conftest import Client2
from Selenium2_Test.tests.conftest import TextField_Name
from Selenium2_Test.tests.conftest import TextField_Email
from Selenium2_Test.tests.conftest import TextField_Phone

# -------------------------- Data setup --------------------------
form_errors = []
text_fields = [
    TextField_Name("firstname", 3, 18),
    TextField_Name("lastname", 3, 30),
    TextField_Email("email", 1),
    TextField_Phone("phone", 11, 21),
]   

#Clients testing different configuration of limitations + upper/lower boundaries of valid data
clients = [
    Client2("", "", "", ""),
    Client2("     ", "    ", "            ", "                "), #fail expected here, the phone number accepts empty characters, which should produce an error message
    Client2("Na", "La", "e@e..", "1234512345"),
    Client2("Nam", "Las", ".!#$%^@weirdmail", "12345123451"),
    Client2("Name That Is Very ", "Surename That Is Very Long Clo", "E@e", "123451234512345123451"), #fail possible here if room is already booked, the website throws an error
    Client2("Name That Is Very L", "Surename That Is Very Long Clos", "Email@email.com", "1234512345123451234512"),
    ]

# -------------------------- Test --------------------------
@pytest.fixture(params=clients)
def logins(request):
    return request.param

def test_group(logins, subtests):

    with subtests.test("Wait for form elements to load"):
        mf.load_website("https://automationintesting.online/reservation/1?checkin=2026-01-18&checkout=2026-01-19")
        mf.click_button(True, mf.load_element("/html/body/div[2]/div/div[2]/div/div[2]/div/div/form/button"))
        mf.wait_for_form_elements_to_load(text_fields)
   
    with subtests.test("Fill out form"):
        mf.populate_text_fields(text_fields, logins)
        
    with subtests.test("Check if text was entered"):
        mf.check_text(text_fields, logins)

    with subtests.test("Click the send button"):
        mf.click_button(True, mf.load_element("/html/body/div[2]/div/div[2]/div/div[2]/div/div/form/button[1]"))
    
    with subtests.test("Check if client data is acceptable"):
        element = mf.load_element("/html/body/div[2]/div/div[2]/div/div[2]/div/div/form/div[5]")
        wf.wait_for_element_visible(element)
        form_errors = mf.verify_data(text_fields, logins)

    if len(form_errors) == 0:
        with subtests.test("Verify room booking confirmation message"):
            mf.verify_form_success(logins)
    else:
        with subtests.test("Verify form data error info"):
            mf.verify_form_failure(form_errors)
