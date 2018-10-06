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
import threading
import settings
import time
import datetime
import cv2

def data():
	global runEvent
	
	database = InicializeDatabase(str(timeHour))
	CreateTable(database)

	while runEvent.is_set():
		numPeople = settings.cntUp-settings.cntDown
		print(TAG+'Numero de Pessoas: '+str(numPeople))

		# Calculates inicial time
		timestamp = time.time()
		dateTime = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

		(tempMeetingRoom, tempLara, tempExternal, doorSignal, compressorSignal) = (0,0,0,0,0)

		InsertData(database, dateTime, tempMeetingRoom, tempLara, tempExternal, doorSignal, numPeople, compressorSignal)
		time.sleep(60)

def counter(timeHour, SAVE_RESULTS):
        try:
                PeopleCounter(0, 0, str(timeHour), SAVE_RESULTS)
        except KeyboardInterrupt:
                print("Destruindo Janelas Abertas")
                cv2.destroyAllWindows()

SAVE_RESULTS = True

TAG = '(main) '

# Calculates inicial time
timestamp = time.time()
timeHour = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

print(TAG+'data/hora: '+ str(timeHour))

settings.init()

runEvent = threading.Event()
runEvent.set()

threadPeopleCounter = threading.Thread(name='people_counter', target=counter, args = (str(timeHour), SAVE_RESULTS))
threadPeopleCounter.daemon = True
threadPeopleCounter.start()
# numberPeople = PeopleCounter(0, 0, str(time), SAVE_RESULTS)
threadPeopleData = threading.Thread(name='data', target=data)
threadPeopleData.start()

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

# print(TAG+'Final2: '+str(numberPeople))

print(TAG+'end')





