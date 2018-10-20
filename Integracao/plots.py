from plotlib import *
from sqlitelib import *

# coding=utf-8

# Identificacao
# name = '2018-10-12 15:44:53'
# name = '2018-10-13 13:10:18'
# name = '2018-10-14 10:18:28'
name = '2018-10-20 12:29:17'

# Liga-Desliga
# name = '2018-10-14 13:04:18'
database = InicializeDatabase(name)
# name = '2018-10-14 13:04:18 3'
plotModel(database, name)
