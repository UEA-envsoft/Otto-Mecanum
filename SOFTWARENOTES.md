### MicroPython

You will need to have set your wifi details in secrets.py  

Assuming all is well main.py will run on powerup.  
Otto will beep once to indicate main.py has started and he will grin.  
If you have kept the button on his head pressed he will then scroll his IP address, leaving the critical last 3 digits on display.

Otto will beep twice to indicate he has connected to wifi and is now awaiting a remote connection.
On successful connection he will beep 3 times, indicating he his raring to go.

If connection is lost he will beep twic, indicating that he is once again awaiting a remote connection.
