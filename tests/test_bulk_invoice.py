"""
Test Bulk Invoice — validates the Bulk Invoice download flow.
"""

import time
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from pages.bulk_invoice_page import BulkInvoicePage


class TestBulkInvoice(BaseTest):
    """Test cases for the Bulk Invoice screen."""

    def test_01_bulk_invoice_download(self):
        """Login → Navigate to Bulk Invoice → Select date range → Download."""
        # Step 1: Login
        login_page = LoginPage(self.driver)
        login_page.login()

        # Step 2: Navigate to Bulk Invoice via menu
        menu_page = MenuPage(self.driver)
        menu_page.navigate_to("Bulk Invoice")

        # Step 3: Interact with Bulk Invoice screen
        invoice_page = BulkInvoicePage(self.driver)

        if not invoice_page.wait_for_screen():
            self.fail("Bulk Invoice screen did not load")

        invoice_page.select_date_range("Last 7 Days")

        if not invoice_page.select_first_invoice():
            self.fail("Could not select any invoice")

        invoice_page.click_download()
        time.sleep(2)
        print("[OK] Bulk Invoice flow completed")


if __name__ == "__main__":
    import unittest
    unittest.main()
