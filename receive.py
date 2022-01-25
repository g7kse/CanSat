import digitalio
import board
import time
import adafruit_rfm9x
import busio
import math

spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = digitalio.DigitalInOut(board.GP6)
reset = digitalio.DigitalInOut(board.GP7)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)


def try_read():
    return rfm9x.receive(timeout=1.0)

def rssi():
    return rfm9x.rssi

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print("Waiting for packets...")

while True:
    led.value = not led.value
    packet = rfm9x.receive()
    quality = (rssi()+ 100)*2
    packet_count = 0
    if packet is not None:
        packet_text = str(packet, 'ascii')
        print ("/*" + '{0}'.format(packet_text),('{0}'.format(quality)) + "*/")
        packet_count = packet_count + 1
