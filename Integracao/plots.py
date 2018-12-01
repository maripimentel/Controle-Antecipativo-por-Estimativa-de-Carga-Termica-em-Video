# coding=utf-8
from plotlib import *
from sqlitelib import *

# coding=utf-8

# Tipos de Controladores
# 0 -> Identificacao do Modelo
# 1 -> Liga-Desliga
# 2 -> PI
# 3 -> Antecipativo
controllerType = 1

# Identificacao
# name = '2018-10-12 15:44:53'
# name = '2018-10-13 13:10:18'
# name = '2018-10-14 10:18:28'
# name = '2018-10-23 22:43:46'
# name = '2018-10-20_16-44-16' # OFICIAL


# Liga-Desliga
# name = '2018-10-14 13:04:18'
# name = '2018-10-21 20:33:57'
# name = '2018-10-22 21:40:40'
# name = '2018-11-03_19:17:43'
# name = '2018-11-04 19:48:08'
#name = '2018-11-05 22:47:36' # OFICIAL SEM PERTURBACAO
#name = '2018-11-20_09-56-07_01'
# name = '2018-11-21_09-44-52_01'
#name = '2018-11-05_22-47-36'
#name = '2018-11-27_19-49-04' # COM PERTURBACAO
name = '2018-12-01_09-36-33'

# PI
# name = '2018-10-29 22:16:39'
# name = '2018-10-30 12:02:54'
# name = '2018-10-31 10:57:30 -FIM'
#name = '2018-11-02 18:40:37' # OFICIAL SEM PERTURBACAO
#name = '2018-11-05 22:47:36'
#name = '2018-11-09_09-55-06' # OFICIAL COM PERTURBACAO
# name = '2018-11-22_09-30-11' # PI
#name = '2018-11-23_09-51-38' #8 HORAS OFICIAL
# name = '2018-11-25_09-52-37' # 8 horas dia frio
#name = '2018-11-26_09-32-43' # 8 horas ganhou do nosso

#Antecipativo
# name = '2018-11-10_12-11-55'
# name = '2018-11-11_15-21-49'
# name = '2018-11-12_19-26-23_02'
# name = '2018-11-14_19-29-21'
# name = '2018-11-15_19-45-00_02'
# name = '2018-11-16_13-32-54_02'
#name = '2018-11-16_16-40-57' # oficial
# name = '2018-11-17_17-12-29_01'
# name = '2018-11-19_09-42-35'
#name = '2018-11-24_09-55-53' 
#name = '2018-11-27_09-38-54' #8 HORAS OFICIAL
#name = '2018-11-30_09-51-26' # 8 HORAS OFICIAL sem mudar ref

database = InicializeDatabase(name)
plotModel(database, name, controllerType)