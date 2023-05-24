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
print(ssid,password)
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

def servo_speed(servo, spd):
    #speed is -1 to 1
    #corrections for different servo speeds
    #YOU WILL NEED TO DETERMINE YOUR OWN VALUES
    #forward correction
    if spd > 0:
        if (servo == LF): spd = spd * 1.0
        if (servo == RF): spd = -spd * 1.0
        if (servo == RR): spd = -spd * 1.0

    #backward correction
    elif spd < 0:
        spd = spd * 1.0
        if (servo == LF): spd = spd * 1.0
        if (servo == RF): spd = -spd * 1.0
        if (servo == RR): spd = -spd * 1.0
    
    servos.throttle(servo,spd)

def stop():
    servos.throttle(LR, 0)
    servos.throttle(RR, 0)
    servos.throttle(LF, 0)
    servos.throttle(RF, 0)

def forward():
    servo_speed(LR, speed)
    servo_speed(RR, speed)
    servo_speed(LF, speed)
    servo_speed(RF, speed)

def backward():
    servo_speed(LR, -speed)
    servo_speed(RR, -speed)
    servo_speed(LF, -speed)
    servo_speed(RF, -speed)

def turn_left():
    servo_speed(LR, -speed)
    servo_speed(RR, speed)
    servo_speed(LF, -speed)
    servo_speed(RF, speed)

def turn_right():
    servo_speed(LR, speed)
    servo_speed(RR, -speed)
    servo_speed(LF, speed)
    servo_speed(RF, -speed)

def crab_left():
    print("CL")
    servo_speed(LR, speed)
    servo_speed(RR, -speed)
    servo_speed(LF, -speed)
    servo_speed(RF, speed)

def crab_right():
    print("CR")
    servo_speed(LR, -speed)
    servo_speed(RR, speed)
    servo_speed(LF, speed)
    servo_speed(RF, -speed)

def curve_left(biasPcent=20):
    servo_speed(LR, speed * (100 - biasPcent) / 100)
    servo_speed(RR, speed * (100 + biasPcent) / 100)
    servo_speed(LF, speed * (100 - biasPcent) / 100)
    servo_speed(RF, speed * (100 + biasPcent) / 100)

def curve_right(biasPcent=20):
    servo_speed(LR, speed * (100 + biasPcent) / 100)
    servo_speed(RR, speed * (100 - biasPcent) / 100)
    servo_speed(LF, speed * (100 + biasPcent) / 100)
    servo_speed(RF, speed * (100 - biasPcent) / 100)

def diag_left():
    servo_speed(LR, speed)
    servo_speed(RR, 0)
    servo_speed(LF, 0)
    servo_speed(RF, speed)

def diag_right():
    servo_speed(LR, 0)
    servo_speed(RR, speed)
    servo_speed(LF, speed)
    servo_speed(RF, 0)
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
    status = "CONN: 0"
    print(status)
    #Line following
    L = "W"
    if lf_left.read_u16() > 54000: L = "B"
    C = "W"
    if lf_centre.read_u16() > 54000: C = "B"
    R = "W"
    if lf_right.read_u16() > 54000: R = "B"
    status += "\nLFL: " + L +"\nLFC: " + C + "\nLFR: " + R
    print(status)
    #Distance
    status += "\nDT: 17" #+ str(get_distance())
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
    #led.matrixIp(str(ip))
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
                if request == "FW":
                    forward()
                elif request == "STP":
                    stop()
                elif request == "BK":
                    backward()
                elif request == "FL":
                    turn_left()
                elif request == "FR":
                    turn_right()
                elif request == "CL":
                    crab_left()
                elif request == "CR":
                    crab_right()
                elif request == "DL":
                    diag_left()
                elif request == "DR":
                    diag_right()
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
