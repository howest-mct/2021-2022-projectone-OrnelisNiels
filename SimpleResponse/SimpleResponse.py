from numpy import diff
from lcdKlasse import lcdKlasse
from klasseKnop import Button
from spiKlasse import SpiClass
from rgbKlasse import RGB

import spidev
from RPi import GPIO
import time

from subprocess import check_output

global resul
global licht

# lcd object
rs = 21
e = 20
lcdObject = lcdKlasse(rs, e, None, True)
licht = 0
GPIO.setmode(GPIO.BCM)
reset = False
status = 0


# Knop
def callback(knop):
    print("test")


def callback_knop(pin):
    global status
    global reset
    global tijd
    global lcdObject
    print("test")
    status += 1
    if status >= 2:
        status = 0
        tijd = "gggggggg"
    reset = True
    print("Status: " + str(status))


status = 0
knop = Button(27)
knop.on_press(callback_knop)

# IP inlezen en decoderen
ips = check_output(['hostname', '--all-ip-addresses'])
ip = ips.decode()
adressen = ip.split()
print(adressen)


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

    # controle variabelen
    tijd = "gggggggg"
    ldrWaarde = "gggggg"
    while True:
        cur_time = time.strftime("%H:%M:%S")

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
            licht = 100-(100*((resultaat-minimum)/(maximum-minimum)))
        print("Ldr waarde: ", str(round(licht, 2)), " %")

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

        print(difference)

        if reset == True:
            print("testje")
            lcdObject.reset_lcd()
            reset = False

        if status == 0:
            # lcdObject.reset_cursor()
            # lcdObject.send_message(a)
            if tijd != cur_time:
                positie = 0
                for (a, b) in zip(cur_time, tijd):
                    if a != b:
                        lcdObject.set_cursor(4+positie)
                        lcdObject.send_message(a)
                    positie += 1
                tijd = cur_time
            lcdObject.set_cursor(0x49)
            lcdObject.send_message(f"{resul:.2f}ßC")
            lcdObject.set_cursor(0x40)
            lcdObject.send_message(f"{licht:.2f}%")
            if licht < 100:
                lcdObject.set_cursor(0x46)
                lcdObject.send_message("  ")

            if licht < 10:
                lcdObject.set_cursor(0x45)
                lcdObject.send_message("  ")
        elif status == 1:
            # lcdObject.reset_cursor()
            lcdObject.eerste_rij()
            lcdObject.send_message(adressen[0])
            lcdObject.tweede_rij()
            lcdObject.send_message(adressen[1])
except KeyboardInterrupt as ex:
    print(ex)
finally:
    lcdObject.reset_lcd()
    print('\n Script is ten einde, cleanup is klaar')
    # lcdObject.reset_cursor()
    GPIO.cleanup()
