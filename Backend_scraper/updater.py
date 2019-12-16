filePath = './data.csv'

import datetime

datetime_str = str(datetime.datetime.now())#https://docs.python.org/3/library/datetime.html

def log(l):
	f = open('log.txt','a')
	f.write('['+datetime_str+']')
	f.write(str(l) + '\n')
	f.close()

def getQuery(query):
	import mysql.connector
	data = []
	try:
		cnx = mysql.connector.connect(user='urur', password='pwpw',  database='DBDB')
		cursor = cnx.cursor()
		# print(query)
		# input()
		cursor.execute(query)
		data = cursor.fetchall()
	except Exception as e:
		log(e)
		exit()
	finally:#https://www.programiz.com/python-programming/exception-handling
		if (cnx.is_connected()):
			cursor.close()
			cnx.close()
		return data

def update():#Close Inside this Function. Stream.
	f_ = open(filePath,'r')
	data = f_.readlines()
	f_.close()

	f_ = open(filePath, 'a')
	lastTime_str = data[-1].split(',')[0]#Split via CSV format..
	nextTime = datetime.datetime.strptime(lastTime_str, '%Y-%m-%d %H:%M:%S')#Sql to datetime.
	nextTime = nextTime.replace(minute = 0, second = 0)#Make sure.
	nextTime = nextTime + datetime.timedelta(hours=1)#Next Hour!
	nextTime_str = nextTime.strftime('%Y-%m-%d %H:%M:%S')#ok.

	Query = "SELECT dateandtime, month_idx, jeopsu_pcnt FROM number_record WHERE dateandtime >= '{}' LIMIT 11;".format(nextTime_str)
	result = getQuery(Query)
	if(len(result) <= 10):#something wrong or not update time. lol.
		f_.close()

		#Try at the Bottom! At the end of recursion.
		import os
		os.system("cp ./data.csv ./KatuSatu/data.csv")#copy
		os.chdir("./KatuSatu")#Lol. chdir func. Exists!!!
		os.system("git add ./*")#almost forgot about this step... 4:43am right now...
		os.system("git commit -m \"Data Uploaddd...\"")
		os.system("git pull origin")#Just in case there is a change in Origin. Usually not data.csv.
		os.system("git push origin")
		#Done.
		
		exit()#Go!
	elif(len(result) == 11):#Probably right... Hehe.
		lines = str(result[0][0].replace(minute = 0, second = 0))#Cleanify. Although hmmm....
		for i in range(11):
			lines += (', ' + str(result[i][2]))
		lines += '\n'
		f_.write(lines)#Done.
		f_.close()#Close output stream.
		log('Added line: ' + lines.rstrip())#yup.
		update()#Recursive let's gooooo.
try:
	f = open(filePath, 'r')
	f.close()
	update()
except Exception as e:
	import os
	os.system('python updater_init.py')#Redo.!!!
	#os.system('python updater.py')#Relive.
	try:
		f = open(filePath, 'r')
		f.close()
		update()
	except Exception as e:
		log(e)
		exit()#Dude...