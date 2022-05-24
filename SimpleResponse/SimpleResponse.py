from lcdKlasse import lcdKlasse
from klasseKnop import Button
from spiKlasse import SpiClass

import spidev
from RPi import GPIO
import time

from subprocess import check_output

# lcd object
rs = 21
e = 20
lcdObject = lcdKlasse(rs, e, None, True)

GPIO.setmode(GPIO.BCM)


# Knop
def callback(knop):
    print("test")


knop = Button(25)
knop.on_press(callback)

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

# Temperatuursensor LM35
LM35 = SpiClass(0, 2)

try:
    lcdObject.setup()
    lcdObject.init_LCD()
    while True:
        # woord = input("Geef een woord: ")
        # # tekst()
        # # cursor().
        # # send_character(65)
        # lcdObject.send_message(woord)
        lcdObject.reset_cursor()
        lcdObject.eerste_rij()
        lcdObject.send_message(adressen[0])
        lcdObject.tweede_rij()
        lcdObject.send_message(adressen[1])
        # time.sleep(1)

        # Joystick waardes inlezen
        xWaarde = joystickX.readChannel(0)
        yWaarde = joystickY.readChannel(1)
        LM35_waarde = LM35.readChannel(2)
        spanning = (LM35_waarde / 1023.0 * 5)
        temperatuur = spanning / 0.01
        # print(str(xWaarde) + " " + str(yWaarde))
        print(str(temperatuur))

except Exception as ex:
    print(ex)
finally:
    # lcdObject.reset_lcd()
    print('\n Script is ten einde, cleanup is klaar')
    # lcdObject.reset_cursor()
    GPIO.cleanup()
