import board
import digitalio
import time
import busio
import adafruit_bmp280
import adafruit_rfm9x
import adafruit_gps

# Setup GPS
uart = busio.UART(board.GP16, board.GP17, baudrate=9600, timeout=10)# set up uart
gps = adafruit_gps.GPS(uart, debug=False)#create gps module instance
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")#Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK220,1000")#set update rate (1second)
last_print = time.monotonic()

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
Setting up the gps
'''
gps = adafruit_gps.GPS(uart, debug=False)
gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')
last_print = time.monotonic()

'''
Define the pins for the RFM9x transmitter
CLK = GP2
MOSI = GP3
MISO = GP4
CS = GP6
Reset = GP7
Then define the parameters for sending the message payload
'''

spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
cs = digitalio.DigitalInOut(board.GP6)
reset = digitalio.DigitalInOut(board.GP7)
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0) # set the transmit frequency to 433MHz

def send(message):
    rfm9x.send(message)

while True:
    
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.monotonic()
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            continue
        # We have a fix! (gps.has_fix is true)
        
        sat_time = "{:02}:{:02}:{:02},".format(
                    gps.timestamp_utc.tm_hour,  
                    gps.timestamp_utc.tm_min,
                    gps.timestamp_utc.tm_sec,
                    )
        
        sat_date = "{}/{}/{},".format(
                    gps.timestamp_utc.tm_mon,
                    gps.timestamp_utc.tm_mday,
                    gps.timestamp_utc.tm_year,
                    )

        print("=" * 70)  # Print a separator line.
        
        #Define the payload strings
        Id = "CanSat Example,"
        temp = str("%.1f," % (bmp280.temperature))# + " C"
        pressure = str("%.0f," % (bmp280.pressure))# + " hPa"
        lat = str("%.4f," % (gps.latitude))
        long = str("%.4f," % (gps.longitude))
        gps_alt = str("%.1f," % (gps.altitude_m))
        sats = str("%.0f" % (gps.satellites))
        json_start = str("/*")
        json_end = str("*/")
    
        Payload = json_end + Id + sat_time + sat_date + temp + pressure + lat + long + gps_alt + sats + json_end # message payload string with json markers
        
        #Send the message payload
        rfm9x.send(Payload)
        print(Payload)# print it in the serial terminal for good measure
        
        led.value = not led.value #Flash the led after th payload is sent
        print("=" * 70)
