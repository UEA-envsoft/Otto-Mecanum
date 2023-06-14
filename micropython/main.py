    """
    Otto Mecanum Server

    Version:    0.0
    Author:     Alex Etchells (UEA-envsoft)
    License:    GNU GPL 3
    Copyright:  2023
    """

import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine
from otto_matrix import OttoMatrix
from otto_servo import Servos
from hcsr04 import HCSR04
import secrets

#WIFI
ssid = secrets.SSID
password = secrets.PASSWORD
#print(ssid,password)
#BUTTON
button = machine.Pin(16, mode=machine.Pin.IN)

#BUZZER
buzzer = machine.PWM(machine.Pin(15))
buzzer.freq(500)

#HCSR04
sonar = HCSR04(trigger_pin=9, echo_pin=8, echo_timeout_us=10000)

#LINE FOLLOWER
lf_left = machine.ADC(machine.Pin(28, mode=machine.Pin.IN))
lf_centre = machine.ADC(machine.Pin(27, mode=machine.Pin.IN))
lf_right = machine.ADC(machine.Pin(26, mode=machine.Pin.IN))

#LED MATRIX
# Create I2C object
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))
led = OttoMatrix(i2c)
led.set_brightness(1)
led.matrixGrin()

#IR PROXIMITY SENSORS
irl = machine.Pin(19, mode=machine.Pin.IN)
irr = machine.Pin(18, mode=machine.Pin.IN)

#SERVOS
servos=Servos()
servos.stop()
LR = 0
RR = 1
LF = 2
RF = 3
speed = 0.1

#****************** Sounds ********************************

def beep():
    buzzer.duty_u16(1000)
    sleep(0.2)
    buzzer.duty_u16(0)

beep()
    
def multi_beep(rpts):
    for i in range(rpts):
        beep()
        sleep(0.2)

#****************  Movement  ******************************
def set_speed(desired):
    global speed
    speed = desired
    print("new speed " + str(speed))
    
def obst_avoid(client):
    avoiding = True
    while avoiding:    
        #Distance
        dist = get_distance()
        status = "\nCONN: 0\nLF: F\nOB: T\nDT: " + str(dist)
        #Proximity
        prox = get_proximity()
        status += "\nIRL: " + str(prox[0]) + "\nIRR: " + str(prox[1])
        
        if prox[0] == 0 and prox[1] == 0: servos.backward(0.1)
        elif prox[0] == 0:
            if dist > 20: servos.curve_right(.1,70)
            else: servos.turn_right(.1)
        elif prox[1] == 0:
            if dist > 20: servos.curve_left(.1,70)
            else: servos.turn_left(.1)
        elif dist < 20: servos.turn_right(0.1)
        else: servos.forward(.1)
        print(status)    
        client.send(status)
        sleep(0.2)
        #print("BUTTON " + str(button.value()))
        if button.value() == 1:
            avoiding = False
            print(" stop obstacle avoid")
        servos.stop()
    
def line_follow(client):
    following = True
    while following:
        LCR=0x00
        L = "W"
        C = "W"
        R = "W"
        #print(str(lf_left.read_u16()) + "       " +  str(lf_centre.read_u16()) + "       " + str(lf_right.read_u16()) ) 
        if lf_left.read_u16() > 55000:
            LCR=(LCR | 4)
            L = "B"
        if lf_centre.read_u16() > 52000:
            LCR=(LCR | 2)
            C = "B"
        if lf_right.read_u16() > 55000:
            LCR=(LCR | 1)
            R = "B"
        print(LCR)
        #LCR = 0
        if LCR==2:
            servos.forward(.1)
        elif LCR==4:
            servos.turn_left(.1)
        elif LCR==6:
            servos.curve_left(.1,10)
        elif LCR==1:
            servos.turn_right(.1)
        elif LCR==3:
            servos.curve_right(.1,10)
        elif LCR==7 or LCR == 5:
            servos.forward(.1)
        elif LCR==0:
            servos.stop()
            
        status = "\nCONN: 0\nLF: T\nOB: F\nLFL: " + L +"\nLFC: " + C + "\nLFR: " + R
        print(status)    
        client.send(status)
        sleep(0.2)
        #print("BUTTON " + str(button.value()))
        if button.value() == 1:
            following = False
            print(" stop following")
        servos.stop()

#***************  End Movement  *************************
    
#***************   distance  ****************************
def get_distance():
    dist = sonar.distance_cm()
    print (dist)
    return int(dist)
#***************  End distance  *************************

#***************   proximity  ***************************
def get_proximity():
    left = irl.value()
    right = irr.value()
    return [left,right]
#***************  End proximity  ************************

#************Create status string  **********************
def status(command = "none"):
    #connected
    status = "CONN: 0\nLF: F\nOB: F"
    print(status)
    #Line following
    L = "W"
    if lf_left.read_u16() > 50000: L = "B"
    C = "W"
    if lf_centre.read_u16() > 50000: C = "B"
    R = "W"
    if lf_right.read_u16() > 50000: R = "B"
    status += "\nLFL: " + L +"\nLFC: " + C + "\nLFR: " + R
    print(status)
    #Distance
    status += "\nDT: " + str(get_distance())
    print(status)
    #Speed
    status += "\nSP: " + str(int(speed*10))
    print(status)
    #Proximity
    prox = get_proximity()
    status += "\nIRL: " + str(prox[0]) + "\nIRR: " + str(prox[1]) 
    print(status)
    #Commands
    status += "\nCMD: " + command +"\n"
    print(status)
    return status

#****************  WiFi Connection  ********************
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    if button.value() == 1:
        print("Displaying ip ")
        led.matrixIp(str(ip))
    return ip

def open_socket(ip):
    # Open a socket
    address = (ip, 8000)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection
    
#***************   SERVER   ********************
def serve(connection):
    #Start server
    while True:        
        #print("LF:    " + str(lf_left.read_u16()) + "     " + str(lf_centre.read_u16()) + "     " + str(lf_right.read_u16()) )
        #sleep(1)        
        print("Accepting connections")
        multi_beep(2)
        accepted = connection.accept()
        print("Connected by", accepted[1])
        client = accepted[0]
        connected = True
        multi_beep(3)
        while connected:
            try:                
                request = client.recv(1024)
                request = request.decode('utf-8')
                request = request.strip()
                print(request)
                if request == "OB":
                    obst_avoid(client)
                if request == "LF":
                    line_follow(client)
                if request == "FW":
                    servos.forward(speed)
                elif request == "STP":
                    servos.stop()
                elif request == "BK":
                    servos.backward(speed)
                elif request == "FL":
                    servos.turn_left(speed)
                elif request == "FR":
                    servos.turn_right(speed)
                elif request == "CL":
                    servos.crab_left(speed)
                elif request == "CR":
                    servos.crab_right(speed)
                elif request == "DL":
                    servos.diag_left(speed)
                elif request == "DR":
                    servos.diag_right(speed)
                elif request == "GRIN":
                    led.matrixGrin()
                elif request == "SURP":
                    led.matrixSurprise()
                elif request == "ANGR":
                    led.matrixAngry()
                elif request.find('SPD') > -1:
                    baz = request.split()
                    print(baz)
                    set_speed(int(baz[1])/10)
                reponse = status(request)
                print(reponse)
                client.send(reponse)
            except Exception:
                print("Exception")
                connected = False            
    
        print("Connection lost")
    client.close()
 
 

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()

