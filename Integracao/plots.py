from plotlib import *
from sqlitelib import *

# coding=utf-8

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

# PI
# name = '2018-10-29 22:16:39'
# name = '2018-10-30 12:02:54'
# name = '2018-10-31 10:57:30 -FIM'
name = '2018-11-02 18:40:37 -METADE'

database = InicializeDatabase(name)
# name = '2018-10-14 13:04:18 3'
plotModel(database, name)
