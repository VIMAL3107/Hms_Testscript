"""
Test Stay View — validates the Stay View screen navigation and scrolling.
"""

import time
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from pages.stay_view_page import StayViewPage


class TestStayView(BaseTest):
    """Test cases for the Stay View screen."""

    def test_01_stay_view_scroll(self):
        """Login → Navigate to Stay View → Scroll through content."""
        # Step 1: Login
        login_page = LoginPage(self.driver)
        login_page.login()

        # Step 2: Navigate via menu
        menu_page = MenuPage(self.driver)
        menu_page.navigate_to("Stay View")

        # Step 3: Interact with Stay View
        stay_view_page = StayViewPage(self.driver)
        stay_view_page.wait_for_screen()
        stay_view_page.scroll_content(times=4)

        print("[OK] Stay View flow completed")


if __name__ == "__main__":
    import unittest
    unittest.main()
