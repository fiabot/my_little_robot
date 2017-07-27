#control our pi robot using adafruit.io 

#imports 
import time 
from Adafruit_IO import Client
import Robot

# globals 
LEFT_TRIM   = 0
RIGHT_TRIM  = 0
ADAFRUIT_IO_KEY = "07939487d2614d2482d79902f43486a9" #adafruit io key 
aio = Client(ADAFRUIT_IO_KEY) #set up io client 
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM) #define the robot


while True: 
  
  #break out of loop if the toggle button is off 
  on_data = aio.receive("on_feed") 
  if on_data.value == "OFF": 
    break 
