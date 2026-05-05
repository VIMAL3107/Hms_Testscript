import time 
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config.settings import EXPLICIT_WAIT_SHORT, EXPLICIT_WAIT_DEFAULT, MENU_LOAD_DELAY
from pages.menu_page import MenuPage


from pages.base_page import BasePage

class checkin_page(BasePage):

    @BasePage.auto_wait
    def navigate_to_checkin(self):
        print("\n=== NAVIGATING TO CHECK-IN ===")
        menu = MenuPage(self.driver)
        return menu.navigate_to(["Check-In"], force_search=True)

    def wait_for_screen(self):
        print("[WAIT] Waiting for Check-In screen...")
        self.wait_for_loading()
        time.sleep(MENU_LOAD_DELAY)

        # Broaden search to multiple common variations seen in the UI
        header_xpaths = [    
            "//*[contains(@content-desc,'Checked-In')]",
        ]
        try:
            for xpath in header_xpaths:
                elements = self.driver.find_elements(AppiumBy.XPATH, xpath)
                if elements:
                    print(f"[OK] Check-In screen loaded (Found matching header: {xpath})")
                    return True
        except Exception:
            pass

        print("[ERROR] Check-In screen did not load")
        self._debug_dump_screen()
        return False

    # Removed auto_wait to prevent getting stuck on background loaders
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

    @BasePage.auto_wait
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
    
    @BasePage.auto_wait
    def add_payment(self):
        print("[INFO] Adding payment (Cash - 100)...")
        try:
            # open add payment popup
            self.driver.find_element(
                AppiumBy.ACCESSIBILITY_ID,
                "Add Payments"
            ).click()
            time.sleep(1)

            # enter amount
            amount_field = self.driver.find_element(
                AppiumBy.XPATH,
                "(//android.widget.EditText)[1]"
            )
            amount_field.click()
            amount_field.clear()
            amount_field.send_keys("100")
            time.sleep(0.5)

            # open payment method dropdown
            self.driver.find_element(
                AppiumBy.ACCESSIBILITY_ID,
                "Select Method"
            ).click()
            time.sleep(1)

            # choose cash
            self.driver.find_element(
                AppiumBy.ACCESSIBILITY_ID,
                "Cash"
            ).click()
            time.sleep(0.5)

            # record payment
            self.driver.find_element(
                AppiumBy.XPATH,
                "//android.widget.Button[@content-desc='Record Payment']"
            ).click()

            print("[OK] Payment recorded")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"[ERROR] Could not add payment: {e}")
            return False
    
    @BasePage.auto_wait
    def add_special_request(self, request_text="i want two room"):
        print(f"[INFO] Adding special request: {request_text}...")
        try:
            # Scroll down to find the button
            self.scroll_down()
            time.sleep(1)

            # Find and click "Add Special Request"
            special_req_btn = self.driver.find_element(
                AppiumBy.XPATH,
                "//android.view.View[@content-desc='Add Special Request']"
            )
            special_req_btn.click()
            time.sleep(1)

            # Enter text in the EditText
            text_field = self.driver.find_element(
                AppiumBy.XPATH,
                "//android.widget.EditText"
            )
            text_field.click()
            text_field.clear()
            text_field.send_keys(request_text)
            time.sleep(0.5)

            # Click "Accepted" button
            accepted_btn = self.driver.find_element(
                AppiumBy.XPATH,
                "//android.widget.Button[@content-desc='Accepted']"
            )
            accepted_btn.click()
            print("[OK] Special request added")
            time.sleep(2)
            return True
        except Exception as e:
            print(f"[ERROR] Could not add special request: {e}")
            self._debug_dump_screen()
            return False

    @BasePage.auto_wait
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

    def _get_guest_fields(self, min_count=1):
        """Find EditText fields below Guest Details header."""
        try:
            guest_section = self.driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Guest Details') or contains(@content-desc,'Guest Details')]")
            guest_y = guest_section.rect['y']
            inputs = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            fields = sorted([f for f in inputs if f.rect['y'] > guest_y], key=lambda x: x.rect['y'])
            if len(fields) < min_count:
                try: self.driver.hide_keyboard()
                except: pass
                size = self.driver.get_window_size()
                self.driver.swipe(size["width"] // 2, int(size["height"] * 0.6), size["width"] // 2, int(size["height"] * 0.2), 800)
                time.sleep(1.5)
                inputs = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
                fields = sorted([f for f in inputs if f.rect['y'] > guest_y], key=lambda x: x.rect['y'])
            return fields
        except: return []

    @BasePage.auto_wait
    def enter_mobile_number(self, number):
        print(f"[INFO] Entering mobile number: {number}...")
        try:
            fields = self._get_guest_fields(min_count=1)
            if fields:
                fields[0].click(); time.sleep(0.5); fields[0].clear(); fields[0].send_keys(number)
                return True
            print("[WARN] Mobile number field not found, skipping...")
            return True
        except: 
            print("[WARN] Error entering mobile number, skipping...")
            return True

    @BasePage.auto_wait
    def enter_guest_name(self, name):
        print(f"[INFO] Entering guest name: {name}...")
        try:
            fields = self._get_guest_fields(min_count=3)
            field = fields[2] if len(fields) >= 3 else None
            if field:
                field.click(); time.sleep(0.5); field.clear(); field.send_keys(name)
                return True
            print("[WARN] Guest name field not found, skipping...")
            return True
        except: 
            print("[WARN] Error entering guest name, skipping...")
            return True

    @BasePage.auto_wait
    def enter_email(self, email):
        print(f"[INFO] Entering email: {email}...")
        try:
            fields = self._get_guest_fields(min_count=4)
            field = fields[3] if len(fields) >= 4 else None
            if field:
                field.click(); time.sleep(0.5); field.clear(); field.send_keys(email)
                return True
            print("[WARN] Email field not found, skipping...")
            return True
        except: 
            print("[WARN] Error entering email, skipping...")
            return True

    @BasePage.auto_wait
    def enter_address(self, address):
        print(f"[INFO] Entering address: {address}...")
        try:
            fields = self._get_guest_fields(min_count=5)
            field = fields[4] if len(fields) >= 5 else None
            if field:
                field.click(); time.sleep(0.5); field.clear(); field.send_keys(address)
                return True
            print("[WARN] Address field not found, skipping...")
            return True
        except: 
            print("[WARN] Error entering address, skipping...")
            return True

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
        try:
            loc = element.location
            size = element.size
            tap_x = loc['x'] + size['width'] // 2
            tap_y = loc['y'] + int(size['height'] * 0.75)
            self.driver.tap([(tap_x, tap_y)])
            print(f"[OK] Tapped at ({tap_x}, {tap_y})")
        except Exception as e:
            print(f"[WARN] Failed to tap element bottom: {e}")


    @BasePage.auto_wait
    def select_room(self, room_number=None):
        """Select a room. If no room_number is provided, it tries to find one matching the selected room type."""
        room_desc = room_number if room_number else "any available"
        print(f"[INFO] Selecting room: {room_desc}...")
        try:
            xpath = "//*[contains(@text,'Select Room') or contains(@content-desc,'Select Room')]"
            dropdown = self.driver.find_element(AppiumBy.XPATH, xpath)
            dropdown.click()
            time.sleep(2)
            
            opt = None
            if room_number:
                opt = self.driver.find_element(AppiumBy.XPATH, f"//*[contains(@content-desc,'{room_number}') or contains(@text,'{room_number}')]")
            elif hasattr(self, 'last_selected_type'):
                # Try to find a room that matches the type (heuristic)
                type_xpath = f"//*[(contains(@content-desc,'{self.last_selected_type}') or contains(@text,'{self.last_selected_type}')) and not(contains(@class,'EditText'))]"
                candidates = self.driver.find_elements(AppiumBy.XPATH, type_xpath)
                if candidates:
                    opt = candidates[0]
            
            if not opt:
                # Fallback: Find any room-like element (heuristic: numeric text or first clickable item)
                all_els = self.driver.find_elements(AppiumBy.XPATH, "//*[@text!='' or @content-desc!='']")
                opt = next((el for el in all_els if any(c.isdigit() for c in (el.get_attribute('text') or el.get_attribute('content-desc') or ''))), None)
            
            if opt:
                opt.click()
                time.sleep(1)
                return True
            return False
        except: return False 
    def _find_plus_button(self, label):
        """Helper: find the '+' button near a given label (Adult/Children)."""
        plus_btn_xpaths = [
            f"//*[@text='{label}' or @content-desc='{label}']/following-sibling::*[@text='+' or @content-desc='+']",
            f"//*[contains(@text,'{label}') or contains(@content-desc,'{label}')]/following-sibling::*[contains(@text,'+') or contains(@content-desc,'+')]",
            f"//*[@text='{label}' or @content-desc='{label}']/parent::*//*[@text='+' or @content-desc='+']",
            f"//*[contains(@text,'{label}') or contains(@content-desc,'{label}')]/parent::*//*[@text='+' or @content-desc='+']",
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

    @BasePage.auto_wait
    def add_adults(self, adults=1):
        print(f"[INFO] Adding {adults} adults using '+' button...")
        try:
            time.sleep(1)
            plus_btn = self._find_plus_button("Adult")

            if not plus_btn:
                print("[WARN] Could not find '+' button for Adult, dumping screen...")
                return False

            for i in range(adults):
                plus_btn.click()
                print(f"[OK] Clicked Adults '+' ({i + 1}/{adults})")
                time.sleep(0.5)

            print(f"[OK] Added {adults} adults")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"[WARN] Could not add adults (skipping): {e}")
            return True

    @BasePage.auto_wait
    def add_children(self, children=1):
        print(f"[INFO] Adding {children} children using '+' button...")
        try:
            time.sleep(1)
            plus_btn = self._find_plus_button("Children")

            if not plus_btn:
                print("[WARN] Could not find '+' button for Children, dumping screen...")
                return False

            for i in range(children):
                plus_btn.click()
                print(f"[OK] Clicked Children '+' ({i + 1}/{children})")
                time.sleep(0.5)

            print(f"[OK] Added {children} children")
            time.sleep(1)
            return True
        except Exception as e:
            print(f"[WARN] Could not add children (skipping): {e}")
            return True

    @BasePage.auto_wait
    def add_parking_details(self, vehicle_number="TN01AB1234",
                            parking_location="Sunrise Parking 1",
                            vehicle_type="Bike"):

        try:
            # Scroll until Parking Details section is visible
            for _ in range(5):
                parking = self.driver.find_elements(
                    AppiumBy.ACCESSIBILITY_ID,
                    "Parking Details"
                )
                if parking:
                    print("[OK] Parking section visible")
                    break
                print("[INFO] Parking not visible, scrolling...")
                self.scroll_down()

            time.sleep(1)

            # Find Vehicle Number field
            vehicle_field = None
            vehicle_xpaths = [
                "//*[contains(@content-desc,'Vehicle Number')]/following::android.widget.EditText[1]",
                "//*[contains(@text,'Vehicle Number')]/following::android.widget.EditText[1]",
                "//*[contains(@content-desc,'Enter Number')]",
                "//*[contains(@content-desc,'--Enter Number--')]",
                "//*[contains(@content-desc,'Parking Details')]/following::android.widget.EditText[1]",
            ]

            for xpath in vehicle_xpaths:
                try:
                    vehicle_field = self.driver.find_element(AppiumBy.XPATH, xpath)
                    if vehicle_field:
                        print(f"[OK] Found vehicle field using: {xpath}")
                        break
                except Exception:
                    continue

            # Fallback: find EditText that appears below the Parking Details label
            if not vehicle_field:
                try:
                    parking_label = self.driver.find_elements(
                        AppiumBy.XPATH,
                        "//*[contains(@content-desc,'Parking Details') or contains(@text,'Parking Details')]"
                    )
                    if parking_label:
                        parking_y = parking_label[0].rect['y']
                        all_edits = self.driver.find_elements(
                            AppiumBy.CLASS_NAME, "android.widget.EditText"
                        )
                        # Get EditText fields below the Parking Details label
                        below_parking = [e for e in all_edits if e.rect['y'] > parking_y]
                        below_parking.sort(key=lambda e: e.rect['y'])
                        if below_parking:
                            vehicle_field = below_parking[0]
                            print("[OK] Found vehicle field by position (below Parking Details)")
                except Exception as ex:
                    print(f"[WARN] Fallback vehicle field search failed: {ex}")

            if vehicle_field:
                vehicle_field.click()
                time.sleep(0.5)
                vehicle_field.clear()
                vehicle_field.send_keys(vehicle_number)
                print(f"[OK] Entered vehicle number: {vehicle_number}")
                try:
                    self.driver.hide_keyboard()
                except Exception:
                    pass
                time.sleep(0.5)
            else:
                print("[WARN] Vehicle number field not found, dumping screen...")
                self._debug_dump_screen()

            # Select Parking Location dropdown (1st 'Select' button)
            if not self.select_dropdown(1, parking_location):
                print(f"[WARN] Could not select parking location: {parking_location}")

            # Select Vehicle Type dropdown
            # After selecting parking location, that dropdown no longer shows 'Select',
            # so Vehicle Type is now the 1st (not 2nd) 'Select' element
            if not self.select_dropdown(1, vehicle_type):
                print(f"[WARN] Could not select vehicle type: {vehicle_type}")

            print("[OK] Parking details added")
            return True

        except Exception as e:
            print(f"[ERROR] Parking failed: {e}")
            return False


    @BasePage.auto_wait
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
    
    @BasePage.auto_wait
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

    @BasePage.auto_wait
    def go_to_dashboard_from_checkin(self):
        """Exit the Check-In flow and return to the main dashboard."""
        print("[INFO] Navigating back to Dashboard from Check-In...")
        try:
            self.driver.back()
            time.sleep(3)
            # Dismiss any leftover success overlays
            try:
                from pages.menu_page import MenuPage
                menu = MenuPage(self.driver)
                menu.dismiss_overlay()
            except: pass
            return True
        except Exception as e:
            print(f"[ERROR] Failed to return to dashboard: {e}")
            return False
