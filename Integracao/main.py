import sys
sys.path.insert(0, '/home/pi/Documents/Controle-Antecipativo-por-Estimativa-de-Carga-Termica-em-Video/Integracao/Bibliotecas')

from Bibliotecas.peoplecounterlib import PeopleCounter

SAVE_RESULTS = True

# Calculates inicial time
timestamp = time.time()
time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

numberPeople = PeopleCounter(0, 0, (str)time, SAVE_RESULTS)