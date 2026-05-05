
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pages.base_page import BasePage

# ── tunables ──────────────────────────────────────────────────────────────────
SHORT   = 5    # seconds — quick presence check
MEDIUM  = 10   # seconds — normal wait
LONG    = 15   # seconds — slow network / animation


class RoomTransferPage(BasePage):
    """Handles the Room Transfer (Room Move) flow from Stay View."""

    # ──────────────────────────────────────────────
    #  1. CLICK ROOM TRANSFER BUTTON
    # ──────────────────────────────────────────────

    def click_room_transfer(self):
        """Tap the 'Room Transfer' button on the Room Detail screen."""
        print("[INFO] Clicking Room Transfer...")

        # Try ACCESSIBILITY_ID first
        try:
            btn = WebDriverWait(self.driver, MEDIUM).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "Room Transfer")
                )
            )
            btn.click()
            print("[OK] Tapped Room Transfer (ACCESSIBILITY_ID)")
            time.sleep(2)
            return True
        except Exception:
            pass

        # Fallback: XPath
        xpaths = [
            "//*[@text='Room Transfer' or @content-desc='Room Transfer']",
            "//*[contains(@text,'Room Transfer') or contains(@content-desc,'Room Transfer')]",
        ]
        for xpath in xpaths:
            try:
                el = WebDriverWait(self.driver, SHORT).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, xpath))
                )
                el.click()
                print("[OK] Tapped Room Transfer (XPath)")
                time.sleep(2)
                return True
            except Exception:
                continue

        print("[ERROR] Room Transfer button not found")
        self._debug_dump_screen()
        return False

    # ──────────────────────────────────────────────
    #  2. WAIT FOR ROOM MOVE SCREEN
    # ──────────────────────────────────────────────

    def wait_for_room_move_screen(self):
        """Wait for the Room Move / Transfer screen to load."""
        print("[WAIT] Waiting for Room Move screen...")
        try:
            WebDriverWait(self.driver, MEDIUM).until(
                EC.presence_of_element_located((
                    AppiumBy.XPATH,
                    "//*[contains(@text,'Room Move') or contains(@content-desc,'Room Move') "
                    "or contains(@text,'Room Type') or contains(@content-desc,'Room Type')]"
                ))
            )
            print("[OK] Room Move screen loaded")
            time.sleep(1)
            return True
        except TimeoutException:
            print("[ERROR] Room Move screen did not load")
            self._debug_dump_screen()
            return False

    # ──────────────────────────────────────────────
    #  3. SELECT ROOM TYPE
    # ──────────────────────────────────────────────

    def select_room_type(self, room_type_name=None):
        """Click Room Type dropdown and select an option."""
        print(f"[INFO] Selecting Room Type: {room_type_name if room_type_name else 'first available'}")

        try:
            # Open dropdown
            room_dropdown = WebDriverWait(self.driver, MEDIUM).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "Room Type")
                )
            )
            room_dropdown.click()
            time.sleep(2)

            # Select specific type
            if room_type_name:
                option = WebDriverWait(self.driver, MEDIUM).until(
                    EC.element_to_be_clickable(
                        (AppiumBy.ACCESSIBILITY_ID, room_type_name)
                    )
                )
                option.click()
                print(f"[OK] Selected room type: {room_type_name}")
                return True

            # Select first available automatically
            else:
                options = self.driver.find_elements(
                    AppiumBy.XPATH,
                    "//android.widget.Button[@content-desc]"
                )
                for opt in options:
                    name = opt.get_attribute("content-desc")
                    if name and name != "Room Type":
                        opt.click()
                        print(f"[OK] Selected first available: {name}")
                        return True

        except Exception as e:
            print(f"[ERROR] Room type selection failed: {e}")

        return False

    # ──────────────────────────────────────────────
    #  4. SELECT AVAILABLE ROOM
    # ──────────────────────────────────────────────
    def select_available_room(self, room_number=None):
        print(f"[INFO] Selecting room: {room_number if room_number else 'first available'}")
        try:
            if room_number:
                el = WebDriverWait(self.driver, MEDIUM).until(
                    EC.element_to_be_clickable((
                        AppiumBy.XPATH,
                        f"//*[contains(@content-desc,'Room {room_number}')]"
                    ))
                )
                el.click()
                print(f"[OK] Selected room: {room_number}")
            else:
                # Wait for at least one available room to appear
                try:
                    WebDriverWait(self.driver, MEDIUM).until(
                        EC.presence_of_element_located((AppiumBy.XPATH, "//*[contains(@content-desc,'Available')]"))
                    )
                    rooms = self.driver.find_elements(
                        AppiumBy.XPATH,
                        "//*[contains(@content-desc,'Available')]"
                    )
                except TimeoutException:
                    print("[ERROR] No available rooms found after waiting")
                    self._debug_dump_screen()
                    return False

                room_desc = rooms[0].get_attribute("content-desc")
                room_name = room_desc.split("\n")[0]
                rooms[0].click()
                print(f"[OK] Selected {room_name}")

            time.sleep(1)
            # IMPORTANT PART
            self.scroll_to_reason()
            return True
        except Exception as e:
            print(f"[ERROR] Room selection failed: {e}")
            return False

    def scroll_to_reason(self):
        print("[INFO] Scrolling to Reason for Move...")
        for _ in range(5):
            reason = self.driver.find_elements(
                AppiumBy.ACCESSIBILITY_ID,
                "Select Reason"
            )
            if reason:
                print("[OK] Reason for Move visible")
                return True
            self.scroll_down()
            time.sleep(1)
        print("[WARN] Could not locate Reason for Move")
        return False
    # ──────────────────────────────────────────────
    #  5. SELECT REASON
    # ──────────────────────────────────────────────

    def select_reason_for_move(self, reason="Upgrade"):
        """Select transfer reason from dropdown."""
        print(f"[INFO] Selecting reason: {reason}")

        try:
            self.scroll_down()

            dropdown = WebDriverWait(self.driver, MEDIUM).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "Select Reason")
                )
            )
            dropdown.click()
            time.sleep(2)

            option = WebDriverWait(self.driver, MEDIUM).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, reason)
                )
            )
            option.click()

            print(f"[OK] Reason selected: {reason}")
            return True

        except Exception as e:
            print(f"[ERROR] Reason selection failed: {e}")
            return False

    # ──────────────────────────────────────────────
    #  6. SELECT BILLING OPTION
    # ──────────────────────────────────────────────

    def select_billing_option(self, keep_current=True):
        """Select billing option radio button."""
        keyword = "Keep current" if keep_current else "Update to"
        print(f"[INFO] Selecting billing option: '{keyword}'")

        try:
            el = WebDriverWait(self.driver, MEDIUM).until(
                EC.element_to_be_clickable((
                    AppiumBy.XPATH,
                    f'//*[contains(@text,"{keyword}") or contains(@content-desc,"{keyword}")]'
                ))
            )
            el.click()
            print(f"[OK] Billing option selected")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"[ERROR] Billing option selection failed: {e}")
            return False

    # ──────────────────────────────────────────────
    #  7. CONFIRM MOVE
    # ──────────────────────────────────────────────
    def click_confirm_move(self, timeout=MEDIUM):
        """Tap the 'Confirm Move' button and handle secondary Proceed popup."""
        print("[INFO] Clicking Confirm Move...")

        try:
            btn = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "Confirm Move")
                )
            )
            btn.click()
            print("[OK] Confirm Move clicked")
            time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Confirm Move not found: {e}")
            self._debug_dump_screen()
            return False

        # Handle secondary Proceed popup
        try:
            proceed = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((
                    AppiumBy.XPATH,
                    "//*[contains(@text,'Proceed') or contains(@content-desc,'Proceed')]"
                ))
            )
            proceed.click()
            print("[OK] Clicked Proceed")
            time.sleep(2)
        except Exception:
            print("[INFO] No Proceed popup appeared")

        return True