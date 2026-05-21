# API Demos – Android Test Suite (BrowserStack)

Automated tests for the ApiDemos Android app running on a real device in the BrowserStack cloud.
---

## Prerequisites

- Python 3.10+
- A BrowserStack account
---

## Setup

**1. Install dependencies**

```
pip install Appium-Python-Client==3.1.0 selenium==4.15.2 pytest==7.4.3
```

**2. Add your BrowserStack credentials to `config.py` in variables:**

- BS_USERNAME
- BS_ACCESS_KEY

**3. Upload APK file on BrowserStack, copy the App ID & insert it in the test_alarm_journey.py**
```
APP_ID = "bs://"
```
---

## Run the tests

- Open terminal.
- Run: 
```
cd <the_path_where_test_folder_exists>
python -m pytest api_demos_final
```
Watch the test run live at App Automate Page of BrowserStack
---

## Notes
- **api_demos_final** folder exists in the scripts of my IDE (not installed globally), hence I run: 
```
cd C:\Users\karagianniste\AppData\Local\Programs\Thonny\Scripts
.\pytest api_demos_final
``` 
so that pytest command is visible from terminal.
- The ApiDemos APK is already uploaded to BrowserStack (app ID hardcoded in the test file)
- Tests run on a Google Pixel 7 with Android 13
- Each test starts a fresh device session and closes it after
