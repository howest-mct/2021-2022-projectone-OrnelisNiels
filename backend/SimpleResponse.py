from h11 import Data
from numpy import diff
from helpers.lcdKlasse import lcdKlasse
from helpers.klasseKnop import Button
from helpers.spiKlasse import SpiClass
from helpers.rgbKlasse import RGB

import spidev
from RPi import GPIO
import time
from datetime import datetime

from subprocess import check_output

# fullstack
import threading

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify
from repositories.DataRepository import DataRepository

from selenium import webdriver

# Code voor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)

# API ENDPOINTS


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    status = DataRepository.read_device()
    emit('B2F_device', {'device': status}, broadcast=True)
    emit('B2F_temperatuur_uitlezen', {'temperatuur': round(resul, 2)})
    emit('B2F_licht_uitlezen', {'licht': round(licht, 2)})


@socketio.on('F2B_toon_sensorwaarde')
def switch_light(data):
    # Ophalen van de data
    id = data['knopid']
    print(id)
    if id == "1":
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
        emit('B2F_temperatuur_uitlezen', {
            'temperatuur': round(resul, 2)})
    elif id == "2":
        emit('B2F_licht_uitlezen', {
            'licht': round(licht, 2)})

    # lcd object
rs = 21
e = 20
lcdObject = lcdKlasse(rs, e, None, True)
licht = 0
GPIO.setmode(GPIO.BCM)
reset = False
status = 0


# Joystickknop
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
hysterese = 0

# Rgb leds
Led1 = RGB(5, 6, 13)
Led2 = RGB(22, 23, 24)
Led3 = RGB(12, 16, 19)

# andere variabelen
start = True
minimum = 1023
maximum = 0
#  controle variabelen
tijd = "gggggggg"
ldrWaarde = "gggggg"


# fullstack
def start_thread():
    print("**** Starting THREAD ****")
    thread = threading.Thread(target=programma, args=(), daemon=True)
    thread.start()


def start_chrome_kiosk():
    import os

    os.environ['DISPLAY'] = ':0.0'
    options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--kiosk')
    # chrome_options.add_argument('--no-sandbox')
    # options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost")
    while True:
        pass


def start_chrome_thread():
    print("**** Starting CHROME ****")
    chromeThread = threading.Thread(
        target=start_chrome_kiosk, args=(), daemon=True)
    chromeThread.start()


def setup():
    lcdObject.setup()
    lcdObject.init_LCD()

    Led1.RGB_set(0, 100, 100)
    Led2.RGB_set(100, 0, 100)
    Led3.RGB_set(100, 100, 0)


def programma():
    global start, minimum, maximum, tijd, ldrWaarde, reset, hysterese, resul, licht
    lcdObject.reset_lcd()
    while True:
        # datum + tijd
        cur_time = time.strftime("%H:%M:%S")
        nu = datetime.now()
        datum = nu.strftime("%Y-%m-%d %H:%M:%S")

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
            socketio.emit('B2F_temperatuur_uitlezen', {
                          'temperatuur': round(resul, 2)})
            socketio.emit('B2F_licht_uitlezen', {
                          'licht': round(licht, 2)})
            DataRepository.create_historiek(
                1, 1, datum, round(resul, 2), "Temp inlezen")

            DataRepository.create_historiek(
                2, 2, datum, round(licht, 2), "Ldr inlezen")

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
            socketio.emit('B2F_temperatuur_uitlezen', {
                          'temperatuur': round(resul, 2)})
            socketio.emit('B2F_licht_uitlezen', {
                          'licht': round(licht, 2)})
            DataRepository.create_historiek(
                1, 1, datum, round(resul, 2), "Temp inlezen")
            DataRepository.create_historiek(
                2, 2, datum, round(licht, 2), "Ldr inlezen")

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
            # licht op lcd
            hysterese = licht - hysterese
            if abs(hysterese) > 1.5:
                lcdObject.set_cursor(0x40)
                lcdObject.send_message(f"{licht:.2f}%")
                if licht < 100:
                    lcdObject.set_cursor(0x46)
                    lcdObject.send_message("  ")

                if licht < 10:
                    lcdObject.set_cursor(0x45)
                    lcdObject.send_message("  ")
                hysterese = licht
            print(abs(hysterese))
        elif status == 1:
            # lcdObject.reset_cursor()
            lcdObject.eerste_rij()
            lcdObject.send_message(adressen[0])
            lcdObject.tweede_rij()
            lcdObject.send_message(adressen[1])


if __name__ == '__main__':
    try:
        setup()
        start_thread()
        # start_chrome_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')
    except KeyboardInterrupt as ex:
        print(ex)
    finally:
        lcdObject.reset_lcd()
        print('\n Script is ten einde, cleanup is klaar')
        # lcdObject.reset_cursor()
        GPIO.cleanup()
