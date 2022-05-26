from ast import While
from lcdKlasse import lcdKlasse
from klasseKnop import Button
from RPi import GPIO
import time
from subprocess import check_output


rs = 21
e = 20
lcdObject = lcdKlasse(rs, e, None, True)
test = 0
GPIO.setmode(GPIO.BCM)


def callback_knop(pin):
    global status
    global reset
    global lcdObject
    print("test")
    status += 1
    if status >= 2:
        status = 0
    reset = True
    print("Status: " + str(status))


reset = False
status = 0
knop = Button(27)
knop.on_press(callback_knop)

ips = check_output(['hostname', '--all-ip-addresses'])
ip = ips.decode()
adressen = ip.split()

try:
    lcdObject.setup()
    lcdObject.init_LCD()
    while True:
        if reset == True:
            print("testje")
            lcdObject.reset_lcd()
            reset = False
        if status == 0:
            lcdObject.reset_cursor()
            lcdObject.eerste_rij()
            lcdObject.set_cursor(4)
            lcdObject.send_message("karl")
            lcdObject.tweede_rij()
            lcdObject.set_cursor(0x44)
            lcdObject.send_message("is lekker")
        elif status == 1:
            lcdObject.reset_cursor()
            lcdObject.eerste_rij()
            lcdObject.send_message(adressen[0])
            lcdObject.tweede_rij()
            lcdObject.send_message(adressen[1])
except KeyboardInterrupt as ex:
    print(ex)
finally:
    lcdObject.reset_lcd()
    GPIO.cleanup()
    print("end of code")
