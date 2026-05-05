"""
Base Test Class — every test class should inherit from this.
Handles setUp / tearDown and provides common utilities.
"""

import unittest
import time

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from core.driver_manager import DriverManager
from config.settings import (
    EXPLICIT_WAIT_DEFAULT,
    EXPLICIT_WAIT_SHORT,
    STABILIZE_DELAY,
)


class BaseTest(unittest.TestCase):
    """
    Base class for all HMS Backoffice Appium tests.
    Subclass this instead of unittest.TestCase directly.
    """

    driver_manager: DriverManager = None
    driver = None

    # ───────────── Lifecycle ─────────────

    def setUp(self):
        """Start a fresh Appium session before each test."""
        self.driver_manager = DriverManager()
        self.driver = self.driver_manager.start_driver()

    def tearDown(self):
        """Close the Appium session after each test."""
        if self.driver_manager:
            self.driver_manager.quit_driver()

    # ───────────── Helpers ─────────────

    def wait(self, timeout=EXPLICIT_WAIT_DEFAULT):
        """Return a WebDriverWait instance with configurable timeout."""
        return WebDriverWait(self.driver, timeout)

    def safe_click(self, locator_type, locator_value, label="element", timeout=EXPLICIT_WAIT_SHORT):
        """
        Wait for an element and click it.
        Returns True on success, False if the element was not found.
        """
        try:
            el = WebDriverWait(self.driver, timeout).until(
                lambda d: d.find_element(locator_type, locator_value)
            )
            el.click()
            print(f"[OK] Clicked {label}")
            return True
        except (TimeoutException, Exception) as e:
            print(f"[SKIP] {label} not found: {e}")
            return False

    def wait_for_element(self, locator_type, locator_value, timeout=EXPLICIT_WAIT_DEFAULT):
        """Wait for and return an element, or raise TimeoutException."""
        return WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(locator_type, locator_value)
        )

    def find_elements_safe(self, locator_type, locator_value):
        """Find elements without raising an exception if none are found."""
        return self.driver.find_elements(locator_type, locator_value)

    def tap_coordinates(self, x, y, label=""):
        """Tap at absolute screen coordinates."""
        self.driver.tap([(x, y)])
        print(f"[OK] Tapped at ({x}, {y}){' — ' + label if label else ''}")

    def swipe_screen(self, start_x_pct=0.5, start_y_pct=0.8, end_x_pct=0.5, end_y_pct=0.3, duration=700):
        """Swipe using percentage-based coordinates."""
        size = self.driver.get_window_size()
        sx = int(size["width"] * start_x_pct)
        sy = int(size["height"] * start_y_pct)
        ex = int(size["width"] * end_x_pct)
        ey = int(size["height"] * end_y_pct)
        self.driver.swipe(sx, sy, ex, ey, duration)


    def hide_keyboard_safe(self):
        """Hide the soft keyboard if visible."""
        try:
            self.driver.hide_keyboard()
        except Exception:
            pass

    def ensure_driver_alive(self):
        """Delegate to DriverManager's ensure_alive, updating self.driver."""
        alive = self.driver_manager.ensure_alive()
        self.driver = self.driver_manager.driver
        return alive
