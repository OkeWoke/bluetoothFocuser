# A bluetooth controlled motor driver for the Meade Zero Image Shift Electronic Micro-Focuser #07080

The Meade Focuser is typically plugged into an LX200 or simillar mount which handles the driving of this focuser, 
however moving to a new mount that lacks this makes the focuser uncontrollable. There are solutions from JMI, however this is a DIY solution.

The setup involves an HC-05/06? bluetooth module, an arduino nano and an L293D motor driving chip.
The speed is controllable through 4 pre set options, done via pwm. 

## Arduino.ino 
This is the program written for the arduino. 

##GUI.py 
This is a python client that allows you to control the focuser. 

##Todo:
Fix handshake/reconnection
Make a mobile phone app client to control the focuser.
