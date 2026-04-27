import time 
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config.settings import EXPLICIT_WAIT_SHORT, EXPLICIT_WAIT_DEFAULT, MENU_LOAD_DELAY
from pages.menu_page import MenuPage


class checkin_page:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT_DEFAULT)

    def navigate_to_checkin(self):
        print("\n=== NAVIGATING TO CHECK-IN ===")
        menu = MenuPage(self.driver)
        result = menu.navigate_to("Check-In")
        time.sleep(2)
        return result

    def wait_for_screen(self):
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
        print("[INFO] Looking for a CheckedIn booking...")
        time.sleep(2)
        checkedin_xpath = (
            "//*[contains(@content-desc,'Reserved') or contains(@text,'Reserved')]")

        max_scrolls = 5
        checkedin = None
        for scroll in range(max_scrolls + 1):
            elements = self.driver.find_elements(AppiumBy.XPATH, checkedin_xpath)
            if elements:
                checkedin = elements[0]
                print(f"[OK] Found Reserved booking")
                break

            if scroll < max_scrolls:
                print(f"[INFO] Scrolling down to find Reserved... ({scroll + 1}/{max_scrolls})")
                size = self.driver.get_window_size()
                self.driver.swipe(
                    size["width"] // 2, int(size["height"] * 0.7),
                    size["width"] // 2, int(size["height"] * 0.3), 700
                )
                time.sleep(1.5)

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

        checkedin.click()
        print("[OK] Clicked booking")
        time.sleep(3)
        return True

    def wait_for_guest_detail(self):
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

    def click_checkin_field(self):
        print("[INFO] Clicking Check-In field...")
        try:
            checkin_field = self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[(@text='Check-In' or @content-desc='Check-In') "
                    "and not(contains(@class,'TextView'))]",
                )
            )
            checkin_field.click()
            print("[OK] Clicked Check-In field")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"[ERROR] Could not click Check-In field: {e}")
            return False

    def scroll_down(self):
        """Scroll down the screen."""
        try:
            size = self.driver.get_window_size()
            self.driver.swipe(
                size["width"] // 2, int(size["height"] * 0.7),
                size["width"] // 2, int(size["height"] * 0.3), 700
            )
            time.sleep(1)
        except Exception:
            pass

    def _tap_element_bottom(self, element):
        """Tap on the bottom part of an element (useful for Flutter combined label+dropdown)."""
        loc = element.location
        size = element.size
        # Tap at 50% width, 75% height of the element (the dropdown value area)
        tap_x = loc['x'] + size['width'] // 2
        tap_y = loc['y'] + int(size['height'] * 0.75)
        self.driver.tap([(tap_x, tap_y)])
        print(f"[OK] Tapped at ({tap_x}, {tap_y})")

    def select_room_type(self, room_type):
        print(f"[INFO] Selecting room type: {room_type}...")
        try:
            # Find the Room Type dropdown element (content-desc: 'Room Type\nStandard King')
            dropdown = None
            dropdown_xpaths = [
                "//*[contains(@content-desc,'Room Type')]",
                "//*[contains(@text,'Room Type')]",
            ]
            for xpath in dropdown_xpaths:
                try:
                    dropdown = self.driver.find_element(AppiumBy.XPATH, xpath)
                    if dropdown:
                        break
                except Exception:
                    continue
                time.sleep(0.3)

            if not dropdown:
                print("[ERROR] Room type dropdown not found")
                return False

            # Tap on the bottom half of the element (where 'Standard King ▼' is)
            self._tap_element_bottom(dropdown)
            print("[OK] Tapped room type dropdown area")
            time.sleep(3)

            # Now find the room type option in the bottom sheet
            room_type_xpaths = [
                f"//*[contains(@content-desc,'{room_type}')]",
                f"//*[contains(@text,'{room_type}')]",
            ]
            room_type_el = None
            for xpath in room_type_xpaths:
                try:
                    els = self.driver.find_elements(AppiumBy.XPATH, xpath)
                    # Pick the one that is NOT the dropdown itself (avoid re-clicking the label)
                    for el in els:
                        desc = el.get_attribute('content-desc') or ''
                        # Skip if it's the combined 'Room Type\n...' element
                        if 'Room Type' not in desc or desc.startswith(room_type):
                            room_type_el = el
                            break
                    if room_type_el:
                        break
                except Exception:
                    continue
                time.sleep(0.3)

            if room_type_el:
                room_type_el.click()
                print(f"[OK] Selected room type: {room_type}")
                time.sleep(2)
                return True
            else:
                print(f"[ERROR] Room type '{room_type}' not found in bottom sheet")
                self._debug_dump_screen(limit=40)
                return False
        except Exception as e:
            print(f"[ERROR] Could not select room type: {e}")
            return False

    def select_room(self, room_number):
        print(f"[INFO] Selecting room: {room_number}...")
        try:
            # Find the Room dropdown element (content-desc: 'Room\nSelect Room')
            dropdown = None
            dropdown_xpaths = [
                "//*[contains(@content-desc,'Select Room')]",
                "//*[contains(@text,'Select Room')]",
            ]
            for xpath in dropdown_xpaths:
                try:
                    dropdown = self.driver.find_element(AppiumBy.XPATH, xpath)
                    if dropdown:
                        break
                except Exception:
                    continue
                time.sleep(0.3)

            if not dropdown:
                print("[ERROR] Room dropdown not found")
                return False

            # Tap on the bottom half of the element (where 'Select Room ▼' is)
            self._tap_element_bottom(dropdown)
            print("[OK] Tapped room dropdown area")
            time.sleep(3)

            # Now find the room number in the bottom sheet
            room_xpaths = [
                f"//*[contains(@content-desc,'{room_number}')]",
                f"//*[contains(@text,'{room_number}')]",
            ]
            room_el = None
            for xpath in room_xpaths:
                try:
                    room_el = self.driver.find_element(AppiumBy.XPATH, xpath)
                    if room_el:
                        break
                except Exception:
                    continue
                time.sleep(0.3)

            if room_el:
                room_el.click()
                print(f"[OK] Selected room: {room_number}")
                time.sleep(2)
                return True
            else:
                print(f"[ERROR] Room '{room_number}' not found in bottom sheet")
                self._debug_dump_screen(limit=40)
                return False
        except Exception as e:
            print(f"[ERROR] Could not select room: {e}")
            return False

    def _find_plus_button(self, label):
        """Helper: find the '+' button near a given label (Adult/Children)."""
        plus_btn_xpaths = [
            f"//*[@text='{label}' or @content-desc='{label}']/following-sibling::*[@text='+' or @content-desc='+']",
            f"//*[contains(@text,'{label}') or contains(@content-desc,'{label}')]/following-sibling::*[contains(@text,'+') or contains(@content-desc,'+')]",
            f"//*[@text='{label}' or @content-desc='{label}']/parent::*//*[@text='+' or @content-desc='+']",
            f"//*[contains(@text,'{label}') or contains(@content-desc,'{label}')]/parent::*//*[@text='+' or @content-desc='+']" 
            f"//*[contains(@content-desc,'{label}')]/ancestor::*[2]//*[@text='+' or @content-desc='+']",
            f"//*[contains(@text,'{label}')]/ancestor::*[2]//*[@text='+' or @content-desc='+']",
        ]
        for xpath in plus_btn_xpaths:
            try:
                btn = self.driver.find_element(AppiumBy.XPATH, xpath)
                if btn:
                    print(f"[OK] Found '+' button for {label}")
                    return btn
            except Exception:
                pass
            time.sleep(0.3)
        return None

    def _debug_dump_screen(self, limit=25):
        """Dump visible elements on screen for debugging."""
        print("[DEBUG] === Screen elements ===")
        try:
            all_els = self.driver.find_elements(
                AppiumBy.XPATH, "//*[@text!='' or @content-desc!='']"
            )
            for el in all_els[:limit]:
                t = el.get_attribute('text') or ''
                c = el.get_attribute('content-desc') or ''
                if t or c:
                    print(f"  - Text: '{t}' | Desc: '{c[:80]}'")
        except Exception:
            print("[DEBUG] Could not dump screen elements")
        print("[DEBUG] === End ===")

    def _find_input_field(self, keywords, field_label="field"):
        """Helper: find an input field by trying multiple keywords in content-desc and text."""
        for keyword in keywords:
            xpaths = [
                f"//*[contains(@content-desc,'{keyword}')]",
                f"//*[contains(@text,'{keyword}')]",
                f"//*[@content-desc='{keyword}']",
                f"//*[@text='{keyword}']",
            ]
            for xpath in xpaths:
                try:
                    el = self.driver.find_element(AppiumBy.XPATH, xpath)
                    if el:
                        print(f"[OK] Found {field_label} field with keyword: '{keyword}'")
                        return el
                except Exception:
                    pass
                time.sleep(0.2)
        return None

    def add_adults(self, adults=1):
        print(f"[INFO] Adding {adults} adults using '+' button...")
        try:
            time.sleep(1)
            # App label is "Adult" (singular), try both
            plus_btn = self._find_plus_button("Adult")

            if not plus_btn:
                print("[WARN] Could not find '+' button for Adult, dumping screen...")
                self._debug_dump_screen()
                return False

            for i in range(adults):
                plus_btn.click()
                print(f"[OK] Clicked Adults '+' ({i + 1}/{adults})")
                time.sleep(0.5)

            print(f"[OK] Added {adults} adults")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"[ERROR] Could not add adults: {e}")
            return False

    def add_children(self, children=1):
        print(f"[INFO] Adding {children} children using '+' button...")
        try:
            time.sleep(1)
            plus_btn = self._find_plus_button("Children")

            if not plus_btn:
                print("[WARN] Could not find '+' button for Children, dumping screen...")
                self._debug_dump_screen()
                return False

            for i in range(children):
                plus_btn.click()
                print(f"[OK] Clicked Children '+' ({i + 1}/{children})")
                time.sleep(0.5)

            print(f"[OK] Added {children} children")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"[ERROR] Could not add children: {e}")
            return False

    def add_email(self, email="iamvimal3107@gmail.com"):
        """
        Find and fill the Email input field.
        On Flutter the field is typically an EditText / TextField.
        We try content-desc, text, class-based, and index-based lookups.
        """
        print(f"[INFO] Entering email: {email}...")
        time.sleep(1)

        # Scroll down a bit so the email field is visible
        self.scroll_down()
        time.sleep(1)

        field = self._find_input_field(
            keywords=["Email", "email", "E-mail"],
            field_label="Email"
        )
        if not field:
            print("[ERROR] Email field not found")
            self._debug_dump_screen()
            return False

        try:
            field.click()
            time.sleep(0.5)
            field.clear()
            field.send_keys(email)
            print(f"[OK] Entered email: {email}")
            # Dismiss keyboard
            self.driver.hide_keyboard()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"[ERROR] Could not type into email field: {e}")
            return False

    def add_address(self, address):
        """
        Find and fill the Address input field.
        """
        print(f"[INFO] Entering address: {address}...")
        time.sleep(1)

        self.scroll_down()
        time.sleep(1)

        field = self._find_input_field(
            keywords=["Address", "address"],
            field_label="Address"
        )
        if not field:
            print("[ERROR] Address field not found")
            self._debug_dump_screen()
            return False

        try:
            field.click()
            time.sleep(0.5)
            field.clear()
            field.send_keys(address)
            print(f"[OK] Entered address: {address}")
            self.driver.hide_keyboard()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"[ERROR] Could not type into address field: {e}")
            return False

    def click_update_checkin(self):
        print(f"[INFO] Clicking 'Update & Check-in' button...")
        try:
            # Scroll down to make sure button is visible
            self.scroll_down()
            time.sleep(1)

            # Try multiple text variations (screenshot shows 'Update & Check-in')
            btn_xpaths = [
                "//*[contains(@text,'Update') and contains(@text,'Check')]",
                "//*[contains(@content-desc,'Update') and contains(@content-desc,'Check')]",
                "//*[contains(@text,'Update & Check-in')]",
                "//*[contains(@content-desc,'Update & Check-in')]",
                "//*[contains(@text,'Update & Check-In')]",
                "//*[contains(@content-desc,'Update & Check-In')]",
            ]
            btn = None
            for xpath in btn_xpaths:
                try:
                    btn = self.driver.find_element(AppiumBy.XPATH, xpath)
                    if btn:
                        print(f"[OK] Found Update & Check-in button")
                        break
                except Exception:
                    continue
                time.sleep(0.3)

            if not btn:
                print("[ERROR] Update & Check-in button not found")
                self._debug_dump_screen()
                return False

            btn.click()
            print("[OK] Clicked Update & Check-in button")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"[ERROR] Could not click Update & Check-in button: {e}")
            return False
    def confirm_checkin(self):
        print(f"[INFO] Looking for Proceed/Confirm button...")
        try:
            proceed_xpaths = [
                "//*[contains(@text,'Proceed') or contains(@text,'proceed')]",
                "//*[contains(@content-desc,'Proceed') or contains(@content-desc,'proceed')]",
            ]
            
            # Wait up to a few seconds for it to appear
            btn = None
            for _ in range(10):  # Retry loop to wait for page load (up to 5s)
                for xpath in proceed_xpaths:
                    try:
                        btn = self.driver.find_element(AppiumBy.XPATH, xpath)
                        if btn:
                            break
                    except Exception:
                        pass
                if btn:
                    break
                time.sleep(0.5)

            if not btn:
                print(f"[ERROR] Could not find Proceed button")
                self._debug_dump_screen()
                return False

            btn.click()
            print("[OK] Clicked Proceed button")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"[ERROR] Could not click Proceed button: {e}")
            return False