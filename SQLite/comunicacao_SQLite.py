import sqlite3

CRIAR = True
INSERIR = True
LER = True

# Cria ou abre o arquivo
db = sqlite3.connect('Dados/info')

# Para criar a tabela
if CRIAR:
	cursor = db.cursor()
	cursor.execute('''
	    CREATE TABLE IF NOT EXISTS informacaoSala(dataHora TEXT PRIMARY KEY, tempSala REAL,
	                       tempVizinha REAL, tempExterna REAL, sinalPorta INTEGER,
	                       numPessoas INTEGER, sinalCompressor INTEGER)
	''')
	db.commit()

# Para inserir dados
if INSERIR:
	cursor = db.cursor()

	# Dados
	dataHora = '2'
	tempSala = '30'
	tempVizinha = '30'
	tempExterna = '30'
	sinalPorta = '1'
	numPessoas = '5'
	sinalCompressor = '1'
	 
	# Insercao
	try:
		cursor.execute('''INSERT INTO informacaoSala(dataHora,tempSala,tempVizinha,tempExterna,sinalPorta,numPessoas,sinalCompressor)
	                  VALUES(?,?,?,?,?,?,?)''', (dataHora,tempSala,tempVizinha,tempExterna,sinalPorta,numPessoas,sinalCompressor))
		print('Dados inseridos com sucesso')
	except Exception as e:
		print('Falha ao inserir dados')
	 
	db.commit()

# Para ler os dados
if LER:
	cursor = db.cursor()
	
	# Le os dados
	try:
		cursor.execute('''SELECT dataHora,tempSala,tempVizinha FROM informacaoSala''')
	except Exception as e:
		print('Falha ao ler os dados')
	# user1 = cursor.fetchone() #retrieve the first row
	# print(user1[0]) #Print the first column retrieved(user's name)
	# print(user1[1])
	# print(user1[2])

	# Imprime a informacao de cada coluna
	colunas = cursor.fetchall()
	for info in colunas:
	    # row[0] returns the first column in the query (name), row[1] returns email column.
	    print('{0} : {1}, {2}'.format(info[0], info[1], info[2]))

# # Para deletar uma tabela
# cursor = db.cursor()
# cursor.execute('''DROP TABLE users''')
# db.commit()

# Fecha o arquivo
db.close()