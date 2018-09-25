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

SAVE_RESULTS = True

TAG = '(main) '

# Calculates inicial time
timestamp = time.time()
time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

print(TAG+'data/hora: '+ str(time))

settings.init()

t = threading.Thread(name='people_counter', target=PeopleCounter)
t.start()
# numberPeople = PeopleCounter(0, 0, str(time), SAVE_RESULTS)

print(TAG+'Final1: '+str(settings.cntUp-settings.cntDown))
print(TAG+'Final2: '+str(numberPeople))

print(TAG+'end')
