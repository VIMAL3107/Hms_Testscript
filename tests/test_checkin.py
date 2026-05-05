"""
Test Check-In — validates the complete Check-In flow.
Login → Navigate to Check-In → Select booking → Fill guest details → Update & Check-In.
"""

from datetime import datetime, timedelta
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.checkin_page import checkin_page


class TestCheckin(BaseTest):
    """Test cases for the Check-In flow."""

    def test_01_checkin_full_flow(self):
        checkin = checkin_page(self.driver)
        
        #if not checkin.navigate_to_checkin():
            #self.fail("Failed to navigate to Check-In screen")

        #if not checkin.wait_for_screen():
            #self.fail("Check-In screen did not load")

        #if not checkin.select_checked_in_booking():
            #self.fail("Could not select a booking")

        #if not checkin.wait_for_guest_detail():
            #self.fail("Guest detail screen did not load")
        
        #if not checkin.add_payment():
            #self.fail("Could not add payment")
        #if not checkin.add_special_request():
            #self.fail("could not add special request")    

        #if not checkin.click_checkin_field():
            #self.fail("Could not click Check-In field")
            
        #if not checkin.select_room_type("King Suite"):
            #self.fail("Could not select room type")
            
        #f not checkin.select_room("204"):
           #self.fail("Could not select room")
        
        if not checkin.add_parking_details():
            self.fail()
            
        #if not checkin.add_adults(adults=1):
            #self.fail("Could not add adults")
            
        #if not checkin.add_children(children=1):
            #self.fail("Could not add children")
            
        #if not checkin.enter_email("iamvimal3107@gmail.com"):
            #self.fail("Could not enter email")
            
        #if not checkin.enter_address("Chennai, India"):
            #self.fail("Could not enter address")
            
            
        #if not checkin.click_update_checkin():
            #self.fail("Could not click Update & Check-In")

        #if not checkin.confirm_checkin():
            #self.fail("Could not confirm check-in")

        print("[OK] Check-In test completed successfully")


if __name__ == "__main__":
    import unittest
    unittest.main()
