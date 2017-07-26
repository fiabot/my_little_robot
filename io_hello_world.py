# Simple example of sending and receiving values from Adafruit IO with the REST
# API client.
# Author: Tony DiCola

# Import Adafruit IO REST client.
from Adafruit_IO import Client

# Set to your Adafruit IO key.
ADAFRUIT_IO_KEY = "07939487d2614d2482d79902f43486a9"

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_KEY)


data = aio.receive('speed_feed')
print('Retrieved value from speed_feed has attributes: {0}'.format(data))
print('Latest value from speed_feed: {0}'.format(data.value))

on_data = aio.receive('on_feed') 
print("on_feed data" + str(on_data.value))

