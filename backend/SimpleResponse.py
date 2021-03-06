from helpers.lcdKlasse import lcdKlasse
from helpers.klasseKnop import Button
from helpers.spiKlasse import SpiClass
from helpers.rgbKlasse import RGB

import os
import sys
import spidev
from RPi import GPIO
import time
from datetime import datetime

from subprocess import check_output

# fullstack
import threading

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from repositories.DataRepository import DataRepository

from selenium import webdriver

time.sleep(15)
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


@app.route('/api/v1/historiek/temp/all/')
def get_historiek_temp_all():
    if request.method == "GET":
        data = DataRepository.read_historiek_temp()
        if data is not None:
            return jsonify(historiek=data), 200
        else:
            return jsonify(message="error"), 404


@app.route('/api/v1/historiek/temp/dag/')
def get_historiek_temp_dag():
    if request.method == "GET":
        data = DataRepository.read_historiek_temp_dag()
        if data is not None:
            return jsonify(historiek=data), 200
        else:
            return jsonify(message="error"), 404


@app.route('/api/v1/historiek/temp/week/')
def get_historiek_temp_week():
    if request.method == "GET":
        data = DataRepository.read_historiek_temp_week()
        if data is not None:
            return jsonify(historiek=data), 200
        else:
            return jsonify(message="error"), 404


@app.route('/api/v1/historiek/berichten/all/')
def get_historiek_berichten_all():
    if request.method == "GET":
        data = DataRepository.read_historiek_berichten()
        if data is not None:
            return jsonify(historiek=data), 200
        else:
            return jsonify(message="error"), 404


@app.route('/api/v1/historiek/berichten/week/')
def get_historiek_berichten_week():
    if request.method == "GET":
        data = DataRepository.read_historiek_berichten_week()
        if data is not None:
            return jsonify(historiek=data), 200
        else:
            return jsonify(message="error"), 404


@app.route('/api/v1/berichten/<id>/')
def get_berichten_by_id(id):
    if request.method == "GET":
        # data = DataRepository.read_berichten_by_id(id, 9, id, 9)
        datum = DataRepository.read_berichtdatum_historiek(id, 1, id, 1)
        if datum is not None:
            return jsonify(berichten=datum), 200
        else:
            return jsonify(message="error"), 404


@app.route('/api/v1/quickReplies/')
def get_quickReplies():
    if request.method == "GET":
        replies = DataRepository.read_quickReplies()
        if datum is not None:
            return jsonify(quickreplies=replies), 200
        else:
            return jsonify(message="error"), 404


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    global var, gewensteTemp, globalStat, globalStatled
    # # Send to the client!
    # vraag de status op van de lampen uit de DB
    status = DataRepository.read_device()
    emit('B2F_device', {'device': status}, broadcast=True)
    emit('B2F_temperatuur_uitlezen', {'temperatuur': round(resul, 2)})
    emit('B2F_licht_uitlezen', {'licht': round(licht, 2)})
    emit('B2F_verander_tempHtml', {'gewTemp': var})
    emit('B2F_verander_status_vent', {'status': globalStat})
    emit('B2F_verander_status_leds', {'status': globalStatled})


@socketio.on('F2B_gebruiker')
def initial_connection(data):
    global gebruikersid
    id = data['gebruiker']
    controle = DataRepository.read_gebruikers_by_id(id)
    gebruikersid = id
    if controle:
        emit('B2F_bestaande_gebruiker', {'message': "bestaand"})
    else:
        emit('B2F_bestaande_gebruiker', {'message': "niet-bestaand"})


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
        print(f"De temp is {resul:.2f} ?? Celcius")
        emit('B2F_temperatuur_uitlezen', {
            'temperatuur': round(resul, 2)})
    elif id == "2":
        emit('B2F_licht_uitlezen', {
            'licht': round(licht, 2)})


@socketio.on('F2B_verander_led')
def verander_kleur(data):
    global cyclus, prevColor, globalStatled, auto, isAan
    actie = data['actie']
    print(actie)
    if cyclus == True:
        stop_rainbow()
        cyclus = False
    if actie == "rood":
        socketio.emit('B2F_verander_status_leds', {'status': 1})
        globalStatled = 1
        Led1.RGB_set(0, 100, 100)
        Led2.RGB_set(0, 100, 100)
        Led3.RGB_set(0, 100, 100)
        prevColor = "rood"
        isAan = True
    elif actie == "groen":
        socketio.emit('B2F_verander_status_leds', {'status': 1})
        Led1.RGB_set(100, 0, 100)
        Led2.RGB_set(100, 0, 100)
        Led3.RGB_set(100, 0, 100)
        prevColor = "groen"
        isAan = True
    elif actie == "blauw":
        socketio.emit('B2F_verander_status_leds', {'status': 1})
        globalStatled = 1
        Led1.RGB_set(100, 100, 0)
        Led2.RGB_set(100, 100, 0)
        Led3.RGB_set(100, 100, 0)
        prevColor = "blauw"
        isAan = True
    elif actie == "cycle":
        auto = False
        socketio.emit('B2F_verander_status_leds', {'status': 1})
        globalStatled = 1
        cyclus = True
        prevColor = "cycle"
        print("start_rainbow")
        start_rainbow()
    elif actie == "aan":
        socketio.emit('B2F_verander_status_leds', {'status': 1})
        globalStatled = 1
        DataRepository.create_historiek(4, 4, datum, actie, "Leds aan")
        print("aan")
        print(prevColor)
        auto = False
        isAan = True
        vorige_kleur()
    elif actie == "uit":
        socketio.emit('B2F_verander_status_leds', {'status': 0})
        globalStatled = 0
        DataRepository.create_historiek(4, 5, datum, actie, "Leds uit")
        Led1.RGB_set(100, 100, 100)
        Led2.RGB_set(100, 100, 100)
        Led3.RGB_set(100, 100, 100)
        isAan = False
    elif actie == "auto":
        print("autooooo")
        isAan = True
        auto = True
        DataRepository.create_historiek(
            4, 13, datum, actie, "Leds automatisch")
    if actie != "aan" or "uit":
        DataRepository.create_historiek(
            4, 6, datum, actie, "Ledkleur veranderen")


@socketio.on('F2B_shutdown')
def shutdownPi():
    callback_shutdown(18)


@socketio.on('F2B_verander_ventilator')
def verander_ventilator(data):
    global motorpwm, gewensteTemp, draaien, controleVentilator, var
    print(data)
    actie = data['actie']
    if actie == "aan":
        controleVentilator = "manueel"
        draaien = True
        DataRepository.create_historiek(
            9, 7, datum, actie, "Ventilator aan")
        # motorpwm.start(0)
        # motorpwm.ChangeDutyCycle(100)
        socketio.emit('B2F_verander_tempHtml', {'gewTemp': -1})
        var = -1

    elif actie == "uitt":
        controleVentilator = "manueel"
        draaien = False
        DataRepository.create_historiek(
            9, 8, datum, actie, "Ventilator uit")
        # motorpwm.ChangeDutyCycle(0)
        # motorpwm.stop()
        socketio.emit('B2F_verander_tempHtml', {'gewTemp': -1})
        var = -1


@socketio.on('F2B_verander_ventilatorAuto')
def verander_ventilatorAuto(data):
    print(data)
    actie = data['actie']
    global gewensteTemp, draaien, controleVentilator, var
    gewensteTemp = float(data['temp'])
    controleVentilator = ""
    socketio.emit('B2F_verander_tempHtml', {'gewTemp': gewensteTemp})
    var = gewensteTemp
    DataRepository.create_historiek(
        9, 12, datum, actie, "Ventilator auto")


@socketio.on('F2B_verstuur_bericht')
def bericht_ontvangen(data):
    global berichtid, inhoud, status, reset, bericht, melding
    inhoud = str(data['berichtinhoud'])
    id = int(data['id'])
    controleGebruiker = DataRepository.read_gebruikers_by_id(id)
    print("test")
    if controleGebruiker:
        print("controle geslaagd")
        DataRepository.create_bericht(inhoud, id, 1)
        bericht = DataRepository.read_id_laatste_bericht()
        berichtid = int(bericht[0]['max(berichtid)'])
        DataRepository.create_historiek_bij_bericht(
            10, berichtid, datum, "bericht ontvangen")
        berichten = DataRepository.read_berichten_by_id(id, 1, id, 1)
        # print(berichten)
        historiekdatum = DataRepository.read_berichtdatum_historiek(
            id, 1, id, 1)
        print(historiekdatum)
        socketio.emit('B2F_refreshBerichtenChart')
        # emit('B2F_toon_berichten', {
        #  'berichten': berichten, "datum": historiekdatum})
        socketio.emit('B2F_nieuw_bericht')
        status = 3
        if len(inhoud) > 16:
            melding = True
        # reset = True
    else:
        print("Controle niet geslaagd")


@ socketio.on('F2B_maak_gebruiker')
def maak_gebruiker(data):
    gebruiker = str(data['gebruikersnaam'])
    controle = DataRepository.read_user_by_naam(gebruiker)
    if(controle):
        print("Error: Gebruiker bestaat al!")
        emit('B2F_toon_error', {
            'error': "Error: Gebruiker bestaat al!"})
    else:
        if gebruiker != "" and len(gebruiker) <= 15:
            DataRepository.create_user(gebruiker)
            user = DataRepository.read_user_by_naam(gebruiker)
            id = int(user['gebruikerid'])
            emit('B2F_toon_succes', {
                'message': "Gebruiker toegevoegd. Dag ", "gebruiker": gebruiker, "id": id})
        else:
            emit('B2F_toon_error', {
                'error': "Error: Gebruiker moet een naam hebben en mag niet leeg zijn! (max 15 characters)"})


@ socketio.on('F2B_login')
def log_in(data):
    gebruiker = str(data['gebruikersnaam'])
    controle = DataRepository.read_user_by_naam(gebruiker)
    if(controle):
        id = int(controle['gebruikerid'])
        emit('B2F_log_in_succes', {
            'id': id})
    else:
        emit('B2F_log_in_error')


@socketio.on('F2B_verander_quickReplies')
def quickReplies(data, data2, data3, data4):
    optie1 = data[0]['inhoud']
    optie2 = data2[0]['inhoud']
    optie3 = data3[0]['inhoud']
    optie4 = data4[0]['inhoud']
    current = DataRepository.read_quickReplies()
    currentOptie1 = current[0]['berichtinhoud']
    currentOptie2 = current[1]['berichtinhoud']
    currentOptie3 = current[2]['berichtinhoud']
    currentOptie4 = current[3]['berichtinhoud']

    if currentOptie1 != optie1:
        if optie1 != "":
            DataRepository.update_quickReplies(optie1, 1)
            emit('B2F_gewijzigd')
    if currentOptie2 != optie2:
        if optie2 != "":
            DataRepository.update_quickReplies(optie2, 2)
            emit('B2F_gewijzigd')
    if currentOptie3 != optie3:
        if optie3 != "":
            DataRepository.update_quickReplies(optie3, 3)
            emit('B2F_gewijzigd')
    if currentOptie4 != optie4:
        if optie4 != "":
            DataRepository.update_quickReplies(optie4, 4)
            emit('B2F_gewijzigd')


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
    global status, reset, vorigeOpties, optie, tijd, positieTeller, lcdTeller, vorigeOptie
    vorigeOpties = ""
    vorigeOptie = ""
    lcdTeller = 0x0
    if status == 3:
        lcdObject.send_instruction(0b00001111)
        positieTeller = 0
        lcdTeller = 0x0
        status += 1
        # reset = True
    elif status == 4:
        lcdObject.send_instruction(0b00001100)
        vorigeOpties = ""
        vorigeOptie = ""
        status += 1
        # reset = True
    elif status == 5:
        status = 0
        tijd = "gggggggg"
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


def callback_shutdown(pin):
    global lcdObject, motorpwm, status
    status = -1
    print("shutdown")
    lcdObject.reset_lcd()
    lcdObject.reset_cursor()
    time.sleep(0.5)
    lcdObject.send_message("Afsluiten")
    motorpwm.stop()
    time.sleep(2)
    # os.system("sudo shutdown -h now")
    # sys.exit()
    lcdObject.reset_lcd()
    check_output(["sudo", "shutdown", "-h", "now"])


knop = Button(27)
knop.on_press(callback_knop)

shutdownknop = Button(18)
shutdownknop.on_press(callback_shutdown)

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

gewensteTemp = 1000
draaien = False
controleVentilator = ""
stat = 0
vorigeStat = 0
var = 0
globalStat = 0
vorigeAdressen = ""
vorigeOpties = ""
opties = []
lcdTeller = 0x0
positieTeller = 0
joyTimer = 0
vorigeJoyTimer = 0
optie = ""
vorigeOptie = ""
gebruikersid = 0
vorigeInhoud = ""
auto = False
isAan = False


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
    global cyclus, prevColor, globalStatled
    globalStatled = 1
    if isAan == True:
        if prevColor == "rood":
            Led1.RGB_set(0, 100, 100)
            Led2.RGB_set(0, 100, 100)
            Led3.RGB_set(0, 100, 100)
            socketio.emit('B2F_verander_status_leds', {'status': 1})
        elif prevColor == "groen":
            Led1.RGB_set(100, 0, 100)
            Led2.RGB_set(100, 0, 100)
            Led3.RGB_set(100, 0, 100)
            socketio.emit('B2F_verander_status_leds', {'status': 1})

        elif prevColor == "blauw":
            Led1.RGB_set(100, 100, 0)
            Led2.RGB_set(100, 100, 0)
            Led3.RGB_set(100, 100, 0)
            socketio.emit('B2F_verander_status_leds', {'status': 1})
        elif prevColor == "cycle":
            cyclus = True
            print("start_rainbow")
            start_rainbow()
        elif prevColor == "":
            Led1.RGB_set(0, 100, 100)
            Led2.RGB_set(0, 100, 100)
            Led3.RGB_set(0, 100, 100)
            socketio.emit('B2F_verander_status_leds', {'status': 1})
    else:
        Led1.RGB_set(100, 100, 100)
        Led2.RGB_set(100, 100, 100)
        Led3.RGB_set(100, 100, 100)
        socketio.emit('B2F_verander_status_leds', {'status': 0})


def setup():
    global motorpwm
    lcdObject.setup()
    lcdObject.init_LCD()

    Led1.RGB_set(100, 100, 100)
    Led2.RGB_set(100, 100, 100)
    Led3.RGB_set(100, 100, 100)
    motor = 25
    GPIO.setup(motor, GPIO.OUT)
    motorpwm = GPIO.PWM(motor, 100)
    motorpwm.start(0)
    print("setup")


def programma():
    global start, minimum, auto, motorpwm, maximum, gebruikersid, tijd, vorigeInhoud, ldrWaarde, reset, hysterese, resul, licht, datum, melding, gewensteTemp, draaien, controleVentilator, stat, vorigeStat, globalStat, vorigeAdressen, vorigeOpties, opties, lcdTeller, positieTeller, joyTimer, vorigeJoyTimer, optie, vorigeOptie
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
        if auto == True:
            if licht < 20:
                vorige_kleur()
            elif licht > 30:
                Led1.RGB_set(100, 100, 100)
                Led2.RGB_set(100, 100, 100)
                Led3.RGB_set(100, 100, 100)
                socketio.emit('B2F_verander_status_leds', {'status': 0})

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
            print(f"De temp is {resul:.2f} ?? Celcius")
            start = False
            socketio.emit('B2F_temperatuur_uitlezen', {
                          'temperatuur': round(resul, 2)})
            socketio.emit('B2F_licht_uitlezen', {
                          'licht': round(licht, 2)})
            DataRepository.create_historiek(
                1, 1, datum, round(resul, 2), "Temp inlezen")

            DataRepository.create_historiek(
                2, 2, datum, round(licht, 2), "Ldr inlezen")
            socketio.emit('B2F_refresh_chart')

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
            print(f"De temp is {resul:.2f} ?? Celcius")
            begintijd = time.time()
            socketio.emit('B2F_temperatuur_uitlezen', {
                          'temperatuur': round(resul, 2)})
            socketio.emit('B2F_licht_uitlezen', {
                          'licht': round(licht, 2)})
            DataRepository.create_historiek(
                1, 1, datum, round(resul, 2), "Temp inlezen")
            DataRepository.create_historiek(
                2, 2, datum, round(licht, 2), "Ldr inlezen")
            print("emit")
            socketio.emit('B2F_refresh_chart')
            if status == 0:
                lcdObject.init_LCD()
                lcdObject.set_cursor(0xC)
                lcdObject.send_message("    ")
                lcdObject.set_cursor(0x48)
                lcdObject.send_message(" ")

        # Ventilator besturen
        if controleVentilator == "manueel":
            if draaien == True:
                stat = 1
                if vorigeStat != stat:
                    socketio.emit('B2F_verander_status_vent', {'status': 1})
                    vorigeStat = stat
                    globalStat = 1
                # motorpwm.start(0)
                motorpwm.ChangeDutyCycle(100)
            elif draaien == False:
                stat = 0
                if vorigeStat != stat:
                    socketio.emit('B2F_verander_status_vent', {'status': 0})
                    vorigeStat = stat
                    globalStat = 0
                motorpwm.ChangeDutyCycle(0)
                # motorpwm.stop(0)
        elif controleVentilator == "":
            if resul > gewensteTemp:
                stat = 1
                if vorigeStat != stat:
                    socketio.emit('B2F_verander_status_vent', {'status': 1})
                    vorigeStat = stat
                    globalStat = 1
                # motorpwm.start(0)
                motorpwm.ChangeDutyCycle(100)
            elif resul <= gewensteTemp:
                stat = 0
                if vorigeStat != stat:
                    socketio.emit('B2F_verander_status_vent', {'status': 0})
                    vorigeStat = stat
                    globalStat = 0
                motorpwm.ChangeDutyCycle(0)
                # motorpwm.stop(0)

        if reset == True:
            print("reset")
            lcdObject.reset_lcd()
            reset = False

        if status == 0:
            # lcdObject.reset_cursor()
            # lcdObject.send_message(a)
            tijd = "gggggggg"
            if tijd != cur_time:
                positie = 0
                for (a, b) in zip(cur_time, tijd):
                    if a != b:
                        lcdObject.set_cursor(4+positie)
                        lcdObject.send_message(a)
                    positie += 1
                tijd = cur_time
            lcdObject.set_cursor(0x49)
            lcdObject.send_message(f"{resul:.2f}??C")
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
                lcdObject.init_LCD()
                lcdObject.set_cursor(0xC)
                lcdObject.send_message("    ")
                lcdObject.set_cursor(0x48)
                lcdObject.send_message(" ")
            # print(abs(hysterese))
        elif status == 1:
            # lcdObject.reset_cursor()
            # if vorigeAdressen != adressen and status == 1:
            # print("vorige")
            lcdObject.eerste_rij()
            lcdObject.send_message(adressen[0])
            lcdObject.tweede_rij()
            lcdObject.send_message(adressen[1])
            vorigeAdressen = adressen

        elif status == 3:
            lcdObject.send_instruction(0b00001111)
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
                print(prevColor)
                vorige_kleur()
                melding = False
            if inhoud != vorigeInhoud:
                melding = True
                gebruiker = DataRepository.read_gebruikers_by_id(gebruikersid)
                gebruikernaam = (gebruiker[0]["naam"])
                lcdObject.reset_lcd()
                lcdObject.eerste_rij()
                lcdObject.send_message(f"{gebruikernaam}:")
                lcdObject.tweede_rij()
                if len(inhoud) > 16:
                    lcdObject.send_message(inhoud[0:16])
                    interval = len(inhoud) - 16
                    time.sleep(1)

                    for i in range(interval):
                        i = i + 1
                        positieTeller += 1
                        lcdObject.tweede_rij()
                        lcdObject.send_message(inhoud[i:16+i])
                        print(inhoud[i+1:16+i+1])
                        time.sleep(0.1)
                        print(i)
                    positieTeller = len(inhoud)
                else:
                    lcdObject.send_message(inhoud)
                vorigeInhoud = inhoud
            joyTimer = time.time()
            # print(xWaarde)
            print(f"positieteller: {positieTeller}")
            print(len(inhoud))
            if xWaarde <= 50:
                if joyTimer - vorigeJoyTimer > 0.1:
                    positieTeller += 1
                    vorigeJoyTimer = joyTimer
                    if positieTeller > len(inhoud):
                        positieTeller = len(inhoud)
                    lcdObject.tweede_rij()
                    lcdObject.send_message(
                        inhoud[positieTeller-16:positieTeller])
            elif xWaarde > 700:
                if joyTimer - vorigeJoyTimer > 0.1:
                    positieTeller -= 1
                    vorigeJoyTimer = joyTimer
                    if positieTeller < 16:
                        positieTeller = 16
                lcdObject.tweede_rij()
                lcdObject.send_message(
                    inhoud[positieTeller-16:positieTeller])
            # print(inhoud[positieTeller:16+positieTeller])
        elif status == 4:
            lcdObject.send_instruction(0b00001111)
            print(f"positieteller: {positieTeller}")
            replies = DataRepository.read_quickReplies()
            opties = [f"{replies[0]['berichtinhoud']}", f"{replies[1]['berichtinhoud']}",
                      f"{replies[2]['berichtinhoud']}", f"{replies[3]['berichtinhoud']}"]

            # opties schrijven
            if vorigeOpties != opties:
                lcdObject.reset_lcd()
                lcdObject.send_message(opties[0])
                if (len(opties[1]) == 2):
                    lcdObject.set_cursor(0xE)
                elif (len(opties[1]) == 3):
                    lcdObject.set_cursor(0xD)
                elif (len(opties[1]) == 4):
                    lcdObject.set_cursor(0xC)
                lcdObject.send_message(opties[1])
                lcdObject.tweede_rij()
                lcdObject.send_message(opties[2])
                if (len(opties[3]) == 2):
                    lcdObject.set_cursor(0x4E)
                elif (len(opties[3]) == 3):
                    lcdObject.set_cursor(0x4D)
                elif (len(opties[3]) == 4):
                    lcdObject.set_cursor(0x4C)
                lcdObject.send_message(opties[3])
                lcdObject.set_cursor(lcdTeller)
                vorigeOpties = opties

            # positie bepalen
            joyTimer = time.time()
            if xWaarde <= 50:
                if joyTimer - vorigeJoyTimer > 0.5:
                    positieTeller += 1
                    vorigeJoyTimer = joyTimer
                    if positieTeller > 3:
                        positieTeller = 0
                        lcdTeller = 0x0
            elif xWaarde >= 700:
                if joyTimer - vorigeJoyTimer > 0.5:
                    positieTeller -= 1
                    vorigeJoyTimer = joyTimer
                    if positieTeller == -1:
                        positieTeller = 3
                        lcdTeller = 0x40
                    if positieTeller == 0:
                        lcdTeller = 0x0
                    elif positieTeller == 1:
                        lcdTeller = 0x0
                    elif positieTeller == 2:
                        lcdTeller = 0x40
                    elif positieTeller == 3:
                        lcdTeller = 0x40
            if yWaarde <= 500:
                if joyTimer - vorigeJoyTimer > 0.5:
                    positieTeller += 2
                    vorigeJoyTimer = joyTimer
                    if positieTeller == 2:
                        lcdTeller = 0x40
                    elif positieTeller == 3:
                        lcdTeller = 0x40
                    elif positieTeller == 4:
                        positieTeller = 2
                    elif positieTeller == 5:
                        positieTeller = 3

            elif yWaarde >= 700:
                if joyTimer - vorigeJoyTimer > 0.5:
                    positieTeller -= 2
                    vorigeJoyTimer = joyTimer
                    if positieTeller == 0:
                        lcdTeller = 0x0
                    elif positieTeller == 1:
                        lcdTeller = 0x0
                    elif positieTeller < 0:
                        positieTeller = 0
                    elif positieTeller < 1:
                        positieTeller = 1

            if lcdTeller == 0x0 and positieTeller == 0:
                lcdObject.set_cursor(lcdTeller)
                optie = opties[0]
            elif lcdTeller == 0x0 and positieTeller == 1:
                lengteOptie4 = len(opties[0])
                # print(lengteOptie4)
                lengteOptie3 = len(opties[1])
                # print(lengteOptie3)
                lengteTussen = 16 - lengteOptie3 - lengteOptie4
                lcdTeller = lcdTeller + lengteOptie4 + lengteTussen
                lcdObject.set_cursor(lcdTeller)
                optie = opties[1]
            elif lcdTeller > 0x0 and positieTeller == 2:
                lcdTeller = 0x40
                lcdObject.set_cursor(lcdTeller)
                optie = opties[2]
            elif lcdTeller == 0x40 and positieTeller == 3:
                lengteOptie1 = len(opties[2])
                lengteOptie2 = len(opties[3])
                lengteTussen = 16 - lengteOptie2 - lengteOptie1
                lcdTeller = lcdTeller + lengteOptie1 + lengteTussen
                lcdObject.set_cursor(lcdTeller)
                optie = opties[3]

        elif status == 5:
            if vorigeOptie != optie:
                lcdObject.reset_lcd()
                print("hallo")
                lcdObject.eerste_rij()
                lcdObject.send_message(f"U verstuurde:")
                lcdObject.tweede_rij()
                lcdObject.send_message(optie)
                DataRepository.create_bericht(optie, 1, gebruikersid)
                bericht = DataRepository.read_id_laatste_bericht()
                berichtid = int(bericht[0]['max(berichtid)'])
                DataRepository.create_historiek_bij_bericht(
                    10, berichtid, datum, "bericht verstuurd")
                socketio.emit('B2F_refreshBerichtenChart')
                vorigeOptie = optie
                vorigeInhoud = ""
                socketio.emit('B2F_nieuw_bericht')
                positieTeller = 0
        # print(gebruikersid)


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
        motorpwm.stop()
        print('\n Script is ten einde, cleanup is klaar')
        # lcdObject.reset_cursor()
        GPIO.cleanup()
