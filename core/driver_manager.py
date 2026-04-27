"""
Driver Manager — handles Appium WebDriver lifecycle.
Provides methods to create, quit, and recover the driver session.
"""

import time
from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.settings import CAPABILITIES, APPIUM_SERVER_URL


class DriverManager:
    """Manages the Appium WebDriver session lifecycle."""

    def __init__(self):
        self.driver = None

    def start_driver(self):
        """Create a new Appium driver session."""
        print("[DRIVER] Starting new Appium session...")
        options = UiAutomator2Options().load_capabilities(CAPABILITIES)
        self.driver = webdriver.Remote(
            command_executor=APPIUM_SERVER_URL,
            options=options,
        )
        print("[DRIVER] Session started successfully")
        return self.driver

    def quit_driver(self):
        """Quit the current driver session safely."""
        if self.driver:
            try:
                self.driver.quit()
                print("[DRIVER] Session closed")
            except Exception as e:
                print(f"[DRIVER] Error closing session: {e}")
            finally:
                self.driver = None

    def is_alive(self) -> bool:
        """Check if the current driver session is still responsive."""
        try:
            _ = self.driver.current_package
            return True
        except Exception:
            return False

    def ensure_alive(self) -> bool:
        """
        Verify driver health and attempt recovery if needed.
        Returns True if the driver is alive (or was recovered), False otherwise.
        """
        print("[DRIVER] Verifying driver health...")
        if self.is_alive():
            print("[DRIVER] Session is healthy")
            return True

        print("[RECOVERY] Driver lost. Attempting to reconnect...")
        for attempt in range(1, 3):
            try:
                self.start_driver()
                print(f"[RECOVERY] Reconnected on attempt {attempt}")
                time.sleep(5)
                return True
            except Exception as e:
                print(f"[RECOVERY] Attempt {attempt} failed: {e}")
                time.sleep(2)

        print("[RECOVERY] All reconnection attempts failed")
        return False
