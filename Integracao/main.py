##Controle Antecipativo por Estimativa de Carga Termica em Video
##Codigo Principal
##Trabalho de Graduação
##Versao 1
##Autores:
##    Alexandre Saran
##    Mariana Pimentel

from peoplecounterlib import *
import time
import datetime

SAVE_RESULTS = True

# Calculates inicial time
timestamp = time.time()
time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

numberPeople = PeopleCounter(0, 0, str(time), SAVE_RESULTS)