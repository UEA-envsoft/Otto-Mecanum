# Otto-Mecanum
Code for the Otto Mecanum Bot

Otto Mecanum is a 3d printed robot with mecanum wheels.

STL files and assembly instructions are to be found on printables (once I complete the entry)

This repository contains the micropython files for the bot and the interface files for the RoboRemo control app for android

Full app: https://play.google.com/store/apps/details?id=com.hardcodedjoy.roboremo  
RoboRemo.interface is the interface to be imported for control of Otto Mecanum

Demo app: https://play.google.com/store/apps/details?id=com.hardcodedjoy.roboremofree  
The demo only allows 5 controls per page so control is distributed over several pages this control has the main functions but is incomplete.  
The files for the demo version are in the RoboRemoDemo Interface files directory.  
Import iface0 on the openning page. Then click the options page button. This button has 7 in brackets, indicating it will take you to page 7 so click the button to go to page 7 and then import iface7 for this page, keep on navigating and importing. Obviously a right faff to do this. I highly recommend paying  for the full version!


The project uses:  
ht16k33.mpy courtesy of smittytone https://github.com/smittytone/HT16K33-Python/tree/main/mpy  
hc-sr04.py courtesy of rsc1975 https://github.com/rsc1975/micropython-hcsr04/tree/master
