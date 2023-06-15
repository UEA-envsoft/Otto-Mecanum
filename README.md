# Otto-Mecanum
Code for the Otto Mecanum Bot

![otto mecanum](https://github.com/UEA-envsoft/Otto-Mecanum/assets/64538329/8e8d4ade-23fb-4242-af25-9b9f096500bb)

Otto Mecanum is a 3d printed robot with mecanum wheels.

STL files and assembly instructions are to be found on printables (https://www.printables.com/model/414218-otto-mecanum)

This repository contains the MicroPython files for the bot and the interface files for the RoboRemo control app for android.

Instructions for setting up a Pi Pico with MicroPython can be founed here: https://projects.raspberrypi.org/en/projects/get-started-pico-w/1

RoboRemo is a nifty, user customisable remote control application intended mainly
for electronics hobby projects. RoboRemo can connect via Bluetooth (RFCOMM /
BLE), Internet or WiFi (TCP, UDP), and USB (CDC-ACM, FTDI, CP210X,
CH340). I use the WiFi

Full app: https://play.google.com/store/apps/details?id=com.hardcodedjoy.roboremo  
RoboRemo.interface is the interface to be imported for control of Otto Mecanum  
![roboremo](https://github.com/UEA-envsoft/Otto-Mecanum/assets/64538329/1e45027b-f2e7-417d-82d1-171e073c5699)

Demo app: https://play.google.com/store/apps/details?id=com.hardcodedjoy.roboremofree  
The demo only allows 5 controls per page so control is distributed over several pages this control has the main functions but is incomplete.  

![roboremodemo0](https://github.com/UEA-envsoft/Otto-Mecanum/assets/64538329/6dbcda49-8df1-4b68-84f3-2db423dc2dad)
![roboremodemo1](https://github.com/UEA-envsoft/Otto-Mecanum/assets/64538329/a5363285-856e-4d50-a757-f0a0aa8bfda3)
![roboremodemo7](https://github.com/UEA-envsoft/Otto-Mecanum/assets/64538329/c1654da2-2b96-408c-9dcf-7b2fb011d3d9)

The files for the demo version are in the RoboRemoDemo Interface files directory.  
Import iface0 on the openning page. Then click the options page button. This button has 7 in brackets, indicating it will take you to page 7 so click the button to go to page 7 and then import iface7 for this page, keep on navigating and importing. Obviously a right faff to do this. I highly recommend paying  for the full version!

In either version the conneciton buttons need to be edited to contain the appropriate ip address for your bot.
You can view this by holding down the button when turning on and holding it until the ip addredd starts to scroll across the display. 
(Assuming you have added wireless connection info to secrets.py)

The project uses:  
ht16k33.mpy courtesy of smittytone https://github.com/smittytone/HT16K33-Python/tree/main/mpy  
hc-sr04.py courtesy of rsc1975 https://github.com/rsc1975/micropython-hcsr04/tree/master
