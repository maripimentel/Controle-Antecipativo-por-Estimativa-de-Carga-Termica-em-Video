##Controle Antecipativo por Estimativa de Carga Termica em Video
##Biblioteca para Comunicacao com a Base de Dados
##Trabalho de Graduacao
##Versao 1
##Autores:
##    Alexandre Saran
##    Mariana Pimentel

# coding=utf-8

import sqlite3

# Inicialize database
def InicializeDatabase(name):
	database = sqlite3.connect('../../Dados/'+name)
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
	TAG = '(sqlite) '
	try:
		cursor.execute('''INSERT INTO informacaoSala(dataHora,tempSala,tempVizinha,tempExterna,sinalPorta,numPessoas,sinalCompressor)
	                  VALUES(?,?,?,?,?,?,?)''', (dateTime, tempMeetingRoom, tempLara, tempExternal, doorSignal, numPeople, compressorSignal))
		print(TAG+'dataHora:{1} | numPessoas:{2}'.format(dateTime, numPeople))
	except Exception as e:
		print(TAG+'Falha ao inserir dados')
	database.commit()
	return database

# Read all data from the table
def ReadTable(database):
	TAG = '(sqlite) '
	cursor = database.cursor()
	try:
		cursor.execute('''SELECT dataHora,numPessoas FROM informacaoSala''')
	except Exception as e:
		print(TAG+'Falha ao ler os dados')
	# Prints each line information
	data = cursor.fetchall()
	cont = 0
	for line in data:
	    print(TAG+'Coluna[{0}] -> dataHora:{1} | numPessoas:{2}'.format(cont, line[0], line[1]))
	    cont = cont + 1
	return data

# Close the table
def CloseTable(database):
	database.close()

