#control our pi robot using adafruit.io 

#imports 
import time 
from Adafruit_IO import Client
import Robot

# globals 
LEFT_TRIM   = 0
RIGHT_TRIM  = 0
ANGLE_MIN = -90 
ANGLE_MAX = 90 
THROTTLE_MAX = 255 
THROTTLE_MIN = -255
ADAFRUIT_IO_KEY = "07939487d2614d2482d79902f43486a9" #adafruit io key 
aio = Client(ADAFRUIT_IO_KEY) #set up io client 
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM) #define the robot

#map value from left range to right range
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

  
def run_motor(angle,throttle,seconds = None): 
  global ANGLE_MIN, ANGLE_MAX,robot
  
  if angle < 0: 
    right_val = throttle 
    left_val = translate(angle, ANGLE_MIN,ANGLE_MAX,-throttle,throttle)
  elif angle >0: 
    left_val = throttle 
    right_val = translate(angle,ANGLE_MIN,ANGLE_MAX,-throttle,throttle) 
  else: 
    left_val = throttle
    right_val = throttle 
  
  robot.move_gen(left_val,right_val,seconds)
  
   

while True: 
  
    #break out of loop if the toggle button is off 
    on_data = aio.receive("on_feed") 
    if on_data.value == "OFF": 
        break 
  
    #get angle from io
    angle_data = aio.receive("turn_feed") 
  
    #get throttle data 
    throttle_data = aio.receive("speed_feed") 
  
    if throttle_data.value > THROTTLE_MAX: 
        throttle_data.value = THROTTLE_MAX 
    elif throttle_data.value < THROTTLE_MIN: 
        thrott_data.value = THROTTLE_MIN
    
    #run robot 
    run_motor(angle_data.value, throttle_data.value,0.1)
  
