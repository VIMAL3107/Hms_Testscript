"""
Login Page — encapsulates all interactions with the login screen.
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from config.settings import LOGIN_USERNAME, LOGIN_PIN


from pages.base_page import BasePage

class LoginPage(BasePage):
    """Page Object for the HMS Backoffice Login screen."""

    # ───────────── Actions ─────────────

    @BasePage.auto_wait
    def skip_onboarding(self):
        """Click 'Get Started' and 'Skip' buttons if they appear."""
        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Get Started").click()
            print("[OK] Clicked Get Started")
        except Exception:
            print("[SKIP] Get Started not found")

        self.driver.implicitly_wait(1)

    @BasePage.auto_wait
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
        
        # Hide keyboard to ensure remaining fields render
        try:
            self.driver.hide_keyboard()
            time.sleep(1)
        except Exception:
            pass

    @BasePage.auto_wait
    def enter_pin(self, pin=LOGIN_PIN):
        """Enter the PIN digit-by-digit using key codes."""
        try:
            # Wait for any previous keyboard transitions (from username field) to settle
            time.sleep(1)
            edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            if len(edit_texts) >= 2:
                pin_field = edit_texts[1]
                pin_field.click()
                
                # Crucial: Wait for focus and numeric pad to be ready before sending keys
                print(f"[INFO] Focus on PIN field, waiting for numeric pad...")
                time.sleep(1.5)
                
                print(f"[INFO] Entering {len(pin)}-digit PIN...")
                for digit in pin:
                    # Keycode 7 is '0', 8 is '1', ..., 16 is '9'
                    # Calculation: int(digit) + 7
                    self.driver.press_keycode(int(digit) + 7)
                    time.sleep(0.5)  # Delay between digits for stability
                
                print(f"[OK] Entered PIN: {'*' * len(pin)}")
            else:
                print("[ERROR] PIN field not found (expected at least 2 EditTexts)")
                # Debug dump if field not found
                self._debug_dump_elements()
        except Exception as e:
            print(f"[ERROR] Failed to enter PIN: {e}")

    def _debug_dump_elements(self):
        """Dump visible elements for debugging purposes."""
        print("=== PAGE SOURCE DUMP ===")
        try:
            all_els = self.driver.find_elements(AppiumBy.XPATH, "//*[@text!='' or @content-desc!='']")
            for el in all_els[:20]:
                t = el.get_attribute('text') or ''
                c = el.get_attribute('content-desc') or ''
                print(f"  - Text: '{t}' | Desc: '{c[:50]}'")
        except Exception:
            print("(Could not dump elements)")
        print("=== END DUMP ===")

    @BasePage.auto_wait
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

    @BasePage.auto_wait
    def login(self, username=LOGIN_USERNAME, pin=LOGIN_PIN):
        """Full login flow — skip if already on Dashboard."""
        print("\n=== LOGIN FLOW ===")
        
        # Check if we are already on the Dashboard
        try:
            self.driver.implicitly_wait(2)
            dashboard = self.driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc,'Dashboard Overview') or contains(@text,'Dashboard Overview')]")
            if dashboard:
                print("[OK] Already on Dashboard, skipping login.")
                return True
        except:
            pass
        finally:
            self.driver.implicitly_wait(5)

        self.skip_onboarding()
        self.enter_username(username)
        self.enter_pin(pin)
        self.click_login_button()
        print("[WAIT] Waiting for dashboard...")
        time.sleep(2)
        self.wait_for_loading()
        print("[OK] Login flow completed")
        return True
