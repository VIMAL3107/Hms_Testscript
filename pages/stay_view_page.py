"""
Stay View Page — encapsulates Stay View screen interactions.
"""

import time
from config.settings import SCREEN_LOAD_DELAY


class StayViewPage:
    """Page Object for the Stay View screen."""

    def __init__(self, driver):
        self.driver = driver

    def wait_for_screen(self):
        """Wait for the Stay View screen to finish loading."""
        print("[WAIT] Waiting for Stay View screen...")
        time.sleep(SCREEN_LOAD_DELAY)
        print("[OK] Stay View screen loaded")

    def scroll_content(self, times=4, delay=1.5):
        """Scroll down through the Stay View content."""
        print("[INFO] Scrolling Stay View page...")
        size = self.driver.get_window_size()
        for i in range(times):
            try:
                self.driver.swipe(
                    size["width"] // 2,
                    int(size["height"] * 0.8),
                    size["width"] // 2,
                    int(size["height"] * 0.3),
                    700,
                )
                print(f"[INFO] Scroll {i + 1}/{times}")
            except Exception:
                print(f"[WARN] Scroll {i + 1} failed, stopping")
                break
            time.sleep(delay)
        print("[OK] Scrolling completed")
