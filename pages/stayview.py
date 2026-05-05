import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config.settings import EXPLICIT_WAIT_SHORT, EXPLICIT_WAIT_DEFAULT, MENU_LOAD_DELAY
from pages.menu_page import MenuPage
from pages.base_page import BasePage


class stayview_page(BasePage):


    # ──────────────────────────────────────────────
    #  NAVIGATION
    # ──────────────────────────────────────────────

    def navigate_to_stayview(self):
        """Navigate to Stay View using the MenuPage."""
        print("[INFO] Navigating to Stay View...")
        menu = MenuPage(self.driver)
        return menu.navigate_to("Stay View")

    # ──────────────────────────────────────────────
    #  ROOM SCANNING & SELECTION
    # ──────────────────────────────────────────────

    def wait_for_screen(self):
        """Wait until the Stay View grid is visible."""
        print("[WAIT] Waiting for Stay View screen...")
        try:
            self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[contains(@text,'Stay View') or contains(@content-desc,'Stay View')]",
                )
            )
            print("[OK] Stay View loaded")
            return True
        except TimeoutException:
            print("[ERROR] Stay View did not load")
            self._debug_dump_screen()
            return False

    def select_first_occupied_room(self):
        """
        Scroll through Stay View and open the first occupied room
        (room that has a guest name instead of 'Ready for Booking').
        """

        print("[INFO] Searching for occupied room...")

        for scroll_attempt in range(10):

            room_cards = self.driver.find_elements(
                AppiumBy.XPATH,
                "//*[contains(@content-desc, '\n') or contains(@text, '\n')]"
            )

            for card in room_cards:
                try:
                    desc = card.get_attribute("content-desc") or card.get_attribute("text") or ""

                    parts = [p.strip() for p in desc.split("\n") if p.strip()]

                    if len(parts) < 3:
                        continue

                    room_number = parts[0]
                    guest_name = parts[-1]

                    # Skip empty rooms
                    if guest_name in ["Ready for Booking", "Dirty Room"]:
                        continue

                    print(f"[OK] Found occupied room {room_number} - Guest {guest_name}")

                    card.click()
                    time.sleep(2)

                    return True

                except Exception:
                    continue

            print("[INFO] No occupied room visible, scrolling...")

            size = self.driver.get_window_size()
            self.driver.swipe(
                size['width'] / 2,
                size['height'] * 0.75,
                size['width'] / 2,
                size['height'] * 0.30,
                1000
            )

            time.sleep(0.5) # Reduced from 2.0

        print("[ERROR] No occupied room found after scrolling")
        return False
    
    def Schedule_Cleaning(self):
        """Schedule a cleaning for the current room."""
        try:
            print("[INFO] Opening Schedule Cleaning popup")
            # Loop to find the button with scrolling
            button = None
            for attempt in range(5):
                # Use find_elements to avoid implicit wait hits
                buttons = self.driver.find_elements(AppiumBy.ACCESSIBILITY_ID, "Schedule Cleaning")
                if not buttons:
                    buttons = self.driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc,'Schedule Cleaning') or contains(@text,'Schedule Cleaning')]")
                
                if buttons:
                    button = buttons[0]
                    print(f"[OK] Found Schedule Cleaning button (Attempt {attempt + 1})")
                    break
                
                if attempt < 4:
                    print(f"[INFO] Button not found, scrolling down (Attempt {attempt + 1})...")
                    self.scroll_down()
                    time.sleep(0.5) # Reduced from 1.5

            if not button:
                print("[ERROR] Schedule Cleaning button not found after scrolling")
                self._debug_dump_screen()
                return False

            button.click()
            time.sleep(2)

            # STEP 1 — Open calendar
            print("[INFO] Opening cleaning date picker")
            date_field = self.driver.find_element(
                AppiumBy.XPATH,
                "//android.view.View[contains(@text,'202')]"
            )
            date_field.click()
            time.sleep(2)

            # reuse your calendar functions
            self.select_next_day()
            self.confirm_date_picker()

            # STEP 2 — Special Instructions
            print("[INFO] Entering Special Instructions")
            try:
                instruction_box = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, "//android.view.View[@content-desc='Special Instructions']/following-sibling::android.widget.EditText"))
                )
                instruction_box.click() # Tap to focus
                time.sleep(1)
                instruction_box.send_keys("Room requires deep cleaning")
                print("[OK] Special Instructions entered")
            except Exception as e:
                print(f"[WARN] Special Instructions entry failed: {e}")

            # STEP 3 — Select Reported By
            print("[INFO] Selecting Reported By")
            try:
                reported_dropdown = self.driver.find_element(
                    AppiumBy.XPATH,
                    "//android.view.View[@content-desc='Reported By']/following-sibling::android.widget.Button"
                )
                reported_dropdown.click()
                time.sleep(2)
                
                # The dropdown is now open, click the first available person or a specific one
                # The debug dump showed names like 'Saravanan', 'James', etc.
                try:
                    option = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((AppiumBy.XPATH, "//*[contains(@content-desc,'Saravanan') or contains(@content-desc,'James')]"))
                    )
                    option.click()
                    print("[OK] Reported By selected")
                except:
                    print("[WARN] Could not find specific user, closing dropdown...")
                    self.driver.tap([(500, 500)]) # Tap outside to close if possible
            except Exception as e:
                print(f"[WARN] Reported By interaction failed: {e}")

            time.sleep(1)

            # STEP 4 — Scroll and Add
            print("[INFO] Scrolling to find 'Confirm' button")
            self.scroll_down()
            time.sleep(1)

            print("[INFO] Clicking Add button")
            add_button = None
            try:
                add_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Confirm"))
                )
            except:
                add_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, "//*[@content-desc='Confirm']"))
                )
            
            add_button.click()
            print("[OK] Schedule Cleaning completed")
            time.sleep(2)
            return True

        except Exception as e:
            print(f"[ERROR] Schedule Cleaning failed: {e}")
            self._debug_dump_screen()
            return False

    def add_charge(self, category="Restaurant service",
                   service="Room Services",
                   quantity="1",
                   amount="600"):
        """Add a service charge to the current room."""
        try:
            print("[INFO] Opening Add Charge popup")
            button = None
            # ───── FIND ADD CHARGE BUTTON WITH SCROLL ─────
            # Optimization: Use find_elements to avoid implicit wait delay
            for attempt in range(5):
                buttons = self.driver.find_elements(AppiumBy.ACCESSIBILITY_ID, "Add Charge")
                if not buttons:
                    buttons = self.driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc,'Add Charge') or contains(@text,'Add Charge')]")
                
                if buttons:
                    button = buttons[0]
                    print(f"[OK] Found Add Charge button (Attempt {attempt + 1})")
                    break

                # Scroll down to find the button (it's usually below the fold)
                print(f"[INFO] Button not found, scrolling down (Attempt {attempt + 1})...")
                self.scroll_down()
                time.sleep(0.5)

            if not button:
                print("[ERROR] Add Charge button not found")
                self._debug_dump_screen()
                return False

            button.click()
            time.sleep(2)

            # ───────── CATEGORY ─────────
            print("[INFO] Selecting category")
            category_dropdown = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "Select category...")
                )
            )
            category_dropdown.click()

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, category)
                )
            ).click()

            print(f"[OK] Category selected: {category}")
            time.sleep(1)

            # Close category popup if it stays open
            print("[INFO] Closing category popup if open")
            try:
                dismiss = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Dismiss")
                dismiss.click()
                print("[OK] Category popup closed")
                time.sleep(1)
            except:
                pass

            # ───────── SERVICE ─────────
            print("[INFO] Selecting service")
            try:
                # Check if the service option is ALREADY visible (sometimes opens automatically)
                try:
                    option = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, service)
                    print(f"[INFO] Service '{service}' already visible, clicking directly")
                except:
                    # Not visible, click the dropdown button
                    print("[INFO] Clicking service dropdown button")
                    service_dropdown = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((
                            AppiumBy.XPATH,
                            "//*[contains(@content-desc,'service') or contains(@text,'Service')]"
                        ))
                    )
                    service_dropdown.click()
                    time.sleep(2)
                    
                    option = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, service))
                    )

                option.click()
                print(f"[OK] Service selected: {service}")
            except Exception as e:
                print(f"[ERROR] Service selection failed: {e}")
                self._debug_dump_screen()
                raise

            # ───────── QUANTITY ─────────
            print("[INFO] Entering quantity")
            qty_xpaths = [
                "//android.view.View[contains(@content-desc,'Quantity') or contains(@text,'Quantity')]/following-sibling::android.widget.EditText",
                "//android.widget.EditText[1]" # Fallback
            ]
            qty = None
            for xpath in qty_xpaths:
                try:
                    qty = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((AppiumBy.XPATH, xpath))
                    )
                    if qty: break
                except: continue
            
            if qty:
                qty.click()
                qty.clear()
                qty.send_keys(quantity)
                print("[OK] Quantity entered")
            else:
                print("[WARN] Quantity field not found")

            # ───────── AMOUNT ─────────
            print("[INFO] Entering amount")
            amt_xpaths = [
                "//android.view.View[contains(@content-desc,'Amount') or contains(@text,'Amount')]/following-sibling::android.widget.EditText",
                "(//android.widget.EditText)[2]" # Fallback
            ]
            amt = None
            for xpath in amt_xpaths:
                try:
                    amt = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((AppiumBy.XPATH, xpath))
                    )
                    if amt: break
                except: continue

            if amt:
                amt.click()
                amt.clear()
                amt.send_keys(amount)
                print("[OK] Amount entered")
            else:
                print("[WARN] Amount field not found")

            # ───────── CONFIRM ─────────
            print("[INFO] Confirming charge")
            confirm_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "Confirm")
                )
            )
            confirm_btn.click()
            print("[OK] Charge added successfully")
            time.sleep(2)
            return True

        except Exception as e:
            print(f"[ERROR] Add Charge failed: {e}")
            self._debug_dump_screen()
            return False
    # ──────────────────────────────────────────────
    #  MODIFY STAY — MAIN ENTRY
    # ──────────────────────────────────────────────

    def click_modify_stay(self):

        """Tap the 'Modify Stay' button on the Room Detail screen."""
        print("[INFO] Clicking Modify Stay...")
        xpaths = [
            "//*[@text='Modify Stay' or @content-desc='Modify Stay']",
            "//*[contains(@text,'Modify Stay') or contains(@content-desc,'Modify Stay')]",
        ]
        if self._tap_first_found(xpaths, label="Modify Stay button"):
            time.sleep(2)
            return True
        return False

    def wait_for_modify_stay_dialog(self):
        """Wait for the Modify Stay dialog/bottom-sheet to be fully settled."""
        print("[WAIT] Waiting for Modify Stay dialog...")
        try:
            self.wait.until(
                lambda d: d.find_element(
                    AppiumBy.XPATH,
                    "//*[@text='Room No.' or @content-desc='Room No.' "
                    "or @text='Check-Out Date' or @content-desc='Check-Out Date']"
                )
            )
            print("[OK] Modify Stay dialog opened")
            # FIX: increased sleep so dialog fully settles before any interaction
            time.sleep(2)
            return True
        except TimeoutException:
            print("[ERROR] Modify Stay dialog did not appear")
            self._debug_dump_screen()
            return False

    def tap_checkout_date_field(self):
        """Open the Check-Out Date calendar picker."""
        print("[INFO] Opening Check-Out calendar...")
        try:
            date_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((
                    AppiumBy.XPATH,
                    "//android.view.View[contains(@text,'2026') or contains(@text,'AM') or contains(@text,'PM')]"
                ))
            )

            current_date = date_field.get_attribute("text")
            print(f"[INFO] Current checkout date: {current_date}")

            date_field.click()
            time.sleep(2)

            print("[OK] Calendar opened")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to open calendar: {e}")
            return False

    def select_next_day(self):
        """Select next day in calendar picker."""
        print("[INFO] Selecting next day...")
        try:
            today_btn = self.driver.find_element(
                AppiumBy.XPATH,
                "//android.widget.Button[contains(@content-desc,'Today')]"
            )

            desc = today_btn.get_attribute("content-desc")

            # Example: "4, Monday, May 4, 2026, Today"
            today_day = int(desc.split(",")[0])
            next_day = today_day + 1

            print(f"[INFO] Today: {today_day} → Selecting {next_day}")

            next_day_xpath = f"//android.widget.Button[starts-with(@content-desc,'{next_day},')]"
            next_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, next_day_xpath))
            )

            next_btn.click()
            print(f"[OK] Selected next day: {next_day}")
            return True

        except Exception as e:
            print(f"[ERROR] Next day selection failed: {e}")
            return False

    def confirm_date_picker(self):
        """Tap OK button in calendar picker."""
        print("[INFO] Confirming date picker...")

        # Try ACCESSIBILITY_ID first (Flutter uses this)
        try:
            ok_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "OK")
                )
            )
            ok_btn.click()
            print("[OK] Date confirmed (ACCESSIBILITY_ID)")
            time.sleep(2)
            return True
        except Exception:
            pass

        # Fallback: XPath with text or content-desc
        ok_xpaths = [
            "//*[@text='OK']",
            "//*[@content-desc='OK']",
            "//*[contains(@text,'OK')]",
            "//*[contains(@content-desc,'OK')]",
        ]
        for xpath in ok_xpaths:
            try:
                ok_btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, xpath))
                )
                ok_btn.click()
                print(f"[OK] Date confirmed (XPath)")
                time.sleep(2)
                return True
            except Exception:
                continue

        print("[ERROR] Confirm date picker failed - OK button not found")
        self._debug_dump_screen()
        return False

    def click_date_button(self):
        """Click the date button in Stay View and handle selection (Today's date)."""
        print("[INFO] Clicking date button...")
        try:
            # 🔷 STEP 1 — Open the date picker
            date_btn = None
            date_xpaths = [
                "//*[contains(@content-desc, '202')]",
                "//*[contains(@text, '202')]",
            ]
           
            for xpath in date_xpaths:
                try:
                    date_btn = self.driver.find_element(AppiumBy.XPATH, xpath)
                    if date_btn: break
                except: continue
           
            if not date_btn:
                print("[FALLBACK] Date button not found, tapping top toolbar...")
                self.driver.tap([(300, 150)])
            else:
                date_btn.click()
                print("[OK] Date button clicked")
           
            time.sleep(2)
 
            # 🔷 STEP 2 — Select TODAY'S DAY NUMBER
            from datetime import datetime
            today_day = datetime.now().strftime("%d").lstrip('0')
            print(f"[INFO] Selecting today's date: {today_day}...")
           
            # Try to find and click the day number
            try:
                # Optimized XPath for day selection
                day_xpath = f"//*[@text='{today_day}' or @content-desc='{today_day}']"
                days = self.driver.find_elements(AppiumBy.XPATH, day_xpath)
                if days:
                    # Usually the last one is the one in the current month view
                    days[-1].click()
                    print(f"[OK] Selected day: {today_day}")
                else:
                    print(f"[WARN] Day '{today_day}' not found in calendar")
                time.sleep(1)
            except Exception as e:
                print(f"[WARN] Could not select day: {e}")
 
            # 🔷 STEP 3 — Click OK
            print("[INFO] Confirming date...")
            try:
                ok_btn = self.driver.find_element(
                    AppiumBy.XPATH,
                    "//*[contains(@text,'OK') or contains(@content-desc,'OK')]"
                )
                ok_btn.click()
                print("[OK] Date confirmed")
                time.sleep(2)
            except Exception as e:
                print(f"[WARN] 'OK' button not found: {e}")
 
        except Exception as e:
            print(f"[ERROR] Date selection flow failed: {e}")
    
    def confirm_time_picker(self):
        """Keep existing time and tap OK."""
        print("[INFO] Confirming time picker...")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (AppiumBy.ACCESSIBILITY_ID, "Select time")
                )
            )
            time.sleep(1)
        except Exception:
            print("[WARN] Time picker wait skipped")

        try:
            ok_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "OK")
                )
            )
            ok_btn.click()
            print("[OK] Time picker confirmed")
            time.sleep(2)
            return True

        except Exception as e:
            print(f"[ERROR] Could not confirm time picker: {e}")
            return False


    # ──────────────────────────────────────────────
    #  MODIFY STAY — OTHER FIELDS
    # ──────────────────────────────────────────────

    def update_adults_in_modify(self, count):
        print(f"[INFO] Setting adults to {count} in Modify Stay dialog...")
        return self._set_numeric_field(keywords=["Adults", "Adult"], value=str(count))

    def update_children_in_modify(self, count):
        print(f"[INFO] Setting children to {count} in Modify Stay dialog...")
        return self._set_numeric_field(keywords=["Children", "Child"], value=str(count))

    def update_room_rate_in_modify(self, rate):
        print(f"[INFO] Setting room rate to {rate}...")
        return self._set_numeric_field(keywords=["Room Rate", "rate", "Rate"], value=str(rate))

    # ──────────────────────────────────────────────
    #  MODIFY STAY — REPORTED BY DROPDOWN
    # ──────────────────────────────────────────────

    def select_reported_by(self, user_name=None):
        """
        Select Reported By user.
        """

        print("[INFO] Selecting Reported By user...")

        try:

            dropdown_xpaths = [
                "//*[contains(@text,'Amala')]",
                "//*[contains(@text,'Reported By')]",
                "//android.widget.Spinner",
            ]

            opened = False

            for xpath in dropdown_xpaths:

                try:

                    elements = self.driver.find_elements(
                        AppiumBy.XPATH,
                        xpath
                    )

                    if elements:

                        elements[0].click()

                        opened = True

                        print("[OK] Reported By dropdown opened")

                        time.sleep(2)

                        break

                except Exception:
                    pass

            if not opened:
                print("[ERROR] Dropdown not opened")
                return False

            # Select specific user
            if user_name:

                user_xpath = (
                    f"//*[@text='{user_name}']"
                )

                try:

                    el = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((
                            AppiumBy.XPATH,
                            user_xpath
                        ))
                    )

                    el.click()

                    print(f"[OK] Selected user: {user_name}")

                    time.sleep(1)

                    return True

                except Exception:
                    print(f"[WARN] User {user_name} not found")

            # Select first available user
            users = self.driver.find_elements(
                AppiumBy.CLASS_NAME,
                "android.widget.TextView"
            )

            for user in users:

                txt = user.text.strip()

                if txt and txt not in [
                    "Modify Stay",
                    "Cancel",
                    "Confirm",
                    "Reported By"
                ]:

                    try:
                        user.click()

                        print(f"[OK] Selected first user: {txt}")

                        time.sleep(1)

                        return True

                    except Exception:
                        pass

        except Exception as e:

            print(f"[ERROR] Reported By failed: {e}")

        return False

    def get_available_reported_by_users(self) -> list:
        """
        After opening the Reported By dropdown, return the list of visible user names.
        Call this after the dropdown is open.
        """
        users = []
        try:
            items = self.driver.find_elements(
                AppiumBy.XPATH,
                "//*[string-length(@text) > 0 and string-length(@text) < 30 "
                "and not(contains(@text,'Modify')) "
                "and not(contains(@text,'Cancel')) "
                "and not(contains(@text,'Confirm')) "
                "and not(contains(@text,'Check')) "
                "and not(contains(@text,'Room')) "
                "and not(contains(@text,'Adults')) "
                "and not(contains(@text,'Children'))]"
            )
            for item in items:
                name = (item.get_attribute("text") or "").strip()
                if name and name not in users:
                    users.append(name)
        except Exception:
            pass
        print(f"[INFO] Available users: {users}")
        return users

    # ──────────────────────────────────────────────
    #  MODIFY STAY — CONFIRM / CANCEL
    # ──────────────────────────────────────────────

    def confirm_modify_stay(self):
        """Confirm Modify Stay."""
        print("[INFO] Clicking Confirm button...")

        # Try ACCESSIBILITY_ID first (Flutter)
        try:
            el = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (AppiumBy.ACCESSIBILITY_ID, "Confirm")
                )
            )
            el.click()
            print("[OK] Modify Stay confirmed (ACCESSIBILITY_ID)")
            time.sleep(3)
            return True
        except Exception:
            pass

        # Fallback: XPath with text or content-desc
        confirm_xpaths = [
            "//*[@text='Confirm']",
            "//*[@content-desc='Confirm']",
            "//*[contains(@text,'Confirm')]",
            "//*[contains(@content-desc,'Confirm')]",
        ]

        for xpath in confirm_xpaths:
            try:
                el = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, xpath))
                )
                el.click()
                print("[OK] Modify Stay confirmed (XPath)")
                time.sleep(3)
                return True
            except Exception:
                continue

        print("[ERROR] Confirm button not found")
        self._debug_dump_screen()
        return False

    # ──────────────────────────────────────────────
    #  HELPERS
    # ──────────────────────────────────────────────

    def _tap_first_found(self, xpaths: list, label: str = "element") -> bool:
        for xpath in xpaths:
            try:
                el = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, xpath))
                )
                el.click()
                print(f"[OK] Tapped: {label}")
                return True
            except Exception:
                continue
        print(f"[ERROR] Could not find: {label}")
        self._debug_dump_screen()
        return False

    def _set_numeric_field(self, keywords: list, value: str):
        """Find a numeric input field by its nearby text/hint and set its value."""
        for keyword in keywords:
            try:
                el = self.driver.find_element(
                    AppiumBy.XPATH,
                    f"//*[contains(@text,'{keyword}') or contains(@content-desc,'{keyword}')]"
                )
                
                # Check if element itself is EditText or find nearby
                target = el
                if "EditText" not in el.get_attribute("class"):
                    # Try to find EditText in the same container
                    try:
                        parent = el.find_element(AppiumBy.XPATH, "./..")
                        target = parent.find_element(AppiumBy.CLASS_NAME, "android.widget.EditText")
                    except:
                        pass
                
                target.click()
                time.sleep(0.5)
                target.clear()
                target.send_keys(value)
                try: self.driver.hide_keyboard()
                except: pass
                print(f"[OK] Set {keyword} to {value}")
                return True
            except Exception:
                continue
        return False

    def _debug_dump_screen(self):
        print("[DEBUG] Dumping visible screen elements...")
        try:
            els = self.driver.find_elements(AppiumBy.XPATH, "//*[@text!='' or @content-desc!='']")
            for el in els[:20]:
                t = (el.get_attribute("text") or "").strip()
                c = (el.get_attribute("content-desc") or "").strip()
                if t or c:
                    print(f"  → text={t!r}, desc={c[:50]!r}")
        except Exception as e:
            print(f"[DEBUG] Could not dump screen: {e}")

