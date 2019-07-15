print('test123456789')

# Python socket API for web server
try:
  import usocket as socket
except:
  import socket

# GPIO pins
from machine import Pin

# turn off vendor OS debugging messages
import esp
esp.osdebug(None)

# run of garbage collector
# - automatic memory management
# - save space in flash memory
import gc
gc.collect()

# access point
import network
ap = network.WLAN(network.AP_IF)
ap.config(essid="ColorSkate", password="12345678")
ap.active(True)
print('IP addres | netmask | gateway | DNS')
print(ap.ifconfig())

# ws2812b
import machine, neopixel
number_of_pixels = 10
rgb_pin = 6
