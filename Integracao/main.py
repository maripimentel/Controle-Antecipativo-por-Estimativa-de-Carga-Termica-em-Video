##Controle Antecipativo por Estimativa de Carga Termica em Video
##Codigo Principal
##Trabalho de Graduacao
##Versao 1
##Autores:
##    Alexandre Saran
##    Mariana Pimentel

# coding=utf-8

from peoplecounterlib import *
from sqlitelib import *
from controllerlib import *
import threading
import settings
import time
import datetime
import cv2

def data():
    global runEvent
	
    database = InicializeDatabase(str(timeHour))
    CreateTable(database)
    
    initialNumPeople = 2
    
    settings.initialNumPeople = initialNumPeople
    
    (tempMeetingRoom, humMeetingRoom, tempLara, tempExternal, doorSignal) = (0,0,0,0,0)
    
    while runEvent.is_set():
        numPeople = settings.cntUp-settings.cntDown + initialNumPeople
        print(TAG+'Numero de Pessoas: '+str(numPeople))

        # Calculates inicial time
        timestamp = time.time()
        dateTime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')
        
        # Read temperatura e humidity sensors
        for i in range (10):
            (readOk, tempMeetingRoom, humMeetingRoom, tempLara, tempExternal, doorSignal) = readTempHumDoor(tempMeetingRoom, humMeetingRoom, tempLara, tempExternal, doorSignal)
            if(readOk):
                break

        dutyCycle = settings.dutyCycle

        # Read compressor signal
        compressorSignal = settings.compressorSignal
        isOn = settings.isOn
        print(TAG+'Esta Ligado: '+str(isOn))

        InsertData(database, dateTime, tempMeetingRoom, humMeetingRoom, tempLara, tempExternal, doorSignal, numPeople, compressorSignal, isOn, dutyCycle)
        time.sleep(60)

def counter(timeHour, SAVE_RESULTS):
        try:
                PeopleCounter(0, 0, str(timeHour), SAVE_RESULTS)
        except KeyboardInterrupt:
                cv2.destroyAllWindows()

def controller():
    global runEvent
    lastOutput = 0
    cont = 1
    while runEvent.is_set():
        (lastOutput, cont) = Controller(lastOutput, cont)

SAVE_RESULTS = False

TAG = '(main) '

# Calculates inicial time
timestamp = time.time()
timeHour = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d_%H-%M-%S')

print(TAG+'data/hora: '+ str(timeHour))

settings.init()

runEvent = threading.Event()
runEvent.set()

threadPeopleCounter = threading.Thread(name='people_counter', target=counter, args = (str(timeHour), SAVE_RESULTS))
threadPeopleCounter.daemon = True
threadPeopleCounter.start()

threadPeopleData = threading.Thread(name='data', target=data)
threadPeopleData.start()

threadController = threading.Thread(name='controller', target=controller)
threadController.start()

try:
    while(True):
        time.sleep(0.3)
except KeyboardInterrupt:

    database = InicializeDatabase(str(timeHour))
    ReadTable(database)
    CloseTable(database)

    cv2.destroyAllWindows()

    runEvent.clear()
    threadPeopleCounter.join()
    threadPeopleData.join()
    threadController.join()
    
    writeRele(0, 30, "(controllerlib) ")

# print(TAG+'Final2: '+str(numberPeople))

print(TAG+'end')





