"""
Menu Page — encapsulates navigation drawer / side-menu interactions.
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import EXPLICIT_WAIT_SHORT, MENU_LOAD_DELAY


from pages.base_page import BasePage

class MenuPage(BasePage):
    """Page Object for the side navigation menu."""

    # ───────────── Actions ─────────────

    def dismiss_overlay(self):
        """Dismiss any overlay / popup that might be covering the screen."""
        overlays = self.driver.find_elements(
            AppiumBy.XPATH,
            "//*[contains(@content-desc, 'Hotel M') "
            "or contains(@content-desc, 'Thanjav') "
            "or @class='android.widget.PopupWindow']",
        )
        if overlays:
            print("[INFO] Overlay detected, dismissing...")
            self.driver.back()
            time.sleep(1)

    def open_drawer(self):
        """Open the navigation drawer."""
        print("\n=== OPEN MENU ===")
        try:
            # Dismiss twice to be sure
            self.dismiss_overlay()
            self.dismiss_overlay()
            
            wait = WebDriverWait(self.driver, 10)
            menu_btn = wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    '(//android.widget.ImageView[@clickable="true"])[1]',
                )
            )
            menu_btn.click()
            time.sleep(1.5)
            print("[OK] Menu drawer opened")
            return True
        except Exception:
            print("[FALLBACK] Tapping menu coordinates (67, 131)")
            self.driver.tap([(67, 131)])
            time.sleep(1)
            return True

    def search_and_navigate(self, menu_item_name):
        """
        Type into the search bar inside the menu and click the matching item.
        Returns True on success, False on failure.
        """
        wait = WebDriverWait(self.driver, EXPLICIT_WAIT_SHORT)
        try:
            search = wait.until(
                lambda d: d.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
            )
            search.click()
            time.sleep(1)

            # Clear existing text
            try:
                search.clear()
                time.sleep(1)
            except Exception:
                pass

            current_text = search.get_attribute("text") or ""
            if current_text and current_text != "Search":
                search.send_keys("\b" * (len(current_text) + 5))

            time.sleep(1)
            search.send_keys(menu_item_name)
            print(f"[OK] Typed '{menu_item_name}' in search bar")
            time.sleep(1)

            # Hide keyboard
            try:
                self.driver.hide_keyboard()
            except Exception:
                pass

            # Click the menu item (exclude the EditText itself)
            menu_btn = wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    f"//*[not(contains(@class, 'EditText')) and "
                    f"(contains(@text,'{menu_item_name}') or contains(@content-desc,'{menu_item_name}'))]",
                )
            )
            menu_btn.click()
            print(f"[OK] Clicked '{menu_item_name}'")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to navigate to '{menu_item_name}': {e}")
            return False

    def navigate_to(self, menu_item_names, force_search=False):
        """
        Full flow: open drawer → try direct find → fallback to search.
        Can accept a string or a list of variations.
        """
        if isinstance(menu_item_names, str):
            menu_item_names = [menu_item_names]

        self.open_drawer()
        
        if not force_search:
            for name in menu_item_names:
                # Try direct find first
                try:
                    xpath = f"//*[not(contains(@class, 'EditText')) and (contains(@text,'{name}') or contains(@content-desc,'{name}'))]"
                    item = self.driver.find_element(AppiumBy.XPATH, xpath)
                    if item.is_displayed():
                        item.click()
                        print(f"[OK] Direct clicked '{name}'")
                        self.wait_for_loading()
                        return True
                except:
                    pass

        # Fallback to search (or forced search) variations one by one
        for name in menu_item_names:
            if self.search_and_navigate(name):
                self.wait_for_loading()
                return True
        
        return False
