# API Demos – Android Test Suite (Local Emulator with Android Studio)

Automated tests for the ApiDemos Android app running on a local Android emulator.
---

## Prerequisites

- Python 3.10+
- Node.js (https://nodejs.org)
- Android Studio (https://developer.android.com/studio)
---

## One-time setup

**1. Install Appium**

```
npm install -g appium
appium driver install uiautomator2
```

**2. Install Python dependencies**

```
pip install Appium-Python-Client selenium
```

**3. Set ANDROID_HOME environment variable**

- Click "Edit the system environment variables" → "Environment Variables": "New"
  - Name: `ANDROID_HOME`
  - Value: `C:\Users\<your_username>\AppData\Local\Android\Sdk`
- Under User variables → select "Path" → click "Edit" → click "New" → paste:
  - `C:\Users\<your_username>\AppData\Local\Android\Sdk\platform-tools`
- Click OK and restart terminal

**4. Create an emulator in Android Studio**

- Open Android Studio → Tools → Device Manager → Create Device
  - E.g. Pixel 6, API 36

**5. Update the APK path in `test_alarm.py` & drop APK file to desktop**

```python
options.app = r"C:\Users\<your_username>\Desktop\ApiDemos-debug.apk"
```
---

## How to RUN:


**Step 1** — Start the emulator in Android Studio; wait for the home screen to appear

**Step 2** — Open a terminal and start Appium; leave this window open

**Step 3** — Open a second terminal from the folder where test_alarm.py is and run:
```
python test_alarm.py
```
---

## Notes

- The emulator must be fully booted before running the tests
- The Appium server must be running in a separate terminal
- Test report is generated inside the the second CMD, mentioning if suite passed/failed 
