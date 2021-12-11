import board
import digitalio
import time
import radio
import busio
import adafruit_rfm9x

#define the LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

'''
Set up the BMP280. Pins usd are:
SCL = GP15
SDA = GP14

Then define the temperature, pressure and altitude
'''
i2c = busio.I2C(scl=board.GP15, sda=board.GP14, frequency=440000)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

def read_temperature():
    return bmp280_sensor.temperature

def read_pressure():
    return bmp280_sensor.pressure
  
def read_altitude():
    return bmp280_sensor.altitude

'''
Set the local atmospheric pressure (QNH). This will be used to calculate the altitude. 
Note that sea level pressure can be your local pressure so a local weather report for that day will suffice.
Its important to note that the sensor only infers altitude for the pressure so it will have
inaccuracies.
'''
sensor.sea_level_pressure = 1013.25

'''
deinine the pins for the RFM9x transmitter
CLK = GP2
MOSI = GP3
MISO = GP4
CS = GP6
Reset = GP7

Then define the paramters for sending the message payload
'''
  
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = digitalio.DigitalInOut(board.GP6)
reset = digitalio.DigitalInOut(board.GP7)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)

def send(message):
    rfm9x.send(message)
    
'''
This bit now send the data
'''

print("RFM9x radio ready")
while True:
    led.value = not led.value
    radio.send(bmp280_sensor.temperature, bmp280_sensor.pressure, bmp280_sensor.altitude)
    print("Radio message sent")
    time.sleep(1)
