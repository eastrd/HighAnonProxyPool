'''
ProxyPool Database:
	- Loop through proxies
	- Check their connection availability and anonymity.
	- Delete the proxy record if found unavailable or non-anonymous.
'''

'''
Next Step:
	- A daemon process to keep branched processes alive
	- Multiprocessing for purifying the proxy data within the database
	- More proxy scraping processes
	- URGENT: Need to separate the "testing internet connection" module into its own
'''

import sqlite3
import requests

REQ_TIMEOUT = 1.5

class ProxyPool:
	#Initialise the ProxyPool
	def __init__(self,ProxyPoolDB):
		self.ProxyPoolDB = ProxyPoolDB
		self.cursor = sqlite3.connect(self.ProxyPoolDB, isolation_level=None).cursor()
		self.TB_ProxyPool = "TB_ProxyPool"
		self.cursor.execute("CREATE TABLE IF NOT EXISTS "+self.TB_ProxyPool+"(ip TEXT UNIQUE, port INTEGER, protocol TEXT)")

	#Add record if not exist
	def addProxy(self, IP, PORT, PROTOCOL):
		self.cursor.execute("INSERT OR IGNORE INTO " + self.TB_ProxyPool+"(ip, port, protocol) VALUES (?,?,?)", [IP,PORT,PROTOCOL])

	#Delete Proxy Data with no connection
	def cleanNonWorking(self):
		for info in self.cursor.execute("SELECT * FROM "+self.TB_ProxyPool).fetchall():
			IP, PORT, PROTOCOL = info[0], str(info[1]), info[2].lower()
			attempt = 0
			while True:
				print "Testing "+IP+":"+PORT
				#Attempt to connect for 4 times
				isAnonymous = self.testConnection(IP,PORT,PROTOCOL) or self.testConnection(IP,PORT,PROTOCOL) or self.testConnection(IP,PORT,PROTOCOL) or self.testConnection(IP,PORT,PROTOCOL)
				if isAnonymous == False:
					if self.testInternet() == True:
						#Not an Anonymous Proxy
						self.delRecord(IP)
						print IP+" is down or not anonymous\n"
						break
					else:
						print "-"*10+" INTERNET IS DOWN "+"-"*10+"\n"
				else:
					#Is Anonymous Connection
					print " "*10+" --->>> ANONYMOUS <<<--- \n"
					break
	
	#Testing connection and anonymity, returns True if it can be used and is anonymous, otherwise returns False
	def testConnection(self, IP, PORT, PROTOCOL):
		proxies = { PROTOCOL: IP+":"+PORT }
		try:
			OrigionalIP = requests.get("http://icanhazip.com", timeout=REQ_TIMEOUT).content
			MaskedIP = requests.get("http://icanhazip.com", timeout=REQ_TIMEOUT, proxies=proxies).content
			if OrigionalIP != MaskedIP:
				return True
			else:
				return False
		except:	
			return False 

	#Erase record based on IP
	def delRecord(self, IP):
		self.cursor.execute("DELETE FROM "+self.TB_ProxyPool+" WHERE ip=?",(IP,))


#####################################################
#				Situational Patches					#
#####################################################
	#Testing connectivity
	def testInternet(self):
		try:
			requests.get("http://baidu.com", timeout=REQ_TIMEOUT)
			return True
		except:
			return False

	#Delete Proxy Data with no protocol provided (Http / Https)
	def cleanNullProtocol(self):
		self.cursor.execute("DELETE FROM "+self.TB_ProxyPool+" WHERE protocol != ? and protocol != ?", ("HTTP","HTTPS"))