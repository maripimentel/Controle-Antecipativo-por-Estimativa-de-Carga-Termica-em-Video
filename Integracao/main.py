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

def logs():
	print(TAG+'Final: '+str(settings.cntUp-settings.cntDown))
	time.sleep(0.3)

def counter():
	global SAVE_RESULTS
	global timeHour
	numberPeople = PeopleCounter(0, 0, str(timeHour), SAVE_RESULTS)

SAVE_RESULTS = True

TAG = '(main) '

# Calculates inicial time
timestamp = time.time()
timeHour = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

print(TAG+'data/hora: '+ str(timeHour))

settings.init()

t = threading.Thread(name='people_counter', target=counter)
t.start()
# numberPeople = PeopleCounter(0, 0, str(time), SAVE_RESULTS)
d = threading.Thread(name='logs', target=logs)
d.start()


# print(TAG+'Final2: '+str(numberPeople))

print(TAG+'end')





