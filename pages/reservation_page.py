"""
Reservation Page — encapsulates Reservation screen interactions.
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import EXPLICIT_WAIT_DEFAULT, SCREEN_LOAD_DELAY


class ReservationPage:
    """Page Object for the Reservation screen."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT_DEFAULT)

    def wait_for_screen(self):
        """Wait for the Reservation screen to load."""
        print("[WAIT] Waiting for Reservation screen...")
        time.sleep(SCREEN_LOAD_DELAY)
        print("[OK] Reservation screen loaded")

    def click_fab_button(self):
        """Click the floating action button (+) to add a new reservation."""
        print("[INFO] Clicking FAB (+) button...")
        try:
            size = self.driver.get_window_size()
            x = int(size["width"] * 0.90)
            y = int(size["height"] * 0.82)
            self.driver.tap([(x, y)])
            print(f"[OK] Clicked FAB at ({x}, {y})")
            time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Failed to click FAB: {e}")

    # ──────── Date Selection ────────

    def click_checkin_field(self):
        """Click the Check-In date field to open the calendar."""
        print("[INFO] Clicking Check-In field...")
        checkin = self.wait.until(
            lambda d: d.find_element(
                AppiumBy.XPATH,
                "//*[contains(@text,'Check In') or contains(@content-desc,'Check In')]",
            )
        )
        checkin.click()
        time.sleep(2)
        print("[OK] Calendar opened")

    def select_dates(self, start_day, end_day):
        """Select start and end dates in the calendar picker."""
        print(f"[INFO] Selecting dates {start_day} to {end_day}...")

        start_els = self.wait.until(
            lambda d: d.find_elements(
                AppiumBy.XPATH,
                f"//*[@text='{start_day}' or contains(@content-desc, '{start_day}')]",
            )
        )
        if start_els:
            start_els[-1].click()
            print(f"[OK] Selected start date: {start_day}")
        time.sleep(1)

        end_els = self.wait.until(
            lambda d: d.find_elements(
                AppiumBy.XPATH,
                f"//*[@text='{end_day}' or contains(@content-desc, '{end_day}')]",
            )
        )
        if end_els:
            end_els[-1].click()
            print(f"[OK] Selected end date: {end_day}")
        time.sleep(2)

    def confirm_calendar(self):
        """Click OK to confirm the date selection."""
        print("[INFO] Confirming calendar...")
        self.wait.until(
            lambda d: d.find_element(
                AppiumBy.XPATH,
                "//*[contains(@text,'OK') or contains(@content-desc,'OK')]",
            )
        ).click()
        print("[OK] Calendar confirmed")
        time.sleep(3)

    # ──────── Room Type ────────

    def select_room_type(self, room_name="Standard King"):
        """Open the Room Type dropdown and select a room."""
        print(f"[INFO] Selecting room type: {room_name}...")
        try:
            room_field = self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().descriptionContains("Select Room Type")',
                )
            )

            location = room_field.location
            size = room_field.size
            print(f"[DEBUG] Room field at {location}, size {size}")

            # Multi-point tap strategy
            opened = False
            for offset in [0.2, 0.5, 0.8]:
                tx = location["x"] + int(size["width"] * offset)
                ty = location["y"] + (size["height"] // 2)
                print(f"[INFO] Tapping at {int(offset * 100)}% width: ({tx}, {ty})")
                self.driver.tap([(tx, ty)])
                time.sleep(2)

                if self.driver.find_elements(
                    AppiumBy.XPATH,
                    "//*[contains(@text,'King') or contains(@content-desc,'King')]",
                ):
                    print("[OK] Room type dropdown opened")
                    opened = True
                    break

            if not opened:
                print("[WARNING] Trying direct click...")
                try:
                    room_field.click()
                except Exception:
                    pass
                time.sleep(3)

            # Select the room
            self._select_room_option(room_name)

        except Exception as e:
            print(f"[ERROR] Room type selection failed: {e}")

    def _select_room_option(self, room_name):
        """Internal: select a room from the opened dropdown."""
        try:
            room_btn = self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    f"//*[contains(@text,'{room_name}') or contains(@content-desc,'{room_name}')]",
                )
            )
            room_btn.click()
            print(f"[OK] Selected {room_name}")
            return
        except Exception:
            pass

        # Fallback: broader search
        keyword = room_name.split()[-1]  # e.g., "King"
        print(f"[INFO] Broad search for '{keyword}'...")
        try:
            self.driver.find_element(
                AppiumBy.XPATH,
                f"//*[contains(@text,'{keyword}') or contains(@content-desc,'{keyword}')]",
            ).click()
            print(f"[OK] Selected via '{keyword}' search")
            return
        except Exception:
            pass

        # Fallback: scroll into view
        print("[INFO] Attempting scroll into view...")
        try:
            self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiScrollable(new UiSelector().scrollable(true))'
                f'.scrollIntoView(new UiSelector().textContains("{keyword}"))',
            ).click()
            print(f"[OK] Selected via scroll")
        except Exception:
            print(f"[ERROR] All attempts to select '{room_name}' failed")
