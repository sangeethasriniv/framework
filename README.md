
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
If you dont see the developer options , Tap 7 times on Settings->About Phone -> Build number. itz a Magic you are developer now

Make sure the adb lists devices
```
$ adb devices
```

## Start appium
```
$ appium &
```

## Run uitests
In a different terminal window, change to uitests folder and execute the runtests.sh
```
$ cd <your repo>/socialcast-ios/socialcast-uitest
$ ./runtests.sh -e iphonesimulator -b /path/to/sources/of/ios/app
$ ./runtests.sh -e android -b /path/to/sources/of/android/app
```
Note: 
- once the app is built and available in the <your repo>/socialcast-ios/socialcast-uitest/build folder, you can run tests without the -b in command line
- runtests.sh -h lists the options available to run tests

## Running tests in ios device

### Xcode Setup
- Make sure your xcode in the host, where you are attempting to run the tests has the right certs and provisioning profiles needed for code signing the app
- Launch the app in device from xcode and see if it works all goes well
Refer: https://developer.apple.com/legacy/library/documentation/ToolsLanguages/Conceptual/YourFirstAppStoreSubmission/ProvisionYourDevicesforDevelopment/ProvisionYourDevicesforDevelopment.html#//apple_ref/doc/uid/TP40011375-CH4-SW1

### Build proxy to access web views on ios devices
```
$ git clone https://github.com/google/ios-webkit-debug-proxy.git
$ cd ios-webkit-debug-proxy
$ ./autogen.sh
$ ./configure
$ make
$ sudo make install
```
### Run tests on Iphone

- In Device Settings->Safari, Advanced -> enable web inspector
- Connect device using USB 
- Open a terminal and run the proxy with the device udid (Get device udid from xcode->window->organizer->device->Identifier) 

```
$ ios_webkit_debug_proxy -c <urdeviceudid>:27753 -d
```

- Edit udid in the testutils/ios7device.json with your device udid
- run the tests with iphone environment (-e iphone)
- Supply the json file having the ios device configuration (-j testutils/ios7device.json)
- in order to build the app for iphone pass in the code signing identity and provisioning profile for the device connected

To get the code signing identity use command and copy the string starting with  "iphone developer"

```
$ security find-identity -p codesiging
```
To get the provisioning profile used in the device, 
 - install and open iphone configuration utility
 - Click on provisioning profile that you would like to use for the device (Double check, if clicking on the provisioning profile lists the device connected currently in the included devices section)  
 - Copy the profile-identitifier (e.g: 6C1F5334-FBB5-4FD5-A703-F4EE57EDD254)
 
Now you can run the tests putting all of the above together, using the following command 

```
$ ./runtests.sh -e iphone -j testutils/ios7device.json -i <code signing identity> -p <prov profile identifier>
eg:
./runtests.sh -e iphone -b ~/work/socialcast-ios  -i "iPhone Developer: Sangeetha Srinivasan" -p "6C1F5334-FBB5-4FD5-A703-F4EE57EDD254" -j testutils/ios7device.json
```
Note: 
- Create a json file for any new test environment similar to the json files in the testutils folder and pass the json file to the runtests command as above to execute tests in the new environment.
- Whenever testing with a new environment it is safe to clean up the build folder, before starting a new build and test 

```
$ rm -rf socialcast-uitest/build"
```
or use -c in the runtests.sh command

## Troubleshoot
- if you see the android tests not running as expected, the first thing to check is, if you have updated your android code base both v3 and hydra repos and make sure to get the latest test code, from the ios repo. Since the common tests for android and ios lives in the ios repo, it is important to keep all 3 repos up to date and build a fresh test app once again
- It is a good idea to clean up the build folder to discard the older apps and build afresh from runtests using -b flag everytime you update the sources
- If there is a instruments crash, Kill appium  Clean up appium tmp folder and restart the server
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
- If you are unable to install an android app in device due to [INSTALL_PARSE_FAILED_INCONSISTENT_CERTIFICATES], the permissions are not correct and probably you installed appium as a sudo user. You can try the last bullets solution. if not simply say sudo chown -R $USER /usr/local/bin/appium

# Test Development Guidelines

General rules of thumb for test writing:

- Minimize iosTest / androidTest checking as much as possible in the Test.py files. Move all differences between iOS and android to page.py. The differences may be due to element names / attributes, the flow in app itself is different, or there are specific appium differences (Eg appium difference accessing web views in android and iOS)
- Avoid XPath usage as much as possible, always try to find elements by Name. if the elements cannot be found by name, try and add accessibility identifiers in iOS or content description in android for element accessibility
- Talk to development, try to sync the element names of android and iOS, wherever possible
- Talk to development / designers and try to sync the flow of the app wherever possible
