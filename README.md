# Otto-Mecanum
Code for the Otto Mecanum Bot

![otto mecanum](https://github.com/UEA-envsoft/Otto-Mecanum/assets/64538329/f07693c9-3b2d-406c-9f04-332b17b79140)

Otto Mecanum is a 3d printed robot with mecanum wheels.

STL files and assembly instructions are to be found on printables (once I complete the entry)

This repository contains the micropython files for the bot and the interface files for the RoboRemo control app for android

Full app: https://play.google.com/store/apps/details?id=com.hardcodedjoy.roboremo  
RoboRemo.interface is the interface to be imported for control of Otto Mecanum  

![roboremo](https://github.com/UEA-envsoft/Otto-Mecanum/assets/64538329/4c737496-a5fe-4d78-9130-7581383d2de8)


Demo app: https://play.google.com/store/apps/details?id=com.hardcodedjoy.roboremofree  
The demo only allows 5 controls per page so control is distributed over several pages this control has the main functions but is incomplete.  

![roboremodemo0](https://github.com/UEA-envsoft/Otto-Mecanum/assets/64538329/d63275af-f367-48ba-b293-68cb87f50113)
![roboremodemo1](https://github.com/UEA-envsoft/Otto-Mecanum/assets/64538329/aaa4ed88-9f64-4204-a95b-7061db2b3b8e)
![roboremodemo7](https://github.com/UEA-envsoft/Otto-Mecanum/assets/64538329/6f62d6f0-bd9f-4de4-8085-b163dc6b8667)

The files for the demo version are in the RoboRemoDemo Interface files directory.  
Import iface0 on the openning page. Then click the options page button. This button has 7 in brackets, indicating it will take you to page 7 so click the button to go to page 7 and then import iface7 for this page, keep on navigating and importing. Obviously a right faff to do this. I highly recommend paying  for the full version!

In either version the conneciton 1 and connection 2 buttons need to be edited to contain the appropriate ip address for your bot  

The project uses:  
ht16k33.mpy courtesy of smittytone https://github.com/smittytone/HT16K33-Python/tree/main/mpy  
hc-sr04.py courtesy of rsc1975 https://github.com/rsc1975/micropython-hcsr04/tree/master
