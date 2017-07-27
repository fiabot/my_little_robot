#control our pi robot using adafruit.io 

#imports 
import time 
from Adafruit_IO import Client
import Robot

# globals 
LEFT_TRIM   = -4
RIGHT_TRIM  = 0
ANGLE_MIN = -90 
ANGLE_MAX = 90 
THROTTLE_MAX = 255 
THROTTLE_MIN = -255
ADAFRUIT_IO_KEY = "07939487d2614d2482d79902f43486a9" #adafruit io key 
aio = Client(ADAFRUIT_IO_KEY) #set up io client 
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM) #define the robot

#map value from left range to right range
def translate(value, min1, max1, min2, max2):
    # Figure out how 'wide' each range is
    max2 = int(max2) 
    min2 = int(min2)
    span1 = max1 - min1
    span2 = max2 - min2

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - min1) / float(span1)

    # Convert the 0-1 range into a value in the right range.
    return min2 + (valueScaled * span2)

  
def run_motor(angle,throttle,seconds = None): 
  global ANGLE_MIN, ANGLE_MAX,robot, THROTTLE_MAX,THROTTLE_MIN
  throttle = int(throttle)
  angle = int(angle)
  if angle < 0: 
    right_val = throttle 
    left_val = translate(angle, ANGLE_MIN,0,-throttle,throttle)
    left_val = int(left_val)
  elif angle >0: 
    left_val = throttle 
    right_val = translate(angle,0,ANGLE_MAX,-throttle,throttle)
    right_val = int(right_val)
  else: 
    left_val = throttle
    right_val = throttle 
    
  if left_val > THROTTLE_MAX or left_val < THROTTLE_MIN:
    print("left val is too high or low") 
    return
  elif right_val > THROTTLE_MAX or right_val < THROTTLE_MIN: 
    print("right val is too high or low") 
    return
  
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
    throttle= throttle_data.value
  
    if throttle > THROTTLE_MAX: 
        throttle = THROTTLE_MAX 
    elif throttle < THROTTLE_MIN: 
        throttle = THROTTLE_MIN
    
    #run robot 
    run_motor(angle_data.value, throttle_data.value)
  
