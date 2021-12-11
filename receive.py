import digitalio
import board
import time
import adafruit_rfm9x
import busio

'''
Setting up the pin allocations
RFM9x pins are:
CLK = GP2
MOSI = GP3
MISO = GP4
CS = GP6
Reset = GP7
'''

spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = digitalio.DigitalInOut(board.GP6)
reset = digitalio.DigitalInOut(board.GP7)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)

'''
defining the functions for the RFM9x and LED for a blink
This could be done in a library. Just remember to call the library in this code
'''

def try_read():
    return rfm9x.receive(timeout=1.0)

def rssi():
    return rfm9x.rssi

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

'''
This is where the magic happens, well its not really magic
the loop listens for a packet and then returns the payload
thre is no need to have a time.sleep() function as there is
sufficient delay in with the rfm9x.receive fuction()
'''

print("Waiting for packets...")
while True:
    led.value = not led.value
    packet = rfm9x.receive()
    packet_count = 0
    if packet is not None:
        #print("Received (raw payload): {0}".format(packet[4:]))
        print ("RSSI: {0}db".format(rfm9x.last_rssi))
        packet_text = str(packet, 'ascii')
        print('{0}'.format(packet_text))
        packet_count = packet_count + 1
