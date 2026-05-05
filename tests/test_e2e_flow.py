import unittest
import time
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.checkin_page import checkin_page
from pages.checkout_page import CheckoutPage
from pages.menu_page import MenuPage
from pages.reservation_page import ReservationPage

class TestE2EFlow(BaseTest):
    """End-to-End flow: Login -> Reservation -> Check-In -> Checkout."""

    def test_complete_guest_cycle(self):
        print("\n=========================================")
        print("   STARTING END-TO-END GUEST CYCLE TEST")
        print("=========================================\n")

        login_page = LoginPage(self.driver)
        self.assertTrue(login_page.login(), "Login failed")

        menu_page = MenuPage(self.driver)
        menu_page.navigate_to("Reservation")

        # Step 3: Interact with Reservation screen
        reservation_page = ReservationPage(self.driver)
        self.assertTrue(reservation_page.wait_for_screen(), "Failed to load Reservation screen")
        self.assertTrue(reservation_page.click_fab_button(), "Failed to click Reservation FAB (+)")

        # Step 4: Select dates (Automatically connects today and tomorrow)
        self.assertTrue(reservation_page.click_checkin_field(), "Failed to click check-in field")
        self.assertTrue(reservation_page.select_auto_dates(), "Failed to select auto dates")
        self.assertTrue(reservation_page.confirm_calendar(), "Failed to confirm calendar selection")

        # Step 5: Select room type
        self.assertTrue(reservation_page.select_room_type("Family Suite"), "Failed to select room type")
        self.assertTrue(reservation_page.add_adults(2), "Failed to add adults")     
        self.assertTrue(reservation_page.add_children(1), "Failed to add children")
        self.assertTrue(reservation_page.enter_mobile_number("8786442299"), "Failed to enter mobile number")
        self.assertTrue(reservation_page.enter_guest_name("steeve"), "Failed to enter guest name")
        self.assertTrue(reservation_page.enter_email("steeve@gmail.com"), "Failed to enter email")

        self.assertTrue(reservation_page.enter_address("Ganapathipuram\nEast kerala"), "Failed to enter address")
        self.assertTrue(reservation_page.click_reserve_all_guests(), "Failed to click 'Reserve All Guests'")
        self.assertTrue(reservation_page.click_proceed_button())
        print("[OK] Reservation fully completed")
        
        # Navigate back to Dashboard to prepare for Check-In flow
        self.assertTrue(reservation_page.go_to_dashboard_from_reservation(), "Failed to return to Dashboard")
        
        print("\n--- Starting Check-In Flow ---")
        checkin = checkin_page(self.driver)
        self.assertTrue(checkin.navigate_to_checkin(), "Failed to navigate to Check-In")
        self.assertTrue(checkin.wait_for_screen(), "Check-In screen did not load")
        self.assertTrue(checkin.select_checked_in_booking(), "Failed to select booking for Check-In")
        self.assertTrue(checkin.wait_for_guest_detail(), "Guest detail did not load")
        self.assertTrue(checkin.click_checkin_field(), "Failed to click check-in field")
        self.assertTrue(checkin.select_room_type("Standard King"), "Failed to select room type")
        self.assertTrue(checkin.select_room(), "Failed to select dynamic room")
        self.assertTrue(checkin.add_adults(2), "Failed to add adults")
        self.assertTrue(checkin.add_children(1), "Failed to add children")
        self.assertTrue(checkin.click_update_checkin(), "Failed to click Update & Check-in")
        self.assertTrue(checkin.confirm_checkin(), "Failed to confirm check-in")
        self.assertTrue(checkin.go_to_dashboard_from_checkin(), "Failed to return to dashboard after Check-In")
        
        # -----------------------------------------
        print("\n--- Starting Checkout Flow ---")
        checkout = CheckoutPage(self.driver)
        self.assertTrue(checkout.navigate_to_checkout(), "Failed to navigate to Check-Out")
        self.assertTrue(checkout.wait_for_screen(), "Check-Out screen did not load")
        self.assertTrue(checkout.select_checked_in_booking(), "Failed to select checked-in booking")
        self.assertTrue(checkout.wait_for_guest_detail(), "Guest detail did not load on Checkout")
        
        # Handle payment first
        self.assertTrue(checkout.click_add_payment_button(), "Failed to click Add Payment")
        self.assertTrue(checkout.wait_for_payment_screen(), "Payment screen did not load")
        self.assertTrue(checkout.select_payment_method("Cash"), "Failed to select payment method")
        self.assertTrue(checkout.click_add_payment_submit(), "Failed to submit payment")
        
        time.sleep(2)
        # Now Check out
        self.assertTrue(checkout.wait_for_guest_detail(), "Guest detail did not reload")
        self.assertTrue(checkout.click_checkout_button(), "Failed to click Check-Out button")
        self.assertTrue(checkout.confirm_checkout(), "Failed to confirm checkout dialog")

        print("\n[OK] =========================================")
        print("[OK] END-TO-END FLOW COMPLETED SUCCESSFULLY!")
        print("[OK] =========================================\n")

if __name__ == "__main__":
    unittest.main()
