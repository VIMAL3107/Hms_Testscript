
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.settings import EXPLICIT_WAIT_DEFAULT

class BasePage:
    """Base class for all Page Objects in the HMS Backoffice automation."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT_DEFAULT)

    @staticmethod
    def auto_wait(func):
        """Decorator to automatically wait for loading before executing a method."""
        def wrapper(self, *args, **kwargs):
            self.wait_for_loading()
            return func(self, *args, **kwargs)
        return wrapper

    def wait_for_loading(self, timeout=300):
        """
        Optimized dynamic wait for background loading/spinners.
        Checks for multiple loader types in a single query for speed.
        """
        # Combine all locators into one single XPath for performance
        loader_xpath = (
            "//android.widget.ProgressBar | "
            "//*[contains(@content-desc, 'Loading')] | "
            "//*[contains(@text, 'Loading')] | "
            "//*[contains(@content-desc, 'Please wait')] | "
            "//*[contains(@text, 'Please wait')] | "
            "//android.widget.ImageView[contains(@content-desc, 'spinner')]"
        )
        
        start_time = time.time()
        # Set a very short implicit wait for this check
        self.driver.implicitly_wait(0.5)
        
        try:
            while time.time() - start_time < timeout:
                loaders = self.driver.find_elements(AppiumBy.XPATH, loader_xpath)
                active_loader = None
                for l in loaders:
                    try:
                        if l.is_displayed():
                            active_loader = l
                            break
                    except: continue
                
                if not active_loader:
                    # Double check after a tiny gap to avoid flicker
                    time.sleep(0.2)
                    loaders = self.driver.find_elements(AppiumBy.XPATH, loader_xpath)
                    still_loading = False
                    for l in loaders:
                        try:
                            if l.is_displayed():
                                still_loading = True; break
                        except: continue
                    if not still_loading:
                        return True
                
                desc = ""
                try: desc = active_loader.get_attribute("content-desc") or active_loader.get_attribute("text") or "spinner"
                except: desc = "spinner"
                print(f"[WAIT] Still loading ({desc})...")
                time.sleep(1)
        except:
            pass
        finally:
            # Restore default implicit wait
            self.driver.implicitly_wait(5)
            
        return False

    def _debug_dump_screen(self, limit=30):
        """Dump visible elements for debugging."""
        print("\n=== PAGE SOURCE DUMP ===")
        try:
            all_els = self.driver.find_elements(AppiumBy.XPATH, "//*[@text!='' or @content-desc!='']")
            for el in all_els[:limit]:
                t = el.get_attribute('text') or ''
                c = el.get_attribute('content-desc') or ''
                print(f"  - Text: '{t}' | Desc: '{c[:60]}'")
        except Exception:
            print("(Could not dump elements)")
        print("=== END DUMP ===\n")

    def select_dropdown(self, dropdown_index, option_text):
        """Select an option from a dropdown by its index and option text.
        
        Args:
            dropdown_index: 1-based index of the dropdown (e.g., 1 for first 'Select' button)
            option_text: The text/content-desc of the option to select
        """
        try:
            print(f"[INFO] Selecting '{option_text}' from dropdown {dropdown_index}")

            # Try multiple element types for the 'Select' dropdown button
            dropdown = None
            dropdown_xpaths = [
                f"(//*[@content-desc='Select'])[{dropdown_index}]",
                f"(//android.widget.Button[@content-desc='Select'])[{dropdown_index}]",
                f"(//android.view.View[@content-desc='Select'])[{dropdown_index}]",
            ]

            for xpath in dropdown_xpaths:
                try:
                    dropdown = self.driver.find_element(AppiumBy.XPATH, xpath)
                    if dropdown:
                        print(f"[OK] Found dropdown using: {xpath}")
                        break
                except Exception:
                    continue

            if not dropdown:
                print("[ERROR] Dropdown button not found")
                return False

            dropdown.click()
            time.sleep(2)

            # Try to find and click the option
            option = None
            option_xpaths = [
                f"//*[@text='{option_text}' or @content-desc='{option_text}']",
                f"//*[contains(@text,'{option_text}') or contains(@content-desc,'{option_text}')]",
            ]

            for xpath in option_xpaths:
                try:
                    elements = self.driver.find_elements(AppiumBy.XPATH, xpath)
                    for el in elements:
                        if el.is_displayed():
                            option = el
                            break
                    if option:
                        break
                except Exception:
                    continue

            if not option:
                print(f"[ERROR] Option '{option_text}' not found in dropdown")
                return False

            option.click()

            print(f"[OK] Selected {option_text}")
            time.sleep(1)
            return True

        except Exception as e:
            print(f"[ERROR] Dropdown selection failed: {e}")
            return False

    def tap_coordinates(self, x, y, label=""):
        """Tap at absolute coordinates."""
        self.driver.tap([(x, y)])
        print(f"[OK] Tapped at ({x}, {y}){ ' - ' + label if label else ''}")

    def get_window_size(self):
        """Return the window size."""
        return self.driver.get_window_size()

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
            time.sleep(2)

        print("[ERROR] No occupied room found after scrolling")
        return False
