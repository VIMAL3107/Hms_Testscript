"""
Test Stay View — validates the Stay View screen functionality.
"""

import time
import unittest
from core.base_test import BaseTest
from pages.stayview import stayview_page
from pages.stayview_roomtransfer import RoomTransferPage
from pages.reservation_page import ReservationPage
from pages.checkin_page import checkin_page
from pages.checkout_page import CheckoutPage


class TestStayView(BaseTest):
    """Test cases for the Stay View screen using stayview_page POM."""

    def test_01_stayview_full_flow(self):
        stayview = stayview_page(self.driver)
        roomtransfer = RoomTransferPage(self.driver)
        reservation = ReservationPage(self.driver)
        checkin = checkin_page(self.driver)
        checkout = CheckoutPage(self.driver)

        # # Reservation & Balances
        # if not reservation.navigate_to_reservation():
        #     self.fail("Failed to navigate to Reservation")
        # if not reservation.wait_for_screen():
        #     self.fail("Reservation screen did not load") 
        # if not reservation.click_fab_button():
        #     self.fail("Failed to click FAB")
        # if not reservation.click_checkin_field():
        #     self.fail("Failed to click Check-In field") 
        # if not reservation.select_auto_dates():
        #     self.fail("Failed to select auto dates")  
        # if not reservation.confirm_calendar():
        #     self.fail("Failed to confirm calendar")
        
        # # Room Selection
        # if not reservation.select_room_type():
        #     self.fail("Failed to select room type")
        # if not reservation.add_adults(2):
        #     self.fail("Failed to enter add aduts") 
        # if not reservation.add_children(1):
        #     self.fail("Failed to enter add children")
        # if not reservation.get_guest_fields():
        #     self.fail("")      
        # if not reservation.enter_mobile_number("9876543210"):
        #     self.fail("Failed to enter mobile number")
        # if not reservation.enter_guest_name("John Doe"):
        #     self.fail("Failed to enter guest name")  
        # if not reservation.enter_email("john.doe@example.com"):
        #     self.fail("Failed to enter email")    
        # if not reservation.enter_address("123 Guest Street, City"):
        #     self.fail("Failed to enter address") 
        # if not reservation.click_reserve_all_guests():
        #     self.fail("Failed to click Reserve All Guests")
        # if not reservation.click_add_button():
        #     self.fail("Failed to click Add button")       
        # if not reservation.go_to_dashboard_from_reservation():
        #     self.fail("Failed to navigate back to dashboard") 
               

     

        # # Check-In
        if not checkin.navigate_to_checkin():
            self.fail("Failed to navigate to Check-In")
        if not checkin.wait_for_screen():
            self.fail("Check-In screen did not load")
        if not checkin.select_checked_in_booking():
            self.fail("Failed to select reserved booking for check-in")
        if not checkin.wait_for_guest_detail():
            self.fail("Guest detail screen did not load during check-in")
        if not checkin.add_payment():
            self.fail("Failed to click add payment") 
        if not checkin.add_special_request():
            self.fail("Failed to click add special request")
        if not checkin.confirm_checkin():
            self.fail("Failed to confirm check-in popup")
        
        if not checkin.click_update_checkin():
            self.fail("Failed to click Update & Check-in")
        if not checkin.confirm_checkin():
            self.fail("Failed to confirm check-in")
        if not reservation.go_to_dashboard_from_reservation():
             self.fail("Failed to navigate back to dashboard")     
        print("[OK] Check-In completed successfully")

                
        # Check-Out
        if not checkin.navigate_to_checkin():
            self.fail("Failed to navigate to Check-In")
        if not checkout.wait_for_screen():
            self.fail("Check-Out screen did not load")
        if not checkout.select_checked_in_booking():
            self.fail("Failed to select checked-in booking for check-out")
        if not checkout.wait_for_guest_detail():
            self.fail("Guest detail screen did not load during check-out")
        if not checkout.click_checkout_button():
            self.fail("Failed to click Check-Out button")
        if not checkout.confirm_checkout():
            self.fail("Failed to confirm check-out")
        print("[OK] Check-Out completed successfully")


        # if not stayview.navigate_to_stayview():
        #     self.fail("Failed to navigate to Stay View screen")

        # if not stayview.wait_for_screen():
        #     self.fail("Stay View screen did not load")

        # if not stayview.select_first_occupied_room():
        #     self.fail("Failed to select an occupied room")
        
        # if not stayview.Schedule_Cleaning():
        #     self.fail("Failed to complete Schedule Cleaning flow") 
        
        # if not stayview.select_first_occupied_room():
        #     self.fail("Failed to select an occupied room")    
        
        # if not stayview.add_charge():
        #     self.fail("Failed to add charge to room")        
       
        # if not stayview.click_modify_stay():
        #     self.fail("Could not click Modify Stay")
        
        # if not stayview.wait_for_modify_stay_dialog():
        #     self.fail("Modify Stay dialog did not open")

        # #Modify checkout date
        
        # if not stayview.tap_checkout_date_field():
        #     self.fail("Could not open checkout date picker")
        
        # if not stayview.select_next_day():
        #     self.fail("Could not select next day")
        
        # if not stayview.confirm_date_picker():
        #     self.fail("Could not confirm date")
        
        # if not stayview.confirm_time_picker():
        #     self.fail("Could not confirm time")

        # #Confirm the modification
        
        # if not stayview.confirm_modify_stay():
        #     self.fail("Could not confirm Modify Stay")

        # print("[OK] Stay View test completed successfully")



        # # if not stayview.navigate_to_stayview():
        # #     self.fail("Failed to navigate to Stay View screen")

        # # if not stayview.wait_for_screen():
        # #     self.fail("Stay View screen did not load")

        # # if not stayview.select_first_occupied_room():
        # #     self.fail("Failed to select an occupied room")

        # if not roomtransfer.click_room_transfer():
        #     self.fail("Could not click Room Transfer")

        # if not roomtransfer.select_room_type():
        #     self.fail("Could not select room type")

        # if not roomtransfer.select_available_room():
        #     self.fail("Could not select available room")

        # if not roomtransfer.select_reason_for_move():
        #     self.fail("Could not select reason")
        
        # if not roomtransfer.click_confirm_move():
        #     self.fail("Failed to click 'Confirm Move' or handle 'Proceed' popup")  
        
        # print("[OK] Room Transfer test completed successfully")


if __name__ == "__main__":
    unittest.main()
