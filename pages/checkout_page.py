

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config.settings import EXPLICIT_WAIT_SHORT, EXPLICIT_WAIT_DEFAULT, MENU_LOAD_DELAY
from pages.menu_page import MenuPage


class CheckoutPage:
    """Page Object for the Check-Out flow."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT_DEFAULT)

    # ───────────── Navigation ─────────────

    def navigate_to_checkout(self):
        """Open the side menu, search for 'Check-Out', and click it."""
        print("\n=== NAVIGATING TO CHECK-OUT ===")
        menu = MenuPage(self.driver)
        result = menu.navigate_to("Check-In")
        time.sleep(2)
        return result

    # ───────────── Check-Out List Screen ─────────────

    def wait_for_screen(self):
        """Wait for the Check-In screen to load."""
        print("[WAIT] Waiting for Check-In screen...")
        time.sleep(MENU_LOAD_DELAY)
        try:
            self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[contains(@text,'Check-In') or contains(@content-desc,'Check-In') "
                    "or contains(@text,'Check In') or contains(@content-desc,'Check In') "
                    "or contains(@text,'Search by Guest') or contains(@content-desc,'Search by Guest')]",
                )
            )
            print("[OK] Check-In screen loaded")
            return True
        except TimeoutException:
            # Debug: print what's on screen
            print("[DEBUG] Screen elements:")
            try:
                all_els = self.driver.find_elements(
                    AppiumBy.XPATH, "//*[@text!='' or @content-desc!='']"
                )
                for el in all_els[:20]:
                    t = el.get_attribute('text') or ''
                    c = el.get_attribute('content-desc') or ''
                    if t or c:
                        print(f"  - Text: '{t}' | Desc: '{c[:80]}'")
            except Exception:
                pass
            print("[ERROR] Check-In screen did not load")
            return False

    def select_checked_in_booking(self):
        """Click the first booking that has 'CheckedIn' status. Scrolls to find one."""
        print("[INFO] Looking for a CheckedIn booking...")
        time.sleep(2)

        checkedin_xpath = (
            "//*[contains(@content-desc,'CheckedIn') or contains(@text,'CheckedIn') "
            "or contains(@content-desc,'Checked In') or contains(@text,'Checked In')]"
        )

        max_scrolls = 5
        checkedin = None
        for scroll in range(max_scrolls + 1):
            elements = self.driver.find_elements(AppiumBy.XPATH, checkedin_xpath)
            if elements:
                checkedin = elements[0]
                print(f"[OK] Found CheckedIn booking")
                break

            if scroll < max_scrolls:
                print(f"[INFO] Scrolling down to find CheckedIn... ({scroll + 1}/{max_scrolls})")
                size = self.driver.get_window_size()
                self.driver.swipe(
                    size["width"] // 2, int(size["height"] * 0.7),
                    size["width"] // 2, int(size["height"] * 0.3), 700
                )
                time.sleep(1.5)

        # Fallback: if no CheckedIn found, click any booking card
        if not checkedin:
            print("[WARN] No CheckedIn booking found. Clicking first available booking...")
            booking_xpath = "//*[contains(@content-desc,'#HBK') or contains(@text,'#HBK')]"
            bookings = self.driver.find_elements(AppiumBy.XPATH, booking_xpath)
            if bookings:
                checkedin = bookings[0]
                print(f"[OK] Found booking to click (fallback)")
            else:
                print("[ERROR] No bookings found at all")
                return False

        # Click the booking
        checkedin.click()
        print("[OK] Clicked booking")
        time.sleep(3)
        return True


    # ───────────── Guest Detail Screen ─────────────

    def wait_for_guest_detail(self):
        """Wait for the guest detail screen to load."""
        print("[WAIT] Waiting for guest detail screen...")
        try:
            self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[contains(@text,'Booking Details') or contains(@content-desc,'Booking Details')]",
                )
            )
            print("[OK] Guest detail screen loaded")
            return True
        except TimeoutException:
            print("[ERROR] Guest detail screen did not load")
            return False

    def click_add_payment_button(self):
        """Click the 'Add Payment' button on the guest detail screen."""
        print("[INFO] Clicking 'Add Payment' button...")
        try:
            # Scroll down to see the buttons at the bottom
            size = self.driver.get_window_size()
            self.driver.swipe(
                size["width"] // 2, int(size["height"] * 0.8),
                size["width"] // 2, int(size["height"] * 0.3), 700
            )
            time.sleep(1)

            add_payment_btn = self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[(@text='Add Payment' or @content-desc='Add Payment') "
                    "and not(contains(@class,'TextView'))]",
                )
            )
            add_payment_btn.click()
            print("[OK] Clicked 'Add Payment'")
            time.sleep(2)
            return True
        except Exception as e:
            # Fallback: try any element with Add Payment text
            try:
                btns = self.driver.find_elements(
                    AppiumBy.XPATH,
                    "//*[contains(@text,'Add Payment') or contains(@content-desc,'Add Payment')]"
                )
                if btns:
                    btns[-1].click()  # Last one is usually the button at the bottom
                    print("[OK] Clicked 'Add Payment' (fallback)")
                    time.sleep(2)
                    return True
            except Exception:
                pass
            print(f"[ERROR] Add Payment button not found: {e}")
            return False

    def click_checkout_button(self):
        """Click the 'Check-Out' button on the guest detail screen."""
        print("[INFO] Clicking 'Check-Out' button...")
        try:
            checkout_btn = self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[@text='Check-Out' or @content-desc='Check-Out' "
                    "or @text='Checkout' or @content-desc='Checkout']",
                )
            )
            checkout_btn.click()
            print("[OK] Clicked 'Check-Out'")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"[ERROR] Check-Out button not found: {e}")
            return False

    # ───────────── Add Payment Screen ─────────────

    def wait_for_payment_screen(self):
        """Wait for the Add Payment screen to load."""
        print("[WAIT] Waiting for Add Payment screen...")
        try:
            self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[contains(@text,'Payment Method') or contains(@content-desc,'Payment Method') "
                    "or contains(@text,'Payment-01') or contains(@content-desc,'Payment-01')]",
                )
            )
            print("[OK] Add Payment screen loaded")
            return True
        except TimeoutException:
            print("[ERROR] Add Payment screen did not load")
            return False

    def select_payment_method(self, method="Cash"):
        """Open the Payment Method dropdown and select a method."""
        print(f"[INFO] Selecting payment method: {method}...")
        try:
            # Click the Payment Method dropdown
            dropdown = self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[contains(@text,'Payment Method') or contains(@content-desc,'Payment Method')]",
                )
            )
            dropdown.click()
            print("[OK] Payment Method dropdown opened")
            time.sleep(1)

            # Select the method (e.g., Cash)
            method_option = self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    f"//*[@text='{method}' or @content-desc='{method}']",
                )
            )
            method_option.click()
            print(f"[OK] Selected '{method}'")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to select payment method: {e}")
            return False

    def click_add_payment_submit(self):
        """Click the 'Add Payment' submit button on the payment screen."""
        print("[INFO] Submitting payment...")
        try:
            # The submit button is at the bottom of the screen
            btns = self.driver.find_elements(
                AppiumBy.XPATH,
                "//*[contains(@text,'Add Payment') or contains(@content-desc,'Add Payment')]"
            )
            if btns:
                btns[-1].click()  # Last "Add Payment" is the submit button
                print("[OK] Payment submitted")
                time.sleep(3)
                return True
            print("[ERROR] Submit button not found")
            return False
        except Exception as e:
            print(f"[ERROR] Failed to submit payment: {e}")
            return False
    
    def confirm_checkout(self):
        """Confirm the checkout dialog (Cancel / Checkout)."""
        print("[INFO] Confirming checkout dialog...")
        time.sleep(2)
        try:
            confirm_btn = self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[@text='Checkout' or @content-desc='Checkout' "
                    "or @text='Check-Out' or @content-desc='Check-Out' "
                    "or @text='Check Out' or @content-desc='Check Out' "
                    "or @text='Confirm' or @content-desc='Confirm']",
                )
            )
            confirm_btn.click()
            print("[OK] Confirmed checkout")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to confirm checkout: {e}")
            return False
    # ───────────── Full Checkout Flow ─────────────

    def full_checkout_flow(self, payment_method="Cash"):
        print("\n=== FULL CHECKOUT FLOW ===")

        if not self.select_checked_in_booking():
            return False 

        if not self.wait_for_guest_detail():
            return False

        if not self.click_add_payment_button():
            return False

        if not self.wait_for_payment_screen():
            return False

        self.select_payment_method(payment_method)
        self.click_add_payment_submit()

        time.sleep(3)
        self.wait_for_guest_detail()

        time.sleep(1)
        self.click_checkout_button()

        self.confirm_checkout()

        print("[OK] Checkout flow completed successfully")
        return True
  
    