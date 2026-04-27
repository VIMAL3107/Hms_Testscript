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
        """Login → Navigate to Check-In → Select Reserved booking → Fill details → Check-In."""
        login_page = LoginPage(self.driver)
        login_page.login()

        checkin = checkin_page(self.driver)
        checkin.navigate_to_checkin()

        if not checkin.wait_for_screen():
            self.fail("Check-In screen did not load")

        if not checkin.select_checked_in_booking():
            self.fail("Could not select a booking")

        if not checkin.wait_for_guest_detail():
            self.fail("Guest detail screen did not load")

        checkin.click_checkin_field()
        checkin.select_room_type("King Suite")
        checkin.select_room("207")
        checkin.add_adults(adults=1)
        checkin.add_children(children=1)
        checkin.add_email("iamvimal3107@gmail.com")
        checkin.add_address("Chennai, India")
        checkin.click_update_checkin()

        checkin.confirm_checkin()

        print("[OK] Check-In test completed successfully")


if __name__ == "__main__":
    import unittest
    unittest.main()
