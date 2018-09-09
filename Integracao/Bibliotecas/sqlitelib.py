##Controle Antecipativo por Estimativa de Carga Termica em Video
##Biblioteca para Comunicacao com a Base de Dados
##Trabalho de Graduação
##Versão 1
##Autores:
##    Alexandre Saran
##    Mariana Pimentel

import sqlite3

# Inicialize database
def InicializeDatabase(name):
	database = sqlite3.connect('../../../Dados/'+name)
	return database


# Create table "informacaoSala"
def CreateTable(database):
	cursor = database.cursor()
	cursor.execute('''
	    CREATE TABLE IF NOT EXISTS informacaoSala(dataHora TEXT PRIMARY KEY, tempSala REAL,
	                       tempVizinha REAL, tempExterna REAL, sinalPorta INTEGER,
	                       numPessoas INTEGER, sinalCompressor INTEGER)
	''')
	database.commit()
	return database 

# Insert data in table
def InsertData(database, dateTime, tempMeetingRoom, tempLara, tempExternal, doorSignal, numPeople, compressorSignal):
	cursor = database.cursor()
	try:
		cursor.execute('''INSERT INTO informacaoSala(dataHora,tempSala,tempVizinha,tempExterna,sinalPorta,numPessoas,sinalCompressor)
	                  VALUES(?,?,?,?,?,?,?)''', (dateTime, tempMeetingRoom, tempLara, tempExternal, doorSignal, numPeople, compressorSignal))
	except Exception as e:
		print('Falha ao inserir dados')
	database.commit()
	return database

# Read all data from the table
def ReadTable(database):
	cursor = database.cursor()
	try:
		cursor.execute('''SELECT dataHora,tempSala,tempVizinha FROM informacaoSala''')
	except Exception as e:
		print('Falha ao ler os dados')
	# Prints each line information
	data = cursor.fetchall()
	for line in data:
	    print('{0} : {1}, {2}'.format(line[0], line[1], line[2]))
	return data

# Close the table
def CloseTable(database):
	database.close()
