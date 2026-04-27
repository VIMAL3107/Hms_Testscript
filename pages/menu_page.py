"""
Menu Page — encapsulates navigation drawer / side-menu interactions.
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import EXPLICIT_WAIT_SHORT, MENU_LOAD_DELAY


class MenuPage:
    """Page Object for the side navigation menu."""

    def __init__(self, driver):
        self.driver = driver

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
        """Open the navigation drawer via swipe + menu button click."""
        print("\n=== OPEN MENU ===")
        try:
            self.dismiss_overlay()

            print("[INFO] Swiping left→right to open drawer...")
            self.driver.swipe(5, 500, 500, 500, 1000)
            time.sleep(1)

            wait = WebDriverWait(self.driver, EXPLICIT_WAIT_SHORT)

            def find_menu_btn(d):
                candidates = d.find_elements(
                    AppiumBy.XPATH,
                    "//android.widget.ImageView[@clickable='true' and @index='0']",
                )
                if candidates:
                    return candidates[0]
                for img in d.find_elements(
                    AppiumBy.XPATH, "//android.widget.ImageView[@clickable='true']"
                ):
                    if img.location["x"] < 150 and img.location["y"] < 250:
                        return img
                return None

            try:
                wait.until(find_menu_btn).click()
                print("[OK] Menu button clicked")
            except Exception:
                print("[SKIP] Menu button not found, swipe may have worked")

            time.sleep(MENU_LOAD_DELAY)
        except Exception:
            print("[FALLBACK] Tapping menu coordinates (67, 131)")
            self.driver.tap([(67, 131)])
            time.sleep(1)

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

    def navigate_to(self, menu_item_name):
        """
        Full flow: open drawer → search → click menu item.
        Returns True on success.
        """
        self.open_drawer()
        return self.search_and_navigate(menu_item_name)
