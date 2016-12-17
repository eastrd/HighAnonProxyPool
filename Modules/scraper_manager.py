#-*- coding:UTF-8 -*-
#爬虫管理模块
#Author: 苍冥 e0t3rx

import re
import requests
import base64
import time
from bs4 import BeautifulSoup as bs
import db
from time import sleep
import threading
'''
#ScraperManagerThread用来启动所有爬虫线程，以便同时爬取所有代理
class ScraperManagerThread(threading.Thread):
	def __init__(self, IntervalDelay):
		#IntervalDelay是每轮爬取页面后的冷却时间（秒）
		threading.Thread.__init__(self)
		self.IntervalDelay = IntervalDelay
	def run(self):
		A()
		B()

'''
IntervalDelay = 10

def proxy_list_org():
	#http://proxy-list.org
	print("[!] Starting proxy-list.org thread...")
	BASE_URL = "https://proxy-list.org/english/index.php?p=" 
	Re_Pattern_IP = re.compile("(.*):")
	Re_Pattern_PORT = re.compile(":(.*)")
	while True:
		#print("[!] Scraping proxy-list.org...")
		for startingURL_Param in range(1,11):
			while True:
				try:
					#If there's an error duing the request, it will try to reconnect until succeed
					while True:
						try:
							HTML_ProxyPage = requests.get(BASE_URL+str(startingURL_Param)).content
							break
						except Exception as e:
							print("An Error occurred: "+str(e))
					soup = bs(HTML_ProxyPage,"html.parser")
					for Raw_ProxyInfo in soup.find_all("ul",{"class":None}):
						ip_port = str(base64.b64decode(Raw_ProxyInfo.find("li",{"class":"proxy"}).text.replace("Proxy('","").replace("')","")), "utf-8")
						IP = re.findall(Re_Pattern_IP, ip_port)[0]
						PORT = re.findall(Re_Pattern_PORT, ip_port)[0]
						PROTOCOL = Raw_ProxyInfo.find("li",{"class":"https"}).text
						if PROTOCOL != "-":
							db.Database().add(IP,PORT,PROTOCOL.lower())
					break
				except Exception as e:
					print("An error occurred with proxy_list_org: "+str(e))
		#print("[ Done Fetching... Sleep for 5 seconds... ]")
		sleep(IntervalDelay)


def incloak_com():
	#http://inclock.com
	print("[!] Starting incloak.com thread...")
	RE_Pattern_IPaddr = re.compile("[0-9\.].*")
	while True:
		try:
			#print("[!] Scraping incloak.com...")
			soup = bs(requests.get("https://incloak.com/proxy-list/?anon=234#list").content,"html.parser")
			for RAW_ProxyInfo in soup.find_all("tr"):
				#Length is checked so not to include the skeleton frame <td>
				if len(RAW_ProxyInfo.find_all("td")) == 7:
					IP = str(RAW_ProxyInfo.find("td",{"class":"tdl"})).replace("<td class=\"tdl\">","").replace("</td>","")
					PORT = str(RAW_ProxyInfo.find("td",None)).replace("<td>","").replace("</td>","")
					PROTOCOL = RAW_ProxyInfo.find_all("td")[4].text
					if "SOCK" not in PROTOCOL:
						if "HTTPS" in PROTOCOL:
							db.Database().add(IP,PORT,"https")
						elif "HTTP" in PROTOCOL.replace("HTTPS",""):
							db.Database().add(IP,PORT,"http")
		except Exception as e:
			print("An error occurred with incloak_com: "+str(e))
		sleep(IntervalDelay)

def start():
	threading.Thread(target=proxy_list_org, name='proxy-list.org').start()
	threading.Thread(target=incloak_com, name='incloak.com').start()
	while True:
		#print("Current Amount of Threads: "+str(threading.activeCount()))
		sleep(100)
