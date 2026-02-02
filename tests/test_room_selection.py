#This Test selects a room and checks the data in each one, if they match the data on the main page
# -------------------------- Imports --------------------------
import __init__
import pytest
import source.my_functions as mf
from tests.conftest import room_list
from datetime import datetime

# -------------------------- Setup --------------------------
def select_room(room):
    idx = room_list.index(room) + 1
    mf.click_button(True, mf.load_element("/html/body/div[2]/div/div/section[2]/div/div[2]/div[" + str(idx) + "]/div/div[3]/a"))

def verify_room_info_in(room, days):
    room_name = mf.load_element("/html/body/div[2]/div/div[2]/div/div[1]/div[1]/h1").text
    big_price = mf.load_element("/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/span[1]").text
    description = mf.load_element("/html/body/div[2]/div/div[2]/div/div[1]/div[3]/p").text
    small_price = mf.load_element("/html/body/div[2]/div/div[2]/div/div[2]/div/div/form/div[2]/div/div[1]/span[1]").text.split()[0]
    night_counter = mf.load_element("/html/body/div[2]/div/div[2]/div/div[2]/div/div/form/div[2]/div/div[1]/span[1]").text.split()[2]

    if getattr(room, "name") + " Room" != room_name:
        assert False

    if "£" + getattr(room, "price") != big_price:
        assert False

    if "£" + getattr(room, "price") != small_price:
        assert False

    if getattr(room, "description") != description:
        assert False

    if str(days - 1) != str(night_counter):
        assert False #Website often assumes #days = #nights, but that is wrong - Fails are expected here
    
# -------------------------- Test --------------------------
@pytest.fixture(params=room_list, ids=['Single', 'Double', 'Suite'])
def room(request):
    return request.param

def test_room_select_and_info(room, subtests):
    booked_days = int()
    with subtests.test("Set dates"):
        mf.load_website()
        check_in = mf.load_element("/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[1]/div[1]/div/input")
        check_out = mf.load_element("/html/body/div[2]/div/div/section[1]/div/div/div/form/div/div[2]/div[1]/div/input")

        mf.calendar_select_date(check_in, (2, 3))
        mf.calendar_select_date(check_out, (2, 4))

        date1 = str(check_in.get_attribute("value"))
        date_split1 = date1.split("/", 2)
        datetime1 = datetime(int(date_split1[2]), int(date_split1[1]), int(date_split1[0]))
        date2 = str(check_out.get_attribute("value"))
        date_split2 = date2.split("/", 2)
        datetime2 = datetime(int(date_split2[2]), int(date_split2[1]), int(date_split2[0]))
       
        booked_days = (datetime2 - datetime1).days

    with subtests.test("Select Room"):
        select_room(room)

    with subtests.test("Verify Room Information On Room Page"):
        verify_room_info_in(room, booked_days)
