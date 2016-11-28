import lib
import re
import requests
import base64
import time
from bs4 import BeautifulSoup as bs

'''
This is the script for scraping http://proxy-list.org site
'''

Pool = lib.ProxyPool("ProxyPoolDB")

BASE_URL = "https://proxy-list.org/english/index.php?p=" 

Re_Pattern_IP = re.compile("(.*):")
Re_Pattern_PORT = re.compile(":(.*)")

while True:
	print "Fetching Proxy..."
	for startingURL_Param in range(1,11):
		while True:
			try:
				#If there's an error duing the request, it will try to reconnect until succeed
				while True:
					try:
						HTML_ProxyPage = requests.get(BASE_URL+str(startingURL_Param)).content
						break
					except Exception as e:
						print "An Error occurred: "+str(e)
				soup = bs(HTML_ProxyPage,"html.parser")
				for Raw_ProxyInfo in soup.find_all("ul",{"class":None}):
					ip_port = base64.b64decode(Raw_ProxyInfo.find("li",{"class":"proxy"}).text.replace("Proxy('","").replace("')",""))
					IP = re.findall(Re_Pattern_IP, ip_port)[0]
					PORT = re.findall(Re_Pattern_PORT, ip_port)[0]
					TYPE = Raw_ProxyInfo.find("li",{"class":"https"}).text
					Pool.addProxy(IP,PORT,TYPE)
				break
			except Exception as e:
				print "An error occurred: "+str(e)
	print "Done Fetching... Sleep for 30 seconds..."
	time.sleep(30)
	print ""

