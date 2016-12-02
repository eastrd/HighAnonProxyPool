import sqlite3
import requests
from os import system as cmd
from time import sleep

REQ_TIMEOUT = 1.5

class ProxyPool:
	#Initialise the ProxyPool
	def __init__(self,ProxyPoolDB="ProxyPoolDB"):
		self.ProxyPoolDB = ProxyPoolDB
		self.cursor = sqlite3.connect(self.ProxyPoolDB, isolation_level=None).cursor()
		self.TB_ProxyPool = "TB_ProxyPool"
		self.cursor.execute("CREATE TABLE IF NOT EXISTS "+self.TB_ProxyPool+"(ip TEXT UNIQUE, port INTEGER, protocol TEXT)")
		#Only Uses UNIQUE IP, which in consequence rejects one IP with multiple protocol supports

	#Add record if not exist
	def addProxy(self, IP, PORT, PROTOCOL):
		self.cursor.execute("INSERT OR IGNORE INTO " + self.TB_ProxyPool+"(ip, port, protocol) VALUES (?,?,?)", [IP,PORT,PROTOCOL])

	#*Delete Proxy Data with no connection
	def cleanNonWorking(self):
		for info in self.cursor.execute("SELECT * FROM "+self.TB_ProxyPool).fetchall():
			self.getProxyPoolStatus()
			print info
			IP, PORT, PROTOCOL = info[0], str(info[1]), info[2].lower()
			attempt = 0
			#Loop the connection until internet is up (if connection failed) or proxy works
			while True:
				#print "Testing "+IP+":"+PORT
				isAnonymous = self.testConnection(IP,PORT,PROTOCOL)
				if isAnonymous == False:
					if self.testInternet() == True:
						#Not an Anonymous Proxy
						self.delRecord(IP)
						#print IP+" is down or not anonymous\n"
						break
					#else:
						#print "-"*10+" INTERNET IS DOWN "+"-"*10+"\n"
				else:
					#Is Anonymous Connection
					#print " "*10+" --->>> ANONYMOUS <<<--- \n"
					break
	
	#Outputs Total number of Proxies within ProxyPoolDB, Rate of Proxy HealthChecks, Num of Threads active, Rate of new Proxies added, Rate of Health Proxies
	def getProxyPoolStatus(self):
		records = self.cursor.execute("SELECT * FROM "+self.TB_ProxyPool).fetchall()
		cmd("cls")
		print "[!] Proxy Amount: "+str(len(records))

	#Testing given Proxy's connection and anonymity, returns True if it can be used and is anonymous, otherwise returns False
	def testConnection(self, IP, PORT, PROTOCOL):
		proxies = { PROTOCOL: IP+":"+PORT }
		try:
			OrigionalIP = requests.get("http://icanhazip.com", timeout=REQ_TIMEOUT).content
			MaskedIP = requests.get("http://icanhazip.com", timeout=REQ_TIMEOUT, proxies=proxies).content
			if OrigionalIP != MaskedIP:
				return True
			else:
				print "Not Anonymous"
				return False
		except Exception as e:
			print e	
			return False 
		sleep(2)

	#Erase record based on IP
	def delRecord(self, IP):
		self.cursor.execute("DELETE FROM "+self.TB_ProxyPool+" WHERE ip=?",(IP,))

	#Testing connectivity
	def testInternet(self):
		try:
			requests.get("http://baidu.com", timeout=REQ_TIMEOUT)
			return True
		except:
			return False
