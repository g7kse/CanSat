import digitalio
import board
import time
import adafruit_rfm9x
import busio
import math

'''
Define the pins for the RFM9x receiver
CLK = GP2
MOSI = GP3
MISO = GP4
CS = GP6
Reset = GP7
'''
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = digitalio.DigitalInOut(board.GP6)
reset = digitalio.DigitalInOut(board.GP7)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0) # set the receive frequency to 433MHz

def try_read():
    return rfm9x.receive(timeout=1.0)

def rssi():
    return rfm9x.rssi
'''
Blink the light as a watchdog to show that the programme is running
'''

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print("Waiting for packets...")

while True:
    led.value = not led.value
    packet = rfm9x.receive()
    quality = (rssi()+ 100)*2 # a crude way of having a relative and positive value for the Serial Studio dashboard
    packet_count = 0
    if packet is not None:
        packet_text = str(packet, 'ascii')
        print ("/*" + '{0}'.format(packet_text),('{0}'.format(quality)) + "*/") # format the data as a frame that can be read in Serial Studio
        packet_count = packet_count + 1
