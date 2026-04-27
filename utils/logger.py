"""
Logger Utility — custom logging for test execution with timestamps.
"""

import time
from datetime import datetime


class TestLogger:
    """Provides formatted logging for test steps."""

    def __init__(self, test_name="Test"):
        self.test_name = test_name
        self.start_time = None

    def start(self):
        """Mark the test start time."""
        self.start_time = time.time()
        self._log("START", f"=== {self.test_name} STARTED ===")

    def end(self):
        """Mark the test end and print elapsed time."""
        elapsed = time.time() - self.start_time if self.start_time else 0
        self._log("END", f"=== {self.test_name} COMPLETED in {elapsed:.1f}s ===")

    def step(self, message):
        self._log("STEP", message)

    def ok(self, message):
        self._log("OK", message)

    def error(self, message):
        self._log("ERROR", message)

    def warn(self, message):
        self._log("WARN", message)

    def info(self, message):
        self._log("INFO", message)

    def skip(self, message):
        self._log("SKIP", message)

    @staticmethod
    def _log(level, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
