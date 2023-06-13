    """Servo class for 360 continuous servos for Otto Mecanum
    Version:    0.0
    Author:     Alex Etchells (UEA-envsoft)
    License:    GNU GPL 3
    Copyright:  2023# 
    
            Derived from Pico Kitronik Simply Servos module SimplyServos.pyhttps://github.com/KitronikLtd/Kitronik-Pico-Simply-Servos-MicroPython/blob/main/Library%20Without%20PIO/SimplyServos.py

    defaults to 4 servos on pins 0 to 3
    has a throttle command for controlling continuous servo speed and a bunch of specific movements
    servo_speed() function allows for calibration of individual servos
    """
class Servos:
    
    LR = 0    #left rear wheel
    RR = 1    #right rear wheel
    LF = 2    #left front wheel
    RF = 3    #right front wheel
    
    def setThrottles(self,lr,rr,lf,rf):    
        print("set throttles " + str(lr) + " " + str(rr) + " " + str(lf) + " " + str(rf)  )    
        self.servo_speed(self.LR, lr)
        self.servo_speed(self.RR, rr)
        self.servo_speed(self.LF, lf)
        self.servo_speed(self.RF, rf)

    def servo_speed(self,servo, spd):
        #speed is -1 to 1
        #corrections for different servo speeds
        #corrections were determined at speeds 0.1, 0.4, -0.1 and -0.4 and then extrapolated
        #(RHS motors are reversed)
        if (servo == self.RF or servo == self.RR): spd = -spd
        
        #forward correction 
        if spd > 0:
            if (servo == self.LF): spd = spd * 1.0 + 0
            if (servo == self.LR): spd = spd * 1.0 + 0
            if (servo == self.RF): spd = spd * 1.0 + 0
            if (servo == self.RR): spd = spd * 1.0 + 0

        #backward correction 
        elif spd < 0:
            if (servo == self.LF): spd = spd * 1.0 - 0
            if (servo == self.LR): spd = spd * 1.0 - 0
            if (servo == self.RF): spd = spd * 1.0 - 0
            if (servo == self.RR): spd = spd * 1.0 - 0
        
        self.throttle(servo,spd)   
    
    def stop(self):
        self.setThrottles(0,0,0, 0)

    def forward(self,speed):
        print("fwd")
        self.setThrottles(speed, speed, speed, speed)

    def backward(self,speed):
        self.setThrottles(-speed, -speed, -speed, -speed)

    def turn_left(self,speed):
        self.setThrottles(-speed, speed, -speed, speed)

    def turn_right(self,speed):
        self.setThrottles(speed, -speed, speed, -speed)

    def crab_left(self,speed):
        self.setThrottles(speed, -speed, -speed, speed)

    def crab_right(self,speed):
        self.setThrottles(-speed, speed, speed, -speed)

    def curve_left(self,speed, biasPcent=20):
        self.setThrottles(speed * (100 - biasPcent) / 100, speed * (100 + biasPcent) / 100, speed * (100 - biasPcent) / 100, speed * (100 + biasPcent) / 100)

    def curve_right(self,speed, biasPcent=20):
        self.setThrottles(speed * (100 + biasPcent) / 100, speed * (100 - biasPcent) / 100, speed * (100 + biasPcent) / 100, speed * (100 - biasPcent) / 100)

    def diag_left(self,speed):
        self.setThrottles(speed, 0, 0, speed)

    def diag_right(self,speed):
        self.setThrottles(0, speed, speed, 0)
    
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
      
