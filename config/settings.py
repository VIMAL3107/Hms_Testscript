"""
Configuration settings for the HMS Backoffice test automation framework.
All device, app, and server settings are centralized here.
"""

import os

# ─────────────────────────────────────────────
# Android SDK Path Setup
# ─────────────────────────────────────────────
ANDROID_SDK_PATH = os.path.expandvars(r"%LOCALAPPDATA%\Android\Sdk")

os.environ["ANDROID_HOME"] = ANDROID_SDK_PATH
os.environ["PATH"] += os.pathsep + os.path.join(ANDROID_SDK_PATH, "platform-tools")
os.environ["PATH"] += os.pathsep + os.path.join(ANDROID_SDK_PATH, "tools")
os.environ["PATH"] += os.pathsep + os.path.join(ANDROID_SDK_PATH, "cmdline-tools", "latest", "bin")


# ─────────────────────────────────────────────
# Appium Server
# ─────────────────────────────────────────────
APPIUM_SERVER_URL = "http://127.0.0.1:4723"


# ─────────────────────────────────────────────
# Device Capabilities
# ─────────────────────────────────────────────
CAPABILITIES = {
    "platformName": "Android",
    "automationName": "UiAutomator2",
    "deviceName": "Android",
    "udid": "c0f6a4c5",
    "appPackage": "com.example.hms_backoffice",
    "appActivity": ".MainActivity",
    "language": "en",
    "locale": "US"
}


# ─────────────────────────────────────────────
# Test Data / Credentials
# ─────────────────────────────────────────────
LOGIN_USERNAME = "hms"
LOGIN_PIN = "1234"


# ─────────────────────────────────────────────
# Timeouts (seconds)
# ─────────────────────────────────────────────
IMPLICIT_WAIT = 3
EXPLICIT_WAIT_SHORT = 5
EXPLICIT_WAIT_DEFAULT = 10
EXPLICIT_WAIT_LONG = 15

STABILIZE_DELAY = 2       # General UI stabilization delay
MENU_LOAD_DELAY = 2       # Wait after opening a menu
SCREEN_LOAD_DELAY = 3     # Wait after navigating to a new screen
SCROLL_DELAY = 1.5        # Wait between scroll actions
