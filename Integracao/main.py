##Controle Antecipativo por Estimativa de Carga Termica em Video
##Codigo Principal
##Trabalho de Graduacao
##Versao 1
##Autores:
##    Alexandre Saran
##    Mariana Pimentel

# coding=utf-8

from peoplecounterlib import *
import threading
import settings
import time
import datetime

def data(runEvent):
	try:
		while(True):
			print(TAG+'Final: '+str(settings.cntUp-settings.cntDown))
			runEvent.sleep(0.3)
	except KeyboardInterrupt:
		data.clear()
        threadPeopleCounter.join()
        threadPeopleData.join()

def counter(timeHour, SAVE_RESULTS, runEvent):
	numberPeople = PeopleCounter(0, 0, str(timeHour), SAVE_RESULTS)

SAVE_RESULTS = True

TAG = '(main) '

# Calculates inicial time
timestamp = time.time()
timeHour = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

print(TAG+'data/hora: '+ str(timeHour))

settings.init()

runEvent = threading.Event()
runEvent.set()

threadPeopleCounter = threading.Thread(name='people_counter', target=counter, args = (str(timeHour), SAVE_RESULTS, runEvent))
threadPeopleCounter.start()
# numberPeople = PeopleCounter(0, 0, str(time), SAVE_RESULTS)
threadPeopleData = threading.Thread(name='data', target=data, args = (runEvent))
threadPeopleData.start()


# print(TAG+'Final2: '+str(numberPeople))

print(TAG+'end')





