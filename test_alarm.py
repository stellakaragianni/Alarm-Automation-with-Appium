#TEST APIDEMOS APK : ANDROID STUDIO APPROACH
# BY KARAGIANNI STELLA @2026
#

# Uncomment below to manually set Android SDK environment variables on Windows (useful when Appium can't find the SDK)
# import os
# os.environ["ANDROID_HOME"] = r"C:\Users\karagianniste\AppData\Local\Android\Sdk" #change with your local path
# os.environ["PATH"] += r";C:\Users\karagianniste\AppData\Local\Android\Sdk\platform-tools" #change with your local path

import unittest # Python's built-in testing framework. It provides methods for writing/running TCs(TestCase class, setUp(), tearDown(), assertTrue() etc.).
import time # Clock in sleep(), monotonic().
from appium import webdriver # Appium's client to control phone.
from appium.options.android import UiAutomator2Options # Android's config object for setting up info like device name, app path, and automation engine.
from appium.webdriver.common.appiumby import AppiumBy # Collection of locator strategies. It tells Appium how to find an element — by accessibility ID, by text, by XPath.
from selenium.webdriver.support.ui import WebDriverWait # Waiting - retries finding an element repeatedly until it appears or the timer runs out.
from selenium.webdriver.support import expected_conditions as EC # Collab with teh above for pending expected outcomes of specific conditions.

class MoroTechTest(unittest.TestCase):
    
    # Options Object (capabilities): Runs before each test. Configures the connection with Android emulator and launches the app.
    def setUp(self):
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "Android Emulator"
        options.automation_name = "UiAutomator2"
        options.app = r"C:\Users\karagianniste\Desktop\ApiDemos-debug.apk"

        # Remote Driver Conenction: Connect to the Appium server and start a session with the configured options.
        self.driver = webdriver.Remote("http://localhost:4723", options=options)
        # Wait for driver/element to load before testing : applied globally.
        self.wait = WebDriverWait(self.driver, 20)

    # Global Wait: Smart peek through helper: every 0.2secs tries to find the text-element; TimeoutError if text not found within 10secs.
    def wait_for_text_in_page(self, phrase, timeout=10):
        end_time = time.monotonic() + timeout
        while time.monotonic() < end_time:
            if phrase in self.driver.page_source:
                return True
            time.sleep(0.2)  # 0.2 --> toast = very short-lived
        raise TimeoutError(f"Text '{phrase}' not found within {timeout}s")

    # Test the following flow on APK:
    # - Verifies the home screen loads correctly
    # - Navigates to App > Alarm > Alarm Controller
    # - Triggers a one-shot alarm
    # - Confirms the '30 seconds' toast appears immediately after scheduling
    # - peeks for up to 60s until the 'gone off' toast appears once the alarm fires
    
    # Locator Strategy:
    # - ANDROID_UIAUTOMATOR -> text elements
    # - ACCESSIBILITY_ID -> navigation
    # - page source -> toast (with XPath help)

    def test_alarm_journey(self):
        # 1. Verify the home screen header is visible
        header = self.wait.until(EC.presence_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("API Demos")')))
        self.assertTrue(header.is_displayed())

        # 2. Navigate to the Alarm Controller screen
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, "App").click()
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Alarm"))).click()
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Alarm Controller"))).click()

        # 3. Tap the button to schedule a one-shot alarm (fires in 30 seconds)
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("One Shot Alarm")').click()

        # 4. Confirm the first toast message indicates the alarm is set for 30 seconds
        self.assertTrue(self.wait_for_text_in_page("30 seconds", timeout=10))
        print("Verified First Pop-Up!")

        # 5. Start peeking immediately — don't sleep a fixed amount - every 0.2s for up to 60s so we don't miss the toast.
        print("Waiting for alarm to go off (peeking for up to 60s)...")
        self.assertTrue(self.wait_for_text_in_page("gone off", timeout=60))
        print("Verified Final Pop-up: 'Gone Off'!")

    # Closes Appium session, once done with testing.
    def tearDown(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    unittest.main()