import unittest
import os
import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

android_sdk_path = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk")
os.environ["ANDROID_HOME"] = android_sdk_path
os.environ["PATH"] += os.pathsep + os.path.join(android_sdk_path, "platform-tools")
os.environ["PATH"] += os.pathsep + os.path.join(android_sdk_path, "tools")
os.environ["PATH"] += os.pathsep + os.path.join(android_sdk_path, "cmdline-tools", "latest", "bin")

capabilities = dict(
    platformName='Android',
    automationName='UiAutomator2',
    deviceName='Android',
    udid='R9ZX809P77P',
    appPackage='com.example.hms_backoffice',
    appActivity='.MainActivity',
    language='en',
    locale='US'
)

appium_server_url = 'http://127.0.0.1:4723'


class TestAppium(unittest.TestCase):

    def setUp(self):
        options = UiAutomator2Options().load_capabilities(capabilities)
        self.driver = webdriver.Remote(appium_server_url, options=options)

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def test_01_login_flow(self):
        print("\n=== LOGIN FLOW ===")

        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Get Started").click()
            print("[OK] Clicked Get Started")
        except:
            print("[SKIP] Get Started not found")

        self.driver.implicitly_wait(2)

        try:
            self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Skip").click()
            print("[OK] Clicked Skip")
        except:
            print("[SKIP] Skip not found")

        self.driver.implicitly_wait(3)

        try:
            username_field = self.driver.find_element(AppiumBy.XPATH, "//android.widget.EditText[contains(@text, 'username') or contains(@hint, 'username') or @index='0']")
            username_field.click()
            username_field.clear()
            username_field.send_keys("hms")
            print("[OK] Entered username: hms")
        except:
            edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
            if edit_texts:
                edit_texts[0].click()
                edit_texts[0].send_keys("hms")
                print("[OK] Entered username via fallback EditText")
            else:
                print("[ERROR] Username field not found")

        edit_texts = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        if len(edit_texts) >= 2:
            edit_texts[1].click()
            for digit in "1234":
                self.driver.press_keycode(int(digit) + 7)
                time.sleep(0.3)
            print("[OK] Entered PIN: 1234")
        else:
            print("[ERROR] PIN field not found")

        try:
            self.driver.find_element(AppiumBy.XPATH, "//android.widget.Button[contains(@text, 'Login') or contains(@content-desc, 'Login')]").click()
            print("[OK] Clicked Login button")
        except:
            print("[SKIP] Login button not found")

        print("[WAIT] Waiting for dashboard...")
        time.sleep(1)

        self.open_menu()
        self.bulk_invoices_flow()

    def open_menu(self):
        print("\n=== OPEN MENU ===")
        try:
            if self.driver.find_elements(AppiumBy.XPATH, "//*[contains(@content-desc, 'Hotel M') or contains(@content-desc, 'Thanjav') or @class='android.widget.PopupWindow']"):
                print("[INFO] Overlay detected, dismissing...")
                self.driver.back()
                time.sleep(1)

            print("[INFO] Swiping left to right to open drawer...")
            self.driver.swipe(5, 500, 500, 500, 1000)
            time.sleep(1)

            wait = WebDriverWait(self.driver, 5)

            def find_menu_btn(d):
                e1 = d.find_elements(AppiumBy.XPATH, "//android.widget.ImageView[@clickable='true' and @index='0']")
                if e1:
                    return e1[0]
                for img in d.find_elements(AppiumBy.XPATH, "//android.widget.ImageView[@clickable='true']"):
                    if img.location['x'] < 150 and img.location['y'] < 250:
                        return img
                return None

            try:
                wait.until(find_menu_btn).click()
                print("[OK] Menu button clicked")
            except:
                print("[SKIP] Menu button not found, swipe may have worked")

            time.sleep(2)
        except:
            print("[FALLBACK] Tapping menu coordinates (67, 131)")
            self.driver.tap([(67, 131)])
            time.sleep(1)

    def bulk_invoices_flow(self):
        print("\n=== BULK INVOICE FLOW ===")
        wait = WebDriverWait(self.driver, 15)
        time.sleep(1)

        
        print("[INFO] Searching for Bulk Invoice in menu...")
        try:
            search_fields = self.driver.find_elements(AppiumBy.XPATH,
                "//android.widget.EditText[contains(@text, 'Search') or contains(@hint, 'Search')]"
            )
            if search_fields:
                search_fields[0].click()
                search_fields[0].send_keys("Bulk Invoice")
                print("[OK] Typed 'Bulk Invoice' in search bar")
                time.sleep(1)
                try:
                    self.driver.hide_keyboard()
                except:
                    pass
                time.sleep(1)

            bulk_btn = wait.until(lambda d: d.find_element(AppiumBy.XPATH,
                "//*[not(contains(@class, 'EditText')) and (contains(@content-desc, 'Bulk Invoice') or contains(@text, 'Bulk Invoice'))]"
            ))
            bulk_btn.click()
            print("[OK] Clicked Bulk Invoice menu item")
        except Exception as e:
            print(f"[ERROR] Could not navigate to Bulk Invoice: {e}")
            return

        # 2. Wait for Bulk Invoice screen
        print("[WAIT] Waiting for Bulk Invoice screen to load...")
        try:
            wait.until(lambda d: d.find_element(AppiumBy.XPATH,
                "//*[contains(@text, 'Last 7 Days') or contains(@content-desc, 'Last 7 Days')]"
            ))
            print("[OK] Bulk Invoice screen loaded")
        except TimeoutException:
            print("[ERROR] Bulk Invoice screen did not load")
            return

        time.sleep(1)

        # 3. Open dropdown and select Last 7 Days
        print("[INFO] Opening Date Range dropdown...")
        try:
            self.driver.find_element(AppiumBy.XPATH,
                "//*[contains(@text, 'Last 7 Days') or contains(@content-desc, 'Last 7 Days')]"
            ).click()
            print("[OK] Dropdown opened")
            time.sleep(1)
            wait.until(lambda d: d.find_element(AppiumBy.XPATH,
                "//*[contains(@text, 'Last 7 Days') or contains(@content-desc, 'Last 7 Days')]"
            )).click()
            print("[OK] Selected 'Last 7 Days'")
            time.sleep(2)
        except Exception as e:
            print(f"[SKIP] Dropdown interaction skipped: {e}")

        # 4. Wait for invoice list
        print("[WAIT] Waiting for invoice list...")
        try:
            wait.until(lambda d: d.find_elements(AppiumBy.XPATH,
                "//*[contains(@text, 'INV') or contains(@content-desc, 'INV')]"
            ))
            invoices = self.driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@text, 'INV') or contains(@content-desc, 'INV')]"
            )
            print(f"[OK] Found {len(invoices)} invoice(s) in list")
        except TimeoutException:
            print("[ERROR] No invoices found in list")
            return

        time.sleep(1)

        # 5. Tap left side of first invoice row to select checkbox
        print("[INFO] Tapping checkbox area of first invoice row...")
        try:
            invoices = self.driver.find_elements(AppiumBy.XPATH,
                "//*[contains(@text, 'INV') or contains(@content-desc, 'INV')]"
            )
            if not invoices:
                print("[ERROR] Invoice list is empty")
                return

            first = invoices[1]
            row_y = first.location['y']
            row_h = first.size['height']
            tap_x = 75
            tap_y = row_y + (row_h // 2)

            print(f"[INFO] First invoice: {first.get_attribute('text') or first.get_attribute('content-desc')}")
            print(f"[INFO] Tapping checkbox at x={tap_x}, y={tap_y}")
            self.driver.tap([(tap_x, tap_y)])
            print("[OK] Checkbox tapped")
        except Exception as e:
            print(f"[ERROR] Could not tap checkbox: {e}")
            return

        time.sleep(1)

        # 6. Confirm checkbox is selected (Download bar should appear)
        print("[WAIT] Waiting for Download button to appear after selection...")
        try:
            download_btn = wait.until(lambda d: d.find_element(AppiumBy.XPATH,
                "//*[contains(@text, 'Download') or contains(@content-desc, 'Download')]"
            ))
            print("[OK] Checkbox selected — '1 selected' bar with Download appeared")
            download_btn.click()
            print("[OK] Clicked Download button")
        except TimeoutException:
            print("[ERROR] Download button did not appear — checkbox may not have been selected")
            print("[DEBUG] Visible texts on screen:")
            try:
                all_els = self.driver.find_elements(AppiumBy.XPATH, "//*[@text!='']")
                for el in all_els[:20]:
                    txt = el.get_attribute("text")
                    if txt:
                        print(f"        -> {txt}")
            except:
                print("[ERROR] Could not get visible texts")


if __name__ == "__main__":
    unittest.main()