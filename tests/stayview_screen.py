"""
Test Stay View — validates the Stay View screen functionality.
"""

import time
import unittest
from core.base_test import BaseTest
from pages.stayview import stayview_page
from pages.stayview_roomtransfer import RoomTransferPage


class TestStayView(BaseTest):
    """Test cases for the Stay View screen using stayview_page POM."""

    def test_01_stayview_full_flow(self):
        stayview = stayview_page(self.driver)
        roomtransfer = RoomTransferPage(self.driver)

        if not stayview.navigate_to_stayview():
            self.fail("Failed to navigate to Stay View screen")

        if not stayview.wait_for_screen():
            self.fail("Stay View screen did not load")

        if not stayview.select_first_occupied_room():
            self.fail("Failed to select an occupied room")
        
        if not stayview.Schedule_Cleaning():
            self.fail("Failed to complete Schedule Cleaning flow") 
        
        if not stayview.select_first_occupied_room():
            self.fail("Failed to select an occupied room")    
        
        if not stayview.add_charge():
            self.fail("Failed to add charge to room")        
       
        if not stayview.click_modify_stay():
            self.fail("Could not click Modify Stay")
        
        if not stayview.wait_for_modify_stay_dialog():
            self.fail("Modify Stay dialog did not open")

        #Modify checkout date
        
        if not stayview.tap_checkout_date_field():
            self.fail("Could not open checkout date picker")
        
        if not stayview.select_next_day():
            self.fail("Could not select next day")
        
        if not stayview.confirm_date_picker():
            self.fail("Could not confirm date")
        
        if not stayview.confirm_time_picker():
            self.fail("Could not confirm time")

        #Confirm the modification
        
        if not stayview.confirm_modify_stay():
            self.fail("Could not confirm Modify Stay")

        print("[OK] Stay View test completed successfully")



        # if not stayview.navigate_to_stayview():
        #     self.fail("Failed to navigate to Stay View screen")

        # if not stayview.wait_for_screen():
        #     self.fail("Stay View screen did not load")

        # if not stayview.select_first_occupied_room():
        #     self.fail("Failed to select an occupied room")

        if not roomtransfer.click_room_transfer():
            self.fail("Could not click Room Transfer")

        if not roomtransfer.select_room_type():
            self.fail("Could not select room type")

        if not roomtransfer.select_available_room():
            self.fail("Could not select available room")

        if not roomtransfer.select_reason_for_move():
            self.fail("Could not select reason")
        
        if not roomtransfer.click_confirm_move():
            self.fail("Failed to click 'Confirm Move' or handle 'Proceed' popup")  
        
        print("[OK] Room Transfer test completed successfully")


if __name__ == "__main__":
    unittest.main()
