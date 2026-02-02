#This test checks selecting different check in / check out dates behaviour
# -------------------------- Imports --------------------------
import __init__
import source.my_functions as mf
import pytest

# -------------------------- Test --------------------------
mf.load_website()

def test_check_in_before_check_out():
    mf.change_day(False, 10)
    mf.change_day(True, 15)

@pytest.mark.xfail
def test_check_in_same_check_out():
    mf.change_day(False, 12)
    mf.change_day(True, 12)
    #Check out should only be allowed to be set if after check in.

@pytest.mark.xfail
def test_check_in_after_check_out():
    mf.change_day(False, 8)
    mf.change_day(True, 6)
    #Check out should only be allowed to be set if after check in.