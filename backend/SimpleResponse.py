from itertools import cycle
from h11 import Data
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
def toon_sensorwaarde(data):
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


@socketio.on('F2B_verander_led')
def verander_kleur(data):
    global cyclus, prevColor
    actie = data['actie']
    # print(kleur)
    if cyclus == True:
        stop_rainbow()
        cyclus = False
    if actie == "rood":
        Led1.RGB_set(0, 100, 100)
        Led2.RGB_set(0, 100, 100)
        Led3.RGB_set(0, 100, 100)
        prevColor = "rood"
    elif actie == "groen":
        Led1.RGB_set(100, 0, 100)
        Led2.RGB_set(100, 0, 100)
        Led3.RGB_set(100, 0, 100)
        prevColor = "groen"
    elif actie == "blauw":
        Led1.RGB_set(100, 100, 0)
        Led2.RGB_set(100, 100, 0)
        Led3.RGB_set(100, 100, 0)
        prevColor = "blauw"
    elif actie == "cycle":
        cyclus = True
        prevColor = "cycle"
        print("start_rainbow")
        start_rainbow()
    elif actie == "aan":
        print("aan")
        print(prevColor)
        vorige_kleur()
    elif actie == "uit":
        Led1.RGB_set(100, 100, 100)
        Led2.RGB_set(100, 100, 100)
        Led3.RGB_set(100, 100, 100)


@socketio.on('F2B_verander_ventilator')
def verander_kleur(data):
    global motorpwm
    actie = data['actie']
    print(actie)
    if actie == "aan":
        motorpwm.ChangeDutyCycle(100)
    elif actie == "uit":
        motorpwm.ChangeDutyCycle(0)


@ socketio.on('F2B_verstuur_bericht')
def bericht_ontvangen(data):
    global berichtid, inhoud, status, reset, bericht, melding
    inhoud = str(data['berichtinhoud'])
    id = int(data['id'])
    print(inhoud)
    DataRepository.create_bericht(inhoud, id)
    bericht = DataRepository.read_id_laatste_bericht()
    berichtid = int(bericht[0]['max(berichtid)'])
    DataRepository.create_historiek_bij_bericht(
        10, berichtid, datum, "bericht ontvangen")
    status = 3
    melding = True
    reset = True


@ socketio.on('F2B_maak_gebruiker')
def maak_gebruiker(data):
    gebruiker = str(data['gebruikersnaam'])
    controle = DataRepository.read_user_by_naam(gebruiker)
    if(controle):
        print("Error: Gebruiker bestaat al!")
        emit('B2F_toon_error', {
            'error': "Error: Gebruiker bestaat al!"})
    else:
        DataRepository.create_user(gebruiker)
        emit('B2F_toon_succes', {
            'message': "Gebruiker toegevoegd. Dag ", "gebruiker": gebruiker})


@ socketio.on('F2B_login')
def log_in(data):
    gebruiker = str(data['gebruikersnaam'])
    controle = DataRepository.read_user_by_naam(gebruiker)
    id = int(controle['gebruikerid'])
    if(controle):
        emit('B2F_log_in_succes', {
            'id': id})
    else:
        emit('B2F_log_in_error', {
            'message': "Gebruiker bestaat niet, gelieve een gebruiker aan te maken."})


# lcd object
rs = 21
e = 20
lcdObject = lcdKlasse(rs, e, None, True)
licht = 0
GPIO.setmode(GPIO.BCM)
reset = False
status = 0
berichtid = 0

cyclus = False
prevColor = ""
# Joystickknop


def callback(knop):
    print("joystick")
    global status, reset
    if status == 3:
        status += 1
        lcdObject.send_instruction(0b00001111)
        reset = True
    elif status == 4:
        status = 3
        lcdObject.send_instruction(0b00001100)
        reset = True


def callback_knop(pin):
    global status, reset, tijd, lcdObject
    print("test")
    status += 1
    if status >= 2:
        status = 0
        tijd = "gggggggg"
        lcdObject.send_instruction(0b00001100)
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

rainbowTask = None

melding = False


class RainbowTask:

    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        rood = 0
        groen = 100
        blauw = 100
        while self._running:
            if rood == 0:
                while rood != 100 and cyclus == True:
                    time.sleep(0.2)
                    rood += 1
                    groen -= 1
                    Led1.RGB_set(rood, groen, blauw)
                    Led2.RGB_set(rood, groen, blauw)
                    Led3.RGB_set(rood, groen, blauw)
                time.sleep(2)
            elif groen == 0:
                while groen != 100 and cyclus == True:
                    time.sleep(0.2)
                    blauw -= 1
                    groen += 1
                    Led1.RGB_set(rood, groen, blauw)
                    Led2.RGB_set(rood, groen, blauw)
                    Led3.RGB_set(rood, groen, blauw)
                time.sleep(2)
            elif blauw == 0:
                while blauw != 100 and cyclus == True:
                    time.sleep(0.2)
                    rood -= 1
                    blauw += 1
                    Led1.RGB_set(rood, groen, blauw)
                    Led2.RGB_set(rood, groen, blauw)
                    Led3.RGB_set(rood, groen, blauw)
                time.sleep(2)
        # if cyclus == True:
        # stop_rainbow()
        # cyclus = False


def start_thread():
    print("**** Starting THREAD ****")
    thread = threading.Thread(target=programma, args=(), daemon=True)
    thread.start()


