
Appium Test Framework
======================

# Setup Appium

## System Requirements
- OSX > 10.9
- Python > 2.7
- Selenium python bindings
- Appium
- ios: > xcode 5.0.2
- android: Latest Android Studio (http://developer.android.com/sdk/installing/studio.html) and install updates 

## System Setup
Python is available in OSX by default
```
$ python --version
```
## Install selenium
```
$ sudo easy_install selenium
```
## Install nose
```
$ sudo easy_install nose
```
## Install node and npm
Go to nodejs.org 
- Click install  
- Click the downloaded .pkg 
- Follow installer

## Install appium
```
$ sudo chown -R $USER /usr/local
$ npm install -g appium
```
## Install appium python bindings
```
$ sudo easy_install pip
$ sudo pip install Appium-Python-Client
```
Make sure all required tools are available for appium
```
$ appium-doctor
```
You will be prompted to install any missing tools, follow prompts and install tools

Make sure the Instruments app is not already open 

Android: set Android Home

By default android sdk is in "Android Studio.app". The space in the folder name causes issues, Making a soft link without the space seems to solve this

```
$ ln -s /Applications/Android Studio.app/sdk /Applications/AndroidStudio.app/sdk
$ export ANDROID_HOME=/Applications/AndroidStudio.app/sdk
```
Device:
Connect a device > 4.1 through usb and enable android debugging (Settings->Developer options-> USB Debugging enable)
If you dont see the developer options , Tap 7 times on Settings->About Phone -> Build number

Make sure the adb lists devices
```
$ adb devices
```

## Start appium
```
$ appium &
```

## Troubleshoot

If there is a instruments crash, Kill appium  Clean up appium tmp folder and restart the server
```
$ killall node
$ rm /tmp/instruments_sock
$ appium &
```
- if you still see the crash rebuild the .app file using the -b flag from runtests.sh. Sometimes the info.plist corruption also crashes instruments
- Make sure you always install appium without being a sudo, if you have accidentally installed appium as sudo, uninstall appium and reinstall again
```
$ sudo uninstall -g appium
$ sudo chown -R $USER /usr/local
$ npm install -g appium
```

# Test Development Guidelines

General rules of thumb for test writing:

- Minimize iosTest / androidTest checking as much as possible in the Test.py files. Move all differences between iOS and android to page.py. The differences may be due to element names / attributes, the flow in app itself is different, or there are specific appium differences (Eg appium difference accessing web views in android and iOS)
- Avoid XPath usage as much as possible, always try to find elements by Name. if the elements cannot be found by name, try and add accessibility identifiers in iOS or content description in android for element accessibility
- Talk to development, try to sync the element names of android and iOS, wherever possible
- Talk to development / designers and try to sync the flow of the app wherever possible
