"""
Driver Manager — handles Appium WebDriver lifecycle.
Provides methods to create, quit, and recover the driver session.
"""

import time
import subprocess
import urllib.request
import sys
from appium import webdriver
from appium.options.android import UiAutomator2Options

from config.settings import CAPABILITIES, APPIUM_SERVER_URL


class DriverManager:
    """Manages the Appium WebDriver session lifecycle."""

    def __init__(self):
        self.driver = None

    def _pre_flight_checks(self):
        """Verify Appium server and connected devices before starting."""
        print("\n[PRE-FLIGHT] Running environment checks...")
        
        # 1. Check if an Android device/emulator is connected
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=False)
            lines = result.stdout.strip().split('\n')
            # 'lines' will have at least the header "List of devices attached". 
            # If there's a device, there will be more lines containing "device" or "emulator".
            if len(lines) <= 1 or not any("device" in line or "emulator" in line for line in lines[1:]):
                print("❌ [ERROR] No Android phone or emulator connected!")
                print("Please plug in your phone or start an Android Emulator.")
                sys.exit(1)
            else:
                print("[PRE-FLIGHT] ✅ Android device detected.")
        except FileNotFoundError:
            print("❌ [ERROR] 'adb' command not found!")
            print("Please run setup.bat to ensure Android SDK is installed and in your PATH.")
            sys.exit(1)

        # 2. Check if Appium Server is running, start it if not
        try:
            status_url = f"{APPIUM_SERVER_URL}/status"
            urllib.request.urlopen(status_url, timeout=2)
            print("[PRE-FLIGHT] ✅ Appium Server is already running.")
        except Exception:
            print("⚠️ [PRE-FLIGHT] Appium Server is down. Starting it automatically in the background...")
            try:
                # Start Appium silently in the background
                subprocess.Popen("appium", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("[PRE-FLIGHT] Booting Appium... please wait 5 seconds...")
                time.sleep(5)
                # Verify it started successfully
                urllib.request.urlopen(status_url, timeout=2)
                print("[PRE-FLIGHT] ✅ Appium Server started successfully!")
            except Exception as e:
                print(f"❌ [ERROR] Failed to auto-start Appium Server: {e}")
                print("Please try starting Appium manually by typing 'appium' in your terminal.")
                sys.exit(1)
        print("[PRE-FLIGHT] Checks passed!\n")

    def start_driver(self):
        """Create a new Appium driver session and ensure the app is in foreground."""
        self._pre_flight_checks()
        
        print("[DRIVER] Starting new Appium session...")
        options = UiAutomator2Options().load_capabilities(CAPABILITIES)
        self.driver = webdriver.Remote(
            command_executor=APPIUM_SERVER_URL,
            options=options,
        )
        
        # Explicitly ensure the app is launched and in foreground
        package = CAPABILITIES.get("appPackage")
        if package:
            print(f"[DRIVER] Ensuring app {package} is active...")
            try:
                self.driver.activate_app(package)
                time.sleep(2)  # Wait for transition
            except Exception as e:
                print(f"[DRIVER] Warning: Could not activate app explicitly: {e}")

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
