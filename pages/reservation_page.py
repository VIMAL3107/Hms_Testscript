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
            return False
        except: return False

    @BasePage.auto_wait
    def enter_guest_name(self, name):
        print(f"[INFO] Entering guest name: {name}...")
        try:
            fields = self._get_guest_fields(min_count=3)
            field = fields[2] if len(fields) >= 3 else None
            if field:
                field.click(); time.sleep(0.5); field.clear(); field.send_keys(name)
                return True
            return False
        except: return False

    @BasePage.auto_wait
    def enter_email(self, email):
        print(f"[INFO] Entering email: {email}...")
        try:
            fields = self._get_guest_fields(min_count=4)
            field = fields[3] if len(fields) >= 4 else None
            if field:
                field.click(); time.sleep(0.5); field.clear(); field.send_keys(email)
                return True
            return False
        except: return False

    @BasePage.auto_wait
    def enter_address(self, address):
        print(f"[INFO] Entering address: {address}...")
        try:
            fields = self._get_guest_fields(min_count=5)
            field = fields[4] if len(fields) >= 5 else None
            if field:
                field.click(); time.sleep(0.5); field.clear(); field.send_keys(address)
                return True
            return False
        except: return False

    @BasePage.auto_wait
    def select_room_type(self, room_type):
        print(f"[INFO] Selecting room type: {room_type}...")
        try:
            dropdown = self.driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Select Room Type') or contains(@content-desc,'Select Room Type')]")
            dropdown.click()
            time.sleep(2)
            opt = self.driver.find_element(AppiumBy.XPATH, f"//*[contains(@content-desc,'{room_type}') or contains(@text,'{room_type}')]")
            opt.click()
            time.sleep(1)
            return True
        except: return False

    @BasePage.auto_wait
    def add_adults(self, count):
        print(f"[INFO] Adding {count} adults...")
        for _ in range(count):
            try:
                label = self.driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Adult') or contains(@content-desc,'Adult')]")
                y = label.rect['y'] + (label.rect['height']/2)
                btns = self.driver.find_elements(AppiumBy.XPATH, "//*[@text='+' or @content-desc='+']")
                for btn in btns:
                    if abs((btn.rect['y'] + btn.rect['height']/2) - y) < 60:
                        btn.click(); time.sleep(0.5); break
            except: pass
        return True

    @BasePage.auto_wait
    def add_children(self, count):
        print(f"[INFO] Adding {count} children...")
        for _ in range(count):
            try:
                label = self.driver.find_element(AppiumBy.XPATH, "//*[contains(@text,'Children') or contains(@content-desc,'Children')]")
                y = label.rect['y'] + (label.rect['height']/2)
                btns = self.driver.find_elements(AppiumBy.XPATH, "//*[@text='+' or @content-desc='+']")
                for btn in btns:
                    if abs((btn.rect['y'] + btn.rect['height']/2) - y) < 60:
                        btn.click(); time.sleep(0.5); break
            except: pass
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
        return False

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
        except: return False
