# Automation API Demos Android, running via BrowserStack cloud.
# By Karagianni Stella @2026
#

import time # Clock in sleep(), monotonic().
import pytest # 3rd party framework, contains eg fixtures, good for readable tests
from appium import webdriver # Appium's client to control phone.
from appium.options.android import UiAutomator2Options # Android's config object for setting up info like device name, app path, and automation engine.
from appium.webdriver.common.appiumby import AppiumBy # Collection of locator strategies. It tells Appium how to find an element — by accessibility ID, by text, by XPath.
from selenium.webdriver.support.ui import WebDriverWait # Waiting for selenium- retries finding an element repeatedly until it appears or the timer runs out.
from selenium.webdriver.support import expected_conditions as EC # Collab with teh above for pending expected outcomes of specific conditions / instead of writing complex waiting logic.
import config  # reads BS_USERNAME and BS_ACCESS_KEY from config.py

# Constants
BROWSERSTACK_URL = (
    f"https://{config.BS_USERNAME}:{config.BS_ACCESS_KEY}"
    f"@hub.browserstack.com/wd/hub")

APP_ID = "bs://e8b31bdf8b0c1a11b5db394498c792680bb88b3f" # Insert the app id from Browserstack here.

# Set Up: start a browser stack session & close it after test is done.
@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.app = APP_ID

    options.set_capability("bstack:options", {
        "deviceName":  "Google Pixel 7",
        "osVersion":   "13.0",
        "projectName": "API Demos Assignment",
        "buildName":   "Alarm Journey",
        "sessionName": "test run",
        "debug":       "true",
    })

    # Initiate a new browser session d with the above options > pause & pass d to the code > resume execution
    d = webdriver.Remote(BROWSERSTACK_URL, options=options)
    yield d
    d.quit()

# Helper 1: wait 'till element with message 'text' appears.
def find_by_text(driver, text, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{text}")'
        ))
    )

# Wait until the app's page source contains the given phrase - using page source, since toasts are short lived.
def wait_for_toast(driver, phrase, timeout=10):
    end_time = time.monotonic() + timeout
    while time.monotonic() < end_time:
        if phrase in driver.page_source:
            return True
        time.sleep(0.5)  # check every half second
    raise TimeoutError(f"Toast with phrase: '{phrase}' did not appear within {timeout} secs")


# TEST SUITE

# Header finder for APK
def test_01_header_is_api_demos(driver):
    title = find_by_text(driver, "API Demos")
    assert title.is_displayed()

# Fidn the text "App" & click it
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

# in "Alarm", find "Alarm Controller" & click it
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

# Pend for "30 seconds" toast to appear
def test_06_toast_says_30_seconds(driver):
    find_by_text(driver, "App").click()
    find_by_text(driver, "Alarm").click()
    find_by_text(driver, "Alarm Controller").click()
    find_by_text(driver, "One Shot Alarm").click()
    # Check page source for the toast text — more reliable than finding the element
    assert wait_for_toast(driver, "30 seconds", timeout=10)

# After the "30 seconds" alarm, pend for 90 secs for the "gone off" toast
def test_07_toast_says_gone_off(driver):
    find_by_text(driver, "App").click()
    find_by_text(driver, "Alarm").click()
    find_by_text(driver, "Alarm Controller").click()
    find_by_text(driver, "One Shot Alarm").click()
    # Wait up to 90 seconds for the final alarm to fire
    assert wait_for_toast(driver, "gone off", timeout=90)