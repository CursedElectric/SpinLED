# SpinLED

A Spin Rhythm XD mod for taking note inputs in game and displaying them on LEDs powered by an arduino.

## Setting up:
### Hardware
An arduino or arduino equivalent (ESP, etc) connected to a strip of individually addressable LEDs.
If you are interested in setting up an arduino powered LED strip for the first time, i reccomend this guide for starting out!
//i havent found a good guide yet

### Software
-SpinLED.exe
-SpinLED.dll
-BepInEx version 5.4.23.2 (x64 version) (https://github.com/BepInEx/BepInEx/releases) (called BepInEx_win_x64_5.4.23.2.zip)
-SpinCore.dll (https://github.com/Raoul1808/SpinCore)
-Arduino IDE (https://www.arduino.cc/en/software/)
-USB to UART bridge driver (https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers?tab=downloads) (You may or may not need this depending on which arduino you have. My ESP32 Board did)

## Installation Guide:
### Arduino
Using the arduino IDE, go to the libary manager and install FastLED by Daniel Garcia (version 3.10.3 or later). This is required for the arduino script to run. Afterwards, copy all of the text in Arduino.txt and paste it into the arduino IDE. At the very top of the scrip be sure to change the DATA_PIN to the data pin your arduino is using. Also change the NUM_LEDS to the exact amount of leds on your strip (any more or any less may result in glitches in the colors). IMPORTANT: BE SURE THE LED COUNT IN THIS SCRIPT MATCHES THE LED STRIP LENGTH ON SPINLED.EXE. You can also set the BAUD_RATE if you wish to, just be sure to again exactly match it in SpinLED.exe as well. Afer you change those values you can upload the script to your arduino.

### BepInEx
Download and extract the BepInEx folder into the games directory. While in the games directory, rename the file "UnityPlayer.dll" to "UnityPlayer_IL2CPP.dll". Then, rename the file "UnityPlayer_Mono.dll" to "UnityPlayer.dll". BepInEx will not run unless these changes are made. Launch Spin Rhythm and close it to generate the necessary folders for BepInEx. Go back into Spin Rhythms directory and find BepInEx --> Plugins. Drop SpinLEd.dll and SpinCore.dll in the plugins folder.

### Exe
If your arduino is plugged in but SpinLED is saying it is not a valid source you may need the USB to UART bridge driver. Download the "CP210x VCP windows driver" and follow the install process. Otherwise, this should work right out of the box!

After you have everything set up you only need to run SpinLED.exe to use it! And Spin Rhythm XD of course.
