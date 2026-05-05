"""
Test Reservation — validates the Reservation creation flow.
"""

import time
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from pages.reservation_page import ReservationPage


class TestReservation(BaseTest):
    """Test cases for the Reservation screen."""

    def test_01_create_reservation(self):
        """Login → Navigate to Reservation → Add new reservation with dates and room."""
        # Step 1: Login
        login_page = LoginPage(self.driver)
        login_page.login()

        # Step 2: Navigate via menu
        menu_page = MenuPage(self.driver)
        menu_page.navigate_to("Reservation")

        # Step 3: Interact with Reservation screen
        reservation_page = ReservationPage(self.driver)
        reservation_page.wait_for_screen()
        reservation_page.click_fab_button()

        # Step 4: Select dates
        try:
            reservation_page.click_checkin_field()
            reservation_page.select_dates("28", "29")
            reservation_page.confirm_calendar()
        except Exception as e:
            print(f"[ERROR] Date selection failed: {e}")

        # Step 5: Select room type
        reservation_page.select_room_type("King Suite")


        # Step 7: Add Adults (example: +2)
        reservation_page.add_adults(2)

        # Step 8: Add Children (example: +1)
        reservation_page.add_children(1)

        # Step 9: Enter Mobile Number

        reservation_page.enter_mobile_number("7540062368")
         
        # Step 10: Enter Guest Name

        reservation_page.enter_guest_name("Leo")

        # Step 11: Enter Email

        reservation_page.enter_email("leo@gmail.com")

        # Step 12: Enter Address

        reservation_page.enter_address(
        "Vetri theatre\nEast Tambaram, Tambaram, Chennai, Tamil Nadu"
        )

        # Step 13: Click Reserve Button

        reservation_page.click_reserve_all_guests()

        # Step 14: Click Proceed Button
        reservation_page.click_proceed_button()
        print("[OK] Reservation fully completed")


if __name__ == "__main__":
    import unittest
    unittest.main()
