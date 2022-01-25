import board
import digitalio
import time
import busio
import adafruit_bmp280
import adafruit_rfm9x

#define the LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

'''
Set up the BMP280. Pins used are:
SCL = GP15
SDA = GP14
Then define the temperature, pressure and altitude
'''

i2c = busio.I2C(scl=board.GP15, sda=board.GP14)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)


def sat_temp():
    return bmp280_sensor.temperature

def sat_pressure():
    return bmp280_sensor.pressure
  
def sat_alt():
    return bmp280_sensor.altitude


'''
Set the local atmospheric pressure (QNH). This will be used to calculate the altitude. 
Note that sea level pressure can be your local pressure so a local weather report for that day will suffice.
Its important to note that the sensor only infers altitude for the pressure so it will have
inaccuracies.
'''
bmp280.sea_level_pressure = 1034

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


while True:

    led.value = not led.value
    #start = "/*"
    #stop = "*/"
    Id = "CanSat Example,"
    sat_time = str("%.0f," % (time.monotonic()))# + " s"
    temp = str("%.1f," % (bmp280.temperature))# + " C"
    pressure = str("%.0f," % (bmp280.pressure))# + " hPa"
    altitude = str("%.1f," % (bmp280.altitude))# + " meters"
    Payload = Id + sat_time + temp + pressure + altitude
    rfm9x.send(Payload)
    print(Payload)
    time.sleep(1)