def start_rainbow():
    global rainbowTask
    print("**** Starting THREAD ****")
    rainbowTask = RainbowTask()
    thread = threading.Thread(target=rainbowTask.run, args=(), daemon=True)
    thread.start()


def stop_rainbow():
    global rainbowTask
    print("**** Stop THREAD ****")
    # thread = threading.Thread(target=rainbow, args=(), daemon=True)
    rainbowTask.terminate()


# def globale():
#     global start, minimum, maximum, tijd, ldrWaarde, reset, hysterese, resul, licht, datum


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


def vorige_kleur():
    global cyclus, prevColor
    print("karl")
    print(prevColor)
    if prevColor == "rood":
        Led1.RGB_set(0, 100, 100)
        Led2.RGB_set(0, 100, 100)
    elif prevColor == "groen":
        Led1.RGB_set(100, 0, 100)
        Led2.RGB_set(100, 0, 100)
        Led3.RGB_set(100, 0, 100)
    elif prevColor == "blauw":
        Led1.RGB_set(100, 100, 0)
        Led2.RGB_set(100, 100, 0)
        Led3.RGB_set(100, 100, 0)
    elif prevColor == "cycle":
        cyclus = True
        print("start_rainbow")
        start_rainbow()
    elif prevColor == "":
        Led1.RGB_set(0, 0, 0)
        Led2.RGB_set(0, 0, 0)
        Led3.RGB_set(0, 0, 0)


def setup():
    global motorpwm
    lcdObject.setup()
    lcdObject.init_LCD()

    Led1.RGB_set(100, 100, 100)
    Led2.RGB_set(100, 100, 100)
    Led3.RGB_set(100, 100, 100)
    motor = 25
    GPIO.setup(motor, GPIO.OUT)
    motorpwm = GPIO.PWM(motor, 1000)
    motorpwm.start(0)
    motorpwm.ChangeDutyCycle(0)


def programma():
    global start, minimum, maximum, tijd, ldrWaarde, reset, hysterese, resul, licht, datum, melding
    lcdObject.reset_lcd()
    while True:
        # datum + tijd
        cur_time = time.strftime("%H:%M:%S")
        nu = datetime.now()
        datum = nu.strftime("%Y-%m-%d %H:%M:%S")

        # Joystick waardes inlezen
        xWaarde = joystickX.readChannel(0)
        yWaarde = joystickY.readChannel(1)
        # print(str(xWaarde) + " " + str(yWaarde))

        # ldr uitlezen
        resultaat = ldr.readChannel(2)
        if(resultaat < minimum):
            minimum = resultaat
        elif(resultaat > maximum):
            maximum = resultaat
        if(maximum != minimum):
            licht = 100-(100*((resultaat-minimum)/(maximum-minimum)))
        # print("Ldr waarde: ", str(round(licht, 2)), " %")

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
            # DataRepository.create_historiek(
            #     1, 1, datum, round(resul, 2), "Temp inlezen")

            # DataRepository.create_historiek(
            #     2, 2, datum, round(licht, 2), "Ldr inlezen")

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
            # DataRepository.create_historiek(
            #     1, 1, datum, round(resul, 2), "Temp inlezen")
            # DataRepository.create_historiek(
            #     2, 2, datum, round(licht, 2), "Ldr inlezen")

        # print(difference)

        if reset == True:
            print("reset")
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
            # print(abs(hysterese))
        elif status == 1:
            # lcdObject.reset_cursor()
            lcdObject.eerste_rij()
            lcdObject.send_message(adressen[0])
            lcdObject.tweede_rij()
            lcdObject.send_message(adressen[1])
        elif status == 3:
            lcdObject.eerste_rij()
            lcdObject.send_message(inhoud)
            if melding == True:
                Led1.RGB_set(0, 100, 100)
                Led2.RGB_set(0, 100, 100)
                Led3.RGB_set(0, 100, 100)
                time.sleep(0.2)
                Led1.RGB_set(100, 100, 100)
                Led2.RGB_set(100, 100, 100)
                Led3.RGB_set(100, 100, 100)
                time.sleep(0.2)
                Led1.RGB_set(0, 100, 100)
                Led2.RGB_set(0, 100, 100)
                Led3.RGB_set(0, 100, 100)
                time.sleep(0.2)
                Led1.RGB_set(100, 100, 100)
                Led2.RGB_set(100, 100, 100)
                Led3.RGB_set(100, 100, 100)
                time.sleep(0.2)
                Led1.RGB_set(0, 100, 100)
                Led2.RGB_set(0, 100, 100)
                Led3.RGB_set(0, 100, 100)
                time.sleep(0.2)
                Led1.RGB_set(100, 100, 100)
                Led2.RGB_set(100, 100, 100)
                Led3.RGB_set(100, 100, 100)
                time.sleep(0.2)
                Led1.RGB_set(100, 100, 100)
                Led2.RGB_set(100, 100, 100)
                Led3.RGB_set(100, 100, 100)
                time.sleep(1)
                vorige_kleur()
                melding = False
        elif status == 4:
            lcdObject.tweede_rij()
            lcdObject.set_cursor(0x40)
            lcdObject.send_message("Nee")
            lcdObject.set_cursor(0x49)
            lcdObject.send_message("Ja")
        # print(status)


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
