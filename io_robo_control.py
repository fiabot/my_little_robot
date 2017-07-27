#control our pi robot using adafruit.io 

#imports 
import time 
from Adafruit_IO import MQTTClient
import Robot

# globals 
LEFT_TRIM   = -4
RIGHT_TRIM  = 0
ANGLE_MIN = -90 
ANGLE_MAX = 90 
THROTTLE_MAX = 255 
THROTTLE_MIN = -255

USERNAME = 'fiabot'
ADAFRUIT_IO_KEY = "07939487d2614d2482d79902f43486a9" #adafruit io key 
client = MQTTClient(USERNAME, ADAFRUIT_IO_KEY)

robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM) #define the robot
angle = 0 
throttle = 0 
on = True

def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO! ')
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe('turn_feed')
    client.subscribe('on_feed')
    client.subscribe('speed_feed')

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    
def message(client, feed_id, value):
    global angle,throttle,on
    print("new message from {} value is {}".format(feed_id,value))
    if feed_id == "turn_feed": 
        angle = value 
    elif feed_id == "speed_feed": 
        throttle = value 
        if throttle > THROTTLE_MAX: 
            throttle = THROTTLE_MAX 
        elif throttle < THROTTLE_MIN: 
            throttle = THROTTLE_MIN
    elif feed_id == "on_feed": 
        if value == "OFF": 
            on = False 
        elif value == "ON":
            on = True 
        
  

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
  
  print("moving motor {} left and {} right" .format(left_val,right_val))
  robot.move_gen(left_val,right_val,seconds)
  
# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

client.connect()

while True: 
    client.loop()
    #break out of loop if the toggle button is off 
    if not on: 
        print("robot turned off exiting out of program") 
        break
   
    #run robot 
    run_motor(angle, throttle)
    
    time.sleep(0.1)
  
