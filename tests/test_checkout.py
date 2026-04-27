"""
Test Checkout — validates the complete Check-Out flow.
"""

from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage


class TestCheckout(BaseTest):
    """Test cases for the Check-Out flow."""

    def test_01_checkout_with_payment(self):
        """Login → Navigate to Check-Out → Select booking → Add Payment → Check-Out."""
        # Step 1: Login
        login_page = LoginPage(self.driver)
        login_page.login()

        # Step 2: Navigate to Check-Out List
        checkout_page = CheckoutPage(self.driver)
        checkout_page.navigate_to_checkout()

        # Step 3: Wait for screen
        if not checkout_page.wait_for_screen():
            self.fail("Check-Out List screen did not load")

        # Step 4: Run the full checkout flow (select booking → payment → checkout)
        checkout_page.full_checkout_flow(payment_method="Cash")

        print("[OK] Checkout test completed")


if __name__ == "__main__":
    import unittest
    unittest.main()
