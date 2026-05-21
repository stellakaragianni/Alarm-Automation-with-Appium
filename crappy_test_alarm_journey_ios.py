# Automation API Demos iOS, running via BrowserStack cloud.
# By Karagianni Stella @2026
#
# HOW TO RUN:
#   0. Install requirements.txt
#      - Also run: appium driver install xcuitest
#   1. Paste your BrowserStack username and access key into config.py
#   2. Upload your .ipa file to BrowserStack and replace APP_ID below with the returned bs:// URL
#      - Upload via: https://app-automate.browserstack.com/dashboard → Upload App
#      - Or via CLI: curl -u "user:key" -X POST ... (see BrowserStack docs)
#   3. Open PowerShell/Terminal inside your project folder
#   4. Run:  pytest test_alarm_journey_ios_browserstack.py
#   5. Watch live at https://app-automate.browserstack.com

import time
import pytest
from appium import webdriver
from appium.options.ios import XCUITestOptions              # iOS config object (replaces UiAutomator2Options)
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config  # reads BS_USERNAME and BS_ACCESS_KEY from config.py

# Constants
BROWSERSTACK_URL = (
    f"https://{config.BS_USERNAME}:{config.BS_ACCESS_KEY}"
    f"@hub.browserstack.com/wd/hub")

APP_ID = "bs://5aa7d94a3970901801502661ca5dfad802000eeb"


# Set Up: start a BrowserStack session & close it after test is done
@pytest.fixture(scope="function")
def driver():
    options = XCUITestOptions()
    options.platform_name = "iOS"
    options.automation_name = "XCUITest"
    options.app = APP_ID

    options.set_capability("bstack:options", {
        "deviceName":  "iPhone 14",       # BrowserStack real device name — see full list at browserstack.com/list-of-browsers-and-platforms/app_automate
        "osVersion":   "16",              # iOS version available on BrowserStack
        "projectName": "API Demos Assignment",
        "buildName":   "Alarm Journey iOS",
        "sessionName": "test run",
        "debug":       "true",
    })

    d = webdriver.Remote(BROWSERSTACK_URL, options=options)
    yield d
    d.quit()


# Helper 1: wait until an element with matching label text appears
# iOS uses IOS_PREDICATE_STRING instead of ANDROID_UIAUTOMATOR
def find_by_text(driver, text, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((
            AppiumBy.IOS_PREDICATE_STRING,
            f'label == "{text}"'           # iOS equivalent of UiSelector().text()
        ))
    )

# Helper 2: wait until the app's page source contains the given phrase.
# NOTE: iOS doesn't have Android-style toasts. Transient messages may appear
# as UIAlertControllers, banners, or custom overlays — page_source polling still works
# if the text is rendered in the accessibility tree.
def wait_for_toast(driver, phrase, timeout=10):
    end_time = time.monotonic() + timeout
    while time.monotonic() < end_time:
        if phrase in driver.page_source:
            return True
        time.sleep(0.5)
    raise TimeoutError(f"Toast with phrase: '{phrase}' did not appear within {timeout} secs")


# TEST SUITE

# Header finder for the app
def test_01_header_is_api_demos(driver):
    title = find_by_text(driver, "API Demos")
    assert title.is_displayed()

# Find the text "App" & click it
def test_02_click_app(driver):
    app_option = find_by_text(driver, "App")
    assert app_option.is_displayed()
    app_option.click()

# Find "App", click it; then find "Alarm" & click it too
def test_03_click_alarm(driver):
    find_by_text(driver, "App").click()
    alarm_option = find_by_text(driver, "Alarm")
    assert alarm_option.is_displayed()
    alarm_option.click()

# In "Alarm", find "Alarm Controller" & click it
def test_04_click_alarm_controller(driver):
    find_by_text(driver, "App").click()
    find_by_text(driver, "Alarm").click()
    alarm_controller = find_by_text(driver, "Alarm Controller")
    assert alarm_controller.is_displayed()
    alarm_controller.click()

# In "Alarm Controller", find "One Shot Alarm" & click it
def test_05_click_one_shot_alarm(driver):
    find_by_text(driver, "App").click()
    find_by_text(driver, "Alarm").click()
    find_by_text(driver, "Alarm Controller").click()
    one_shot = find_by_text(driver, "One Shot Alarm")
    assert one_shot.is_displayed()
    one_shot.click()

# Pend for "30 seconds" toast/message to appear
def test_06_toast_says_30_seconds(driver):
    find_by_text(driver, "App").click()
    find_by_text(driver, "Alarm").click()
    find_by_text(driver, "Alarm Controller").click()
    find_by_text(driver, "One Shot Alarm").click()
    assert wait_for_toast(driver, "30 seconds", timeout=10)

# After the "30 seconds" alarm, pend for 90 secs for the "gone off" message
def test_07_toast_says_gone_off(driver):
    find_by_text(driver, "App").click()
    find_by_text(driver, "Alarm").click()
    find_by_text(driver, "Alarm Controller").click()
    find_by_text(driver, "One Shot Alarm").click()
    assert wait_for_toast(driver, "gone off", timeout=90)
