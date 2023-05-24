    """Servo class for 360 continuous servos
    Version:    0.0
    Author:     Alex Etchells (UEA-envsoft)
    License:    GNU GPL 3
    Copyright:  2023# 
    
            Derived from Pico Kitronik Simply Servos module SimplyServos.pyhttps://github.com/KitronikLtd/Kitronik-Pico-Simply-Servos-MicroPython/blob/main/Library%20Without%20PIO/SimplyServos.py

    defaults to 4 servos on pins 0 to 3
    has a throttle command for controlling continuous servo speed
    """
from machine import Pin, PWM

class Servos:
    #simply stops and starts the servo PIO, so the pin could be used for soemthing else.
    def registerServo(self, servo):
        self.servos[servo] = PWM(Pin(self.servoPins[servo]))
        self.servos[servo].freq(50)
        self.goToPosition(servo, 90) #equivalent of throttle 0

    def deregisterServo(self, servo):
        self.servos[servo].deinit()
 
    def scale(self, value, fromMin, fromMax, toMin, toMax):
        return toMin + ((value - fromMin) * ((toMax - toMin) / (fromMax - fromMin)))

    # goToPosition takes a degree position for the servo to goto. 
    # 0degrees->180 degrees is 0->2000us, plus offset of 500uS
    #1 degree ~ 11uS.
    #This function does the sum then calls goToPeriod to actually poke the PIO 
    def goToPosition(self, servo, degrees):
        if degrees < 0:
            degrees = 0
        if degrees > 180:
            degrees = 180
        scaledValue = self.scale(degrees, 0, 180, 1638, 8192)
        self.servos[servo].duty_u16(int(scaledValue))
    
    def goToPeriod(self, servo, period):
        if period < 500:
            period = 500
        if period > 2500:
            period = 2500
        scaledValue = self.scale(period, 500, 2500, 1638, 8192)
        self.servos[servo].duty_u16(int(scaledValue))

    #continuous servos take a throttle setting from -1 (O deg) to 1 (180 deg)
    def throttle(self, servo, speed):
        if speed < -1:
            speed = -1
        if speed > 1:
            speed = 1
        scaledValue = self.scale(speed, -1, 1, 1638, 8192)
        self.servos[servo].duty_u16(int(scaledValue))


    #Class initialisation
    def __init__(self, numberOfServos = 4):
        self.servoPins = [0,1,2,3]
        self.servos = [None for _ in range(numberOfServos)]
        #connect the servos by default on construction 
        for i in range(numberOfServos):
            self.registerServo(i)
      