# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony DiCola

# Import Adafruit IO REST client.
from Adafruit_IO import Client
import time

# Set to your Adafruit IO key.
ADAFRUIT_IO_KEY = "07939487d2614d2482d79902f43486a9"

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_KEY)

on_data = aio.receive('on_feed') 
if on_data.value == "ON": 
  while True:
    data = aio.receive('speed_feed')
    print('Latest value from speed_feed: {0}'.format(data.value))
    on_data = aio.receive('on_feed') 
    if on_data.value == "OFF": 
      break
    time.sleep(1)




