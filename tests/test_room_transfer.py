"""
Test Room Transfer — validates the Room Transfer flow from Stay View.
"""

import time
import unittest
from core.base_test import BaseTest
from pages.stayview import stayview_page
from pages.stayview_roomtransfer import RoomTransferPage


class TestRoomTransfer(BaseTest):
    """Test cases for the Room Transfer flow."""

    def test_01_room_transfer_flow(self):
        stayview = stayview_page(self.driver)
        roomtransfer = RoomTransferPage(self.driver)

        if not stayview.navigate_to_stayview():
            self.fail("Failed to navigate to Stay View screen")

        if not stayview.wait_for_screen():
            self.fail("Stay View screen did not load")

        if not stayview.select_first_occupied_room():
            self.fail("Failed to select an occupied room")

        if not roomtransfer.click_room_transfer():
            self.fail("Could not click Room Transfer")

        if not roomtransfer.select_room_type():
            self.fail("Could not select room type")

        if not roomtransfer.select_available_room():
            self.fail("Could not select available room")

        if not roomtransfer.select_reason_for_move():
            self.fail("Could not select reason")
        
        if not roomtransfer.click_confirm_move():
            self.fail()  
        if not roomtransfer.click_confirm_move():
            self.fail()     

        print("[OK] Room Transfer test completed successfully")


if __name__ == "__main__":
    unittest.main()
