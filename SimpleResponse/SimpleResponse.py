from lcdKlasse import lcdKlasse
from klasseKnop import Button
from spiKlasse import SpiClass
from rgbKlasse import RGB

import spidev
from RPi import GPIO
import time

from subprocess import check_output

global resul
global test

# lcd object
rs = 21
e = 20
lcdObject = lcdKlasse(rs, e, None, True)
test = 0
GPIO.setmode(GPIO.BCM)

status = 0


# Knop
def callback(knop):
    print("test")


def callback_knop(pin):
    global status
    if knop.pressed:
        lcdObject.reset_lcd()
        status += 1
        if status >= 2:
            status = 0
        print("Status: " + str(status))


knop = Button(27)
knop.on_press(callback_knop)

# IP inlezen en decoderen
ips = check_output(['hostname', '--all-ip-addresses'])
ip = ips.decode()
adressen = ip.split()


# Joystick
knopJoystick = Button(17)
knopJoystick.on_press(callback)
joystickX = SpiClass(0, 0)
joystickY = SpiClass(0, 1)

# One wire
sensor_file_name = '/sys/bus/w1/devices/28-01883800007d/w1_slave'

# Ldr
ldr = SpiClass(0, 2)

# Rgb leds
Led1 = RGB(5, 6, 13)
Led2 = RGB(22, 23, 24)
Led3 = RGB(12, 16, 19)
try:
    lcdObject.setup()
    lcdObject.init_LCD()
    start = True
    minimum = 1023
    maximum = 0
    Led1.RGB_set(0, 100, 100)
    Led2.RGB_set(100, 0, 100)
    Led3.RGB_set(100, 100, 0)
    while True:
        tijd = time.strftime("%H:%M:%S")
        # time.sleep(1)

        # Joystick waardes inlezen
        xWaarde = joystickX.readChannel(0)
        yWaarde = joystickY.readChannel(1)
        print(str(xWaarde) + " " + str(yWaarde))

        # ldr uitlezen
        resultaat = ldr.readChannel(2)
        if(resultaat < minimum):
            minimum = resultaat
        elif(resultaat > maximum):
            maximum = resultaat
        if(maximum != minimum):
            test = 100-(100*((resultaat-minimum)/(maximum-minimum)))
        print("Ldr waarde: ", str(round(test, 2)), " %")

        # One wire uitlezen
        if start == True:
            begintijd = time.time()
            sensor_file = open(sensor_file_name, 'r')
            lijn = sensor_file.readline()
            lijn = sensor_file.readline()
            found = lijn.find("=")
            resul = float(lijn[found + 1::])
            resul = resul/1000
            if resul > 30:
                resul = 30
            if resul < 10:
                resul = 10
            print(f"De temp is {resul:.2f} ° Celcius")
            start = False

        eindtijd = time.time()
        difference = int(eindtijd)-(begintijd)
        if difference > 60:
            sensor_file = open(sensor_file_name, 'r')
            lijn = sensor_file.readline()
            lijn = sensor_file.readline()
            found = lijn.find("=")
            resul = float(lijn[found + 1::])
            resul = resul/1000
            if resul > 30:
                resul = 30
            if resul < 10:
                resul = 10
            print(f"De temp is {resul:.2f} ° Celcius")
            begintijd = time.time()

        if status == 0:
            lcdObject.reset_cursor()
            lcdObject.eerste_rij()
            lcdObject.set_cursor(4)
            lcdObject.send_message(tijd)
            lcdObject.tweede_rij()
            lcdObject.send_message(f"{resul:.2f}ßC")
            lcdObject.set_cursor(0x4A)
            lcdObject.send_message(str(round(test, 2))+"%")
        elif status == 1:
            lcdObject.reset_cursor()
            lcdObject.eerste_rij()
            lcdObject.send_message(adressen[0])
            lcdObject.tweede_rij()
            lcdObject.send_message(adressen[1])
except Exception as ex:
    print(ex)
finally:
    lcdObject.reset_lcd()
    print('\n Script is ten einde, cleanup is klaar')
    # lcdObject.reset_cursor()
    GPIO.cleanup()
