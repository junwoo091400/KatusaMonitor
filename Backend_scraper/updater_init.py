filePath = './data.csv'

import datetime

datetime_str = str(datetime.datetime.now())#https://docs.python.org/3/library/datetime.html

def log(l):
	f = open('log.txt','a')
	f.write('['+datetime_str+']')
	f.write(str(l))
	f.close()

def init_header(f_):
	Query = "SELECT dateandtime, month_idx, jeopsu_pcnt FROM number_record WHERE dateandtime >= '2019-09-19 02:09:05' LIMIT 11;"
	import mysql.connector
	try:
		cnx = mysql.connector.connect(user='urur', password='pwpw',  database='DBDB')
		cursor = cnx.cursor()
		cursor.execute(Query)
		records = cursor.fetchall()
		#print(records[0])
		#input('dh')
		comparable = datetime.datetime(2019, 9, 19, 2, 9, 5)
		#print(records)
		for i in range(11):
			if(records[i][0] != comparable):
				log('Datetime Non-match between ' + comparable + ' and ' + records[i][0])
				exit()
			elif(records[i][1] != i):
				log('Sql month_idx non-match, expected ' + i + ' got ' + str(records[i][1]))
				exit()
		#Safe and sound.
		Header = 'DateTime'
		for i in range(11):
			Header += (', month_' + str(i + 2))
		Header += '\n'

		f_.write(Header)#yes.

		lines = str(records[i][0].replace(minute = 0, second = 0))
		for i in range(11):
			lines += (', ' + str(records[i][2]))
		lines += '\n'

		f_.write(lines)#Done.
	except Exception as e:
		print(e)
		log(e)
		exit()
	finally:#https://www.programiz.com/python-programming/exception-handling
		if (cnx.is_connected()):
			cursor.close()
			cnx.close()

try:
	f = open(filePath, 'r')
	if(len(f.readlines()) >= 2):
		print('Already has more than 2 lines in the file. Exiting..')
		f.close()
		exit()
	else:
		f = open(filePath, 'a')
		init_header(f)
		f.close()
except Exception as e:
	f = open(filePath, 'a')
	init_header(f)
	f.close()
