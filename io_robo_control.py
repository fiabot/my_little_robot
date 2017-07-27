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
def translate(value, x_min, x_max, y_min, y_max):
    
    #find slope
    m = (y_max-y_min) / (x_max - x_min) 
    
    #solve for b
    b = y_min - (m*x_min)
    
    #get new value 
    new_value = m*value + b 
    
    #return new_valie 
    return new_value


  
def run_motor(angle,throttle,seconds = None): 
  global ANGLE_MIN, ANGLE_MAX,robot, THROTTLE_MAX,THROTTLE_MIN
  throttle = int(throttle)
  angle = int(angle)

  if angle < 0: 
    right_val = throttle 
    left_val = translate(angle, ANGLE_MIN,0,-throttle,throttle)
    print(" before left_val" + str(left_val))
    left_val = int(left_val)

  elif angle >0: 
    left_val = throttle 
    right_val = translate(angle, 0,ANGLE_MAX,-throttle,throttle)
    right_val = int(-right_val)
    
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
        print("turned robot off, exiting program") 
        break 
  
    #get angle from io
    angle_data = aio.receive("turn_feed") 
    
    #get throttle data 
    #throttle_data = aio.receive("speed_feed") 
    #throttle= throttle_data.value
    throttle = 5
  
    if throttle > THROTTLE_MAX: 
        throttle = THROTTLE_MAX 
    elif throttle < THROTTLE_MIN: 
        throttle = THROTTLE_MIN
    
    #run robot 
    run_motor(angle_data.value, throttle)
    
    time.sleep(1)
  
