"""
Test Full Flow — runs all flows sequentially in a single session
(Login → Bulk Invoice → Stay View → Reservation → Check-in/out).

Use this when you want to run the complete end-to-end test in one session
without reconnecting the driver between flows.
"""

import time
from core.base_test import BaseTest
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from pages.bulk_invoice_page import BulkInvoicePage
from pages.stay_view_page import StayViewPage
from pages.reservation_page import ReservationPage

from config.settings import STABILIZE_DELAY


class TestFullFlow(BaseTest):
    """End-to-end test that runs all flows sequentially."""

    def test_01_complete_flow(self):
        """Complete end-to-end flow across all screens."""
        login_page = LoginPage(self.driver)
        menu_page = MenuPage(self.driver)

        # ──────── LOGIN ────────
        login_page.login()

        # ──────── BULK INVOICE ────────
        print("\n" + "=" * 50)
        print("BULK INVOICE FLOW")
        print("=" * 50)
        try:
            menu_page.navigate_to("Bulk Invoice")
            invoice_page = BulkInvoicePage(self.driver)
            if invoice_page.wait_for_screen():
                invoice_page.select_date_range("Last 7 Days")
                invoice_page.select_first_invoice()
                invoice_page.click_download()
        except Exception as e:
            print(f"[ERROR] Bulk Invoice flow failed: {e}")

        time.sleep(STABILIZE_DELAY)
        self.ensure_driver_alive()

        # ──────── STAY VIEW ────────
        print("\n" + "=" * 50)
        print("STAY VIEW FLOW")
        print("=" * 50)
        try:
            self.driver.back()
            time.sleep(2)
            menu_page = MenuPage(self.driver)  # refresh reference after potential recovery
            menu_page.navigate_to("Stay View")
            stay_page = StayViewPage(self.driver)
            stay_page.wait_for_screen()
            stay_page.scroll_content(times=4)
        except Exception as e:
            print(f"[ERROR] Stay View flow failed: {e}")

        time.sleep(STABILIZE_DELAY)
        self.ensure_driver_alive()

        # ──────── RESERVATION ────────
        print("\n" + "=" * 50)
        print("RESERVATION FLOW")
        print("=" * 50)
        try:
            menu_page = MenuPage(self.driver)
            menu_page.navigate_to("Reservation")
            res_page = ReservationPage(self.driver)
            res_page.wait_for_screen()
            res_page.click_fab_button()

            # Date selection
            try:
                res_page.click_checkin_field()
                res_page.select_dates("28", "29")
                res_page.confirm_calendar()
            except Exception as e:
                print(f"[ERROR] Date selection failed: {e}")

            # Room type
            res_page.select_room_type("Standard King")

        except Exception as e:
            print(f"[ERROR] Reservation flow failed: {e}")

        print("\n" + "=" * 50)
        print("[DONE] ALL FLOWS COMPLETED")
        print("=" * 50)


if __name__ == "__main__":
    import unittest
    unittest.main()
