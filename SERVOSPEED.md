There's no two ways about it, this is a right pain, but if you don't do this, the mecanum wheels will not function properly.

The point of this is to get all 4 servos turning at the same speed.

The first job is to find the slowest servo

I use Thonny for this

create a new file servocal.py


	from time import sleep
	from otto_servo import Servos


	#SERVOS
	servos=Servos()
	LR = 0    #Left Rear
	RR = 1    #Right Rear
	LF = 2    #Left Front
	RF = 3    #Right Front


	servos.throttle(LR, .1)   
	sleep(2)   
	servos.throttle(LR, 0)
	
put a bit of tape on the left rear wheel so you can see how much it rotates 

run the file (make a note of how much it rotated)

edit the file, replacing LR with RR, move the tape to the right rear wheel

run the file (make a note of how much it rotated)

repeat for the front wheels

whichever rotated least is your slowest servo  

Now for the slowest servo adjust the sleep time until it rotates exactly 360 degrees (for my slowest servo this was 2.04 secs and it was LF)  
Now for each of the other servos, using the same amount of time (2.04 in my case) adjust the speed until the wheel rotated exactly 360 degrees 
and make a note of this speed.

here are some made up values to illustrate
```
Servo   |    speed     for 360 degrees forward rotation in 2.04 s
LR      |    0.0928        'LRF1'  (LR forward .1)
RR      |    0.09945       'RRF1' 
LF      |    0.1           'LFF1' 
RF      |    0.083         'RFF1' 
```
Now do it again using negative speeds to get a speed value for 360 degrees backwards in the same time
```
LR      |    -0.1189        'LRB1' 
RR      |    -0.128         'RRB1' 
LF      |    -0.113         'LFB1' 
RF      |    -0.1045        'RFB1' 
```
Now find the time for the slowest servo to rotate 360 degrees when the speed is 0.4 (0.615s in my case)  
Using that time setting, find the speeds for 360 degree rotation forward and backward for all the servos
giving us  LRF4, RRF4, LFF4,  RFF4,  LRB4,  RRB4, LFB4,  RFB4

Use these values to determine the calibration values to enter into the servo_speed() function in otto_servo.py

For your slowest servo, no values are required for forward movement so if that servo was LF
the calibration would be left as: `if (servo == self.LF): spd = spd * 1.0 + 0`

for all the others it's time to do some calculations  
that's 7 calculations where the general equation is  `spd = spd * M + C`

here's 2 examples

### FORWARD CORRECTIONS   (if spd > 0:)

for LR forward
```
M = (LRF4 - LRF1)/.3
C = LRF1 - (M * 0.1)
```
so if LRF4  was 0.352    and LRF1 was  0.0928
```
M = (0.352 - 0.0928)/.3
  = 0.2592/.3
  = 0.864

C = 0.0928 - (0.864 * 0.1)
  = 0.0928 - 0.0864
  = 0.0064
```  
so for spd > 0 the LR correction is
`if (servo == self.LR): spd = spd * 0.864 + 0.0064`

### BACKWARD CORRECTIONS   (if spd < 0:)

for RR backward  
if RRB4 =  -0.37   and   RRB1 = -0.128
```
M = (-0.37 - -0.128)/.3
  = -2.42/.3
  = -0.8067
  
C = -0.128 - (-0.8067 * 0.1)
  = -0.128 - -0.08067
  = -0.0473
```
the servo_speed() function in otto_servo.py already makes the speed negative so M becomes a positive number

so for spd < 0:
`if (servo == self.RR): spd = spd * 0.8067 -0.0473`

now edit otto_servo.py, find the servo_speed function and enter your correction values.
