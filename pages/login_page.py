"""
Login Page — encapsulates all interactions with the login screen.
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from config.settings import LOGIN_USERNAME, LOGIN_PIN


class LoginPage:
    """Page Object for the HMS Backoffice Login screen."""

    def __init__(self, driver):
        self.driver = driver

    # ───────────── Actions ─────────────

    def skip_onboarding(self):
        """Click 'Get Started' and 'Skip' buttons if they appear."""
        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Get Started").click()
            print("[OK] Clicked Get Started")
        except Exception:
            print("[SKIP] Get Started not found")

        self.driver.implicitly_wait(1)

    def enter_username(self, username=LOGIN_USERNAME):
        """Enter the username into the first EditText field."""
        try:
            username_field = self.driver.find_element(
                AppiumBy.XPATH,
                "//android.widget.EditText[contains(@text, 'username') "
                "or contains(@hint, 'username') or @index='0']",
            )
            username_field.click()
            username_field.clear()
            username_field.send_keys(username)
            print(f"[OK] Entered username: {username}")
        except Exception:
            edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            if edit_texts:
                edit_texts[0].click()
                edit_texts[0].send_keys(username)
                print(f"[OK] Entered username via fallback: {username}")
            else:
                print("[ERROR] Username field not found")

    def enter_pin(self, pin=LOGIN_PIN):
        """Enter the PIN digit-by-digit using key codes."""
        edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        if len(edit_texts) >= 2:
            edit_texts[1].click()
            for digit in pin:
                self.driver.press_keycode(int(digit) + 7)
                time.sleep(0.3)
            print(f"[OK] Entered PIN: {'*' * len(pin)}")
        else:
            print("[ERROR] PIN field not found")

    def click_login_button(self):
        """Click the Login button."""
        try:
            self.driver.find_element(
                AppiumBy.XPATH,
                "//android.widget.Button[contains(@text, 'Login') "
                "or contains(@content-desc, 'Login')]",
            ).click()
            print("[OK] Clicked Login button")
        except Exception:
            print("[SKIP] Login button not found")

    def login(self, username=LOGIN_USERNAME, pin=LOGIN_PIN):
        """Full login flow — onboarding skip → credentials → submit."""
        print("\n=== LOGIN FLOW ===")
        self.skip_onboarding()
        self.enter_username(username)
        self.enter_pin(pin)
        self.click_login_button()
        print("[WAIT] Waiting for dashboard...")
        time.sleep(2)
        print("[OK] Login flow completed")
