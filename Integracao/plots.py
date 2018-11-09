from plotlib import *
from sqlitelib import *

# coding=utf-8

# Tipos de Controladores
# 0 -> Identificacao do Modelo
# 1 -> Liga-Desliga
# 2 -> PI
# 3 -> Antecipativo
controllerType = 2

# Identificacao
# name = '2018-10-12 15:44:53'
# name = '2018-10-13 13:10:18'
# name = '2018-10-14 10:18:28'
# name = '2018-10-20 16:44:16'
# name = '2018-10-23 22:43:46'


# Liga-Desliga
# name = '2018-10-14 13:04:18'
# name = '2018-10-21 20:33:57'
# name = '2018-10-22 21:40:40'
# name = '2018-11-03_19:17:43'
# name = '2018-11-04 19:48:08'

# PI
# name = '2018-10-29 22:16:39'
# name = '2018-10-30 12:02:54'
# name = '2018-10-31 10:57:30 -FIM'
#name = '2018-11-02 18:40:37'
#name = '2018-11-05 22:47:36'

name = '2018-11-09_09-55-06_07'

database = InicializeDatabase(name)
plotModel(database, name, controllerType)
