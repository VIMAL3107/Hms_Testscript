"""
Bulk Invoice Page — encapsulates all Bulk Invoice screen interactions.
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config.settings import EXPLICIT_WAIT_LONG, EXPLICIT_WAIT_SHORT


class BulkInvoicePage:
    """Page Object for the Bulk Invoice screen."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT_LONG)

    # ───────────── Navigation ─────────────

    def navigate_to_bulk_invoice(self):
        """Open the side menu, search for 'Bulk Invoice', and click it."""
        print("\n=== NAVIGATING TO BULK INVOICE ===")
        wait = WebDriverWait(self.driver, EXPLICIT_WAIT_SHORT)

        # Step 1: Open drawer via swipe
        print("[INFO] Swiping to open menu...")
        self.driver.swipe(5, 500, 500, 500, 1000)
        time.sleep(1)

        # Step 2: Search for Bulk Invoice
        try:
            search = wait.until(
                lambda d: d.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
            )
            search.click()
            time.sleep(1)
            try:
                search.clear()
            except Exception:
                pass
            time.sleep(1)
            search.send_keys("Bulk Invoice")
            print("[OK] Typed 'Bulk Invoice' in search bar")
            time.sleep(1)
            try:
                self.driver.hide_keyboard()
            except Exception:
                pass
        except Exception as e:
            print(f"[ERROR] Search bar not found: {e}")
            return False

        # Step 3: Click the Bulk Invoice menu item
        try:
            menu_btn = wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[not(contains(@class, 'EditText')) and "
                    "(contains(@text,'Bulk Invoice') or contains(@content-desc,'Bulk Invoice'))]",
                )
            )
            menu_btn.click()
            print("[OK] Clicked Bulk Invoice menu item")
            return True
        except Exception as e:
            print(f"[ERROR] Bulk Invoice menu item not found: {e}")
            return False

    # ───────────── Waits / Verifications ─────────────

    def wait_for_screen(self):
        """Wait until the Bulk Invoice screen is loaded."""
        print("[WAIT] Waiting for Bulk Invoice screen to load...")
        try:
            self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[contains(@text, 'Last 7 Days') or contains(@content-desc, 'Last 7 Days')]",
                )
            )
            print("[OK] Bulk Invoice screen loaded")
            return True
        except TimeoutException:
            print("[ERROR] Bulk Invoice screen did not load")
            return False

    # ───────────── Date Range ─────────────

    def select_date_range(self, range_label="Last 7 Days"):
        """Open the date dropdown and select a range option."""
        print(f"[INFO] Selecting date range: {range_label}...")
        try:
            self.driver.find_element(
                AppiumBy.XPATH,
                "//*[contains(@text, 'Last 7 Days') or contains(@content-desc, 'Last 7 Days')]",
            ).click()
            print("[OK] Dropdown opened")
            time.sleep(1)

            self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    f"//*[contains(@text, '{range_label}') or contains(@content-desc, '{range_label}')]",
                )
            ).click()
            print(f"[OK] Selected '{range_label}'")
            time.sleep(2)
        except Exception as e:
            print(f"[SKIP] Dropdown interaction skipped: {e}")

    # ───────────── Invoice List ─────────────

    def get_invoices(self):
        """Wait for and return all invoice elements on screen."""
        print("[WAIT] Waiting for invoice list...")
        try:
            invoices = self.wait.until(
                lambda d: d.find_elements(
                    AppiumBy.XPATH,
                    "//*[contains(@text, 'INV') or contains(@content-desc, 'INV')]",
                ) or None
            )
            if invoices:
                print(f"[OK] Found {len(invoices)} invoice(s)")
                return invoices
            print("[ERROR] No invoices found")
            return []
        except TimeoutException:
            print("[ERROR] No invoices found (timeout)")
            return []

    def select_first_invoice(self):
        """Tap the checkbox area of the first invoice row."""
        print("[INFO] Selecting the first invoice...")
        invoices = self.get_invoices()
        if not invoices:
            return False

        target = invoices[0]
        label = target.get_attribute("text") or target.get_attribute("content-desc")
        print(f"[INFO] Target invoice: {label}")

        row_y = target.location["y"]
        row_h = target.size["height"]
        tap_x = 80
        tap_y = row_y + (row_h // 2)

        print(f"[INFO] Tapping checkbox at ({tap_x}, {tap_y})")
        self.driver.tap([(tap_x, tap_y)])
        print("[OK] Invoice selected")
        time.sleep(2)
        return True

    # ───────────── Download ─────────────

    def click_download(self):
        """Attempt to find and click the Download button."""
        print("[WAIT] Looking for Download button...")
        selectors = [
            "//*[contains(@text, 'Download') or contains(@content-desc, 'Download')]",
            "//*[contains(@text, 'selected') or contains(@content-desc, 'selected')]",
            "//android.widget.Button",
        ]

        for selector in selectors:
            btns = self.driver.find_elements(AppiumBy.XPATH, selector)
            for btn in btns:
                txt = btn.get_attribute("text") or btn.get_attribute("content-desc")
                if txt and "Download" in txt:
                    btn.click()
                    print(f"[OK] Clicked Download: {txt}")
                    return True

        # Fallback: search all clickable elements
        print("[WARNING] Searching all clickable elements for Download...")
        for el in self.driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']"):
            txt = el.get_attribute("text") or el.get_attribute("content-desc")
            if txt and ("Download" in txt or "selected" in txt):
                el.click()
                print(f"[OK] Download found via clickable search: {txt}")
                return True

        print("[ERROR] Download button not found")
        return False
