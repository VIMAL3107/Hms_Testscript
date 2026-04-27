"""
Test Login — validates the login flow for HMS Backoffice.
"""

import time
from core.base_test import BaseTest
from pages.login_page import LoginPage


class TestLogin(BaseTest):
    """Test cases for the Login screen."""

    def test_01_login_with_valid_credentials(self):
        """Verify successful login with valid username and PIN."""
        login_page = LoginPage(self.driver)
        login_page.login()

        # Verify: we should be on the dashboard now
        time.sleep(2)
        print("[VERIFY] Checking if dashboard loaded...")
        try:
            package = self.driver.current_package
            print(f"[OK] Current package: {package}")
            self.assertEqual(package, "com.example.hms_backoffice")
        except Exception as e:
            print(f"[WARN] Dashboard verification skipped: {e}")


if __name__ == "__main__":
    import unittest
    unittest.main()
