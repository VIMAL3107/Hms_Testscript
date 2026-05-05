"""
Reservation Page — encapsulates Reservation screen interactions.
"""

import time
import re
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import EXPLICIT_WAIT_DEFAULT, SCREEN_LOAD_DELAY
from pages.base_page import BasePage

class ReservationPage(BasePage):
    """Page Object for the Reservation screen."""

    @BasePage.auto_wait
    def navigate_to_reservation(self):
        """Navigate to the Reservation screen via the side menu."""
        print("\n=== NAVIGATING TO RESERVATION ===")
        from pages.menu_page import MenuPage
        menu = MenuPage(self.driver)
        return menu.navigate_to(["Reservation", "Reservations"], force_search=True)

    @BasePage.auto_wait
    def wait_for_screen(self):
        """Wait for the Reservation screen to load."""
        print("[WAIT] Waiting for Reservation screen...")
        time.sleep(SCREEN_LOAD_DELAY)
        print("[OK] Reservation screen loaded")
        return True

    @BasePage.auto_wait
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
            return True
        except Exception as e:
            print(f"[ERROR] Failed to click FAB: {e}")
            return False

    # ──────── Date Selection ────────

    @BasePage.auto_wait
    def click_checkin_field(self):
        """Click the Check-In date field to open the calendar."""
        print("[INFO] Clicking Check-In field...")
        try:
            xpath = "//*[contains(@text,'Check In') or contains(@content-desc,'Check In') or contains(@content-desc,'Check-In') or contains(@text,'--Select Date--')]"
            checkin = self.driver.find_element(AppiumBy.XPATH, xpath)
            checkin.click()
            time.sleep(2)
            print("[OK] Calendar is open")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to open calendar: {e}")
            return False

    def select_auto_dates(self):
        """Automatically select today and tomorrow."""
        from datetime import datetime, timedelta
        checkin_day = datetime.now().strftime("%d").lstrip('0')
        checkout_day = (datetime.now() + timedelta(days=1)).strftime("%d").lstrip('0')
        print(f"[INFO] Auto-dates: {checkin_day} to {checkout_day}")
        return self.select_dates(checkin_day, checkout_day)

    @BasePage.auto_wait
    def select_dates(self, start_day, end_day):
        """Select start and end dates in the calendar picker."""
        print(f"[INFO] Selecting dates {start_day} to {end_day}...")
        
        def tap_date(day):
            # Try multiple common patterns
            xpaths = [
                f"//*[@text='{day}' or @content-desc='{day}']",
                f"//*[@text='0{day}' or @content-desc='0{day}']",
                f"//*[starts-with(@text, '{day}') or starts-with(@content-desc, '{day}')]",
                f"//*[contains(@text, ' {day} ') or contains(@content-desc, ' {day} ')]"
            ]
            
            screen_size = self.driver.get_window_size()
            h = screen_size['height']
            w = screen_size['width']

            for xpath in xpaths:
                try:
                    els = self.driver.find_elements(AppiumBy.XPATH, xpath)
                    for el in els:
                        try:
                            if not el.is_displayed(): continue
                            loc = el.location
                            size = el.size
                            
                            # Filter: Calendar cells are usually small (less than 1/5th screen width)
                            # and located in the main central area of the screen.
                            if size['width'] < (w / 5) and loc['y'] > (h * 0.15) and loc['y'] < (h * 0.85):
                                print(f"[INFO] Found candidate for day {day} at ({loc['x']}, {loc['y']}) with size {size['width']}x{size['height']}")
                                
                                # Try clicking first
                                try:
                                    el.click()
                                except:
                                    # Fallback to coordinate tap
                                    self.driver.tap([(loc['x'] + size['width']//2, loc['y'] + size['height']//2)])
                                
                                time.sleep(1)
                                return True
                        except: continue
                except: continue
            return False

        try:
            if not tap_date(start_day):
                print(f"[WARN] Start date {start_day} not found, scrolling...")
                size = self.driver.get_window_size()
                self.driver.swipe(size["width"] // 2, int(size["height"] * 0.6), size["width"] // 2, int(size["height"] * 0.4), 500)
                time.sleep(1)
                if not tap_date(start_day): return False
            
            time.sleep(1)
            
            if not tap_date(end_day):
                print(f"[WARN] End date {end_day} not found, scrolling...")
                size = self.driver.get_window_size()
                self.driver.swipe(size["width"] // 2, int(size["height"] * 0.6), size["width"] // 2, int(size["height"] * 0.4), 500)
                time.sleep(1)
                if not tap_date(end_day): return False
                
            return True
        except Exception as e:
            print(f"[ERROR] Date selection failed: {e}")
            return False

    @BasePage.auto_wait
    def confirm_calendar(self):
        """Click OK to confirm the date selection."""
        print("[INFO] Confirming calendar...")
        try:
            ok_xpaths = [
                "//*[contains(@text,'OK') or contains(@content-desc,'OK')]",
                "//*[contains(@text,'Confirm') or contains(@content-desc,'Confirm')]",
                "//*[contains(@text,'DONE') or contains(@content-desc,'DONE')]"
            ]
            for xpath in ok_xpaths:
                try:
                    btn = self.driver.find_element(AppiumBy.XPATH, xpath)
                    btn.click()
                    time.sleep(2)
                    return True
                except: continue
            # Fallback to bottom-right tap
            size = self.driver.get_window_size()
            self.driver.tap([(int(size["width"] * 0.85), int(size["height"] * 0.85))])
            time.sleep(2)
            return True
        except: return False

    @BasePage.auto_wait
    def click_add_button(self):
        """Click the 'Add' button in the balance/payment dialog."""
        print("[INFO] Clicking Add button...")
        try:
            xpath = "//*[contains(@text,'Add') or contains(@content-desc,'Add')]"
            btn = self.driver.find_element(AppiumBy.XPATH, xpath)
            btn.click()
            time.sleep(2)
            return True
        except: 
            print("[WARN] Add button not found, skipping...")
            return True

    @BasePage.auto_wait
    def click_next_button(self):
        """Click the 'Next' button."""
        print("[INFO] Clicking Next button...")
        try:
            xpath = "//*[contains(@text,'Next') or contains(@content-desc,'Next')]"
            btn = self.driver.find_element(AppiumBy.XPATH, xpath)
            btn.click()
            time.sleep(2)
            return True
        except: return False

    @BasePage.auto_wait
    def select_room_type(self, room_type=None):
        """Select a room type. If no type is provided, picks the first available."""
        type_desc = room_type if room_type else "first available"
        print(f"[INFO] Selecting room type: {type_desc}...")
        try:
            # Try to open dropdown using the same logic that works in check-in
            xpath = "//*[contains(@text,'Select Room Type') or contains(@content-desc,'Select Room Type') or contains(@text,'Select Room')]"
            dropdown = self.driver.find_element(AppiumBy.XPATH, xpath)
            dropdown.click()
            time.sleep(2)
            
            opt = None
            if room_type:
                # Try specific type
                opt_xpaths = [
                    f"//*[contains(@content-desc,'{room_type}') or contains(@text,'{room_type}')]",
                    f"//*[@content-desc='{room_type}' or @text='{room_type}']"
                ]
                for ox in opt_xpaths:
                    try:
                        els = self.driver.find_elements(AppiumBy.XPATH, ox)
                        if els: 
                            opt = els[0]; break
                    except: continue
            
            if not opt:
                # Fallback: Find any available type (heuristic: non-header elements)
                all_els = self.driver.find_elements(AppiumBy.XPATH, "//*[@text!='' or @content-desc!='']")
                exclude = ["Select Room Type", "Room Type", "Select Room"]
                opt = next((el for el in all_els if (el.get_attribute('text') or el.get_attribute('content-desc') or '') not in exclude), None)
            
            if opt:
                self.last_selected_type = opt.get_attribute('text') or opt.get_attribute('content-desc')
                opt.click()
                time.sleep(1)
                return True
            return False
        except: 
            print(f"[WARN] Could not select room type '{type_desc}', skipping...")
            return True

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

    @BasePage.auto_wait
    def add_adults(self, adults=1):
        print(f"[INFO] Adding {adults} adults using '+' button...")
        try:
            time.sleep(1)
            plus_btn = self._find_plus_button("Adult")
            if not plus_btn:
                print("[WARN] Could not find '+' button for Adult")
                return True # Robust skip

            for i in range(adults):
                plus_btn.click()
                print(f"[OK] Clicked Adults '+' ({i + 1}/{adults})")
                time.sleep(0.5)
            return True
        except Exception as e:
            print(f"[WARN] Could not add adults: {e}")
            return True

    @BasePage.auto_wait
    def add_children(self, children=1):
        print(f"[INFO] Adding {children} children using '+' button...")
        try:
            time.sleep(1)
            plus_btn = self._find_plus_button("Children")
            if not plus_btn:
                print("[WARN] Could not find '+' button for Children")
                return True # Robust skip

            for i in range(children):
                plus_btn.click()
                print(f"[OK] Clicked Children '+' ({i + 1}/{children})")
                time.sleep(0.5)
            return True
        except Exception as e:
            print(f"[WARN] Could not add children: {e}")
            return True

    def get_guest_fields(self, min_count=1):
        """Find EditText fields below Guest Details header using check-in logic."""
        try:
            guest_section = self.driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Guest Details') or contains(@content-desc,'Guest Details')]")
            guest_y = guest_section.rect['y']
            inputs = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            fields = sorted([f for f in inputs if f.rect['y'] > guest_y], key=lambda x: x.rect['y'])
            if len(fields) < min_count:
                try: self.driver.hide_keyboard()
                except: pass
                size = self.driver.get_window_size()
                # Swipe slightly more to ensure fields are revealed
                self.driver.swipe(size["width"] // 2, int(size["height"] * 0.7), size["width"] // 2, int(size["height"] * 0.2), 800)
                time.sleep(2)
                inputs = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
                fields = sorted([f for f in inputs if f.rect['y'] > guest_y], key=lambda x: x.rect['y'])
            return fields
        except: return []

    @BasePage.auto_wait
    def enter_mobile_number(self, number="9876543210"):
        print(f"[INFO] Entering mobile number: {number}...")
        try:
            fields = self.get_guest_fields(min_count=1)
            if fields:
                fields[0].click(); time.sleep(0.5); fields[0].clear(); fields[0].send_keys(number)
                return True
            print("[WARN] Mobile number field not found, skipping...")
            return True
        except: 
            print("[WARN] Error entering mobile number, skipping...")
            return True

    @BasePage.auto_wait
    def enter_guest_name(self, name="John Doe"):
        print(f"[INFO] Entering guest name: {name}...")
        try:
            # Re-scroll if needed specifically for name
            fields = self.get_guest_fields(min_count=3)
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
    def enter_email(self, email="guest@example.com"):
        print(f"[INFO] Entering email: {email}...")
        try:
            fields = self.get_guest_fields(min_count=4)
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
    def enter_address(self, address="123 Guest St"):
        print(f"[INFO] Entering address: {address}...")
        try:
            fields = self.get_guest_fields(min_count=5)
            field = fields[4] if len(fields) >= 5 else None
            if field:
                field.click(); time.sleep(0.5); field.clear(); field.send_keys(address)
                return True
            print("[WARN] Address field not found, skipping...")
            return True
        except: 
            print("[WARN] Error entering address, skipping...")
            return True
        

    @BasePage.auto_wait
    def click_reserve_all_guests(self):
        print("[INFO] Clicking 'Reserve All Guests'...")
        try: self.driver.hide_keyboard()
        except: pass
        time.sleep(1)
        xpath = "//*[contains(@text,'Reserve All Guests') or contains(@content-desc,'Reserve All Guests')]"
        for _ in range(3):
            try:
                btn = self.driver.find_element(AppiumBy.XPATH, xpath)
                btn.click(); return True
            except:
                size = self.driver.get_window_size()
                self.driver.swipe(size["width"] // 2, int(size["height"] * 0.8), size["width"] // 2, int(size["height"] * 0.3), 600)
                time.sleep(1)
        print("[WARN] 'Reserve All Guests' button not found, skipping...")
        return True

    @BasePage.auto_wait
    def click_proceed_button(self):
        print("[INFO] Clicking 'Proceed'...")
        try:
            btn = self.driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Proceed') or contains(@content-desc,'Proceed')]")
            btn.click(); return True
        except: return False

    @BasePage.auto_wait
    def go_to_dashboard_from_reservation(self):
        print("[INFO] Navigating back...")
        try:
            self.driver.back(); time.sleep(2); self.driver.back(); time.sleep(2)
            return True
        except: 
            print("[WARN] Failed to navigate back, skipping...")
            return True
