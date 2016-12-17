#-*- coding:UTF-8 -*-
#代理模块
#Author: 苍冥 e0t3rx

import requests
from time import sleep
import db
from time import sleep
import threading

#ProxyCheckerThread用来多线程对每一个代理进行检测
class ProxyCheckerThread(threading.Thread):
	def __init__(self, DirtyProxy):
		#DirtyProxy is a list containing ip(str), port(int), protocol(str)
		threading.Thread.__init__(self)
		self.DirtyProxy = DirtyProxy
	def run(self):
		#print("Starting Thread for checking %s:%s" %(self.DirtyProxy[0], self.DirtyProxy[1]))
		Proxy().check_ConnAnon(self.DirtyProxy)
		

class Proxy:
	def __init__(self):
		self.REQ_TIMEOUT = 8

	def check_ConnAnon(self, DirtyProxy):
		ip, port, protocol = DirtyProxy[0], DirtyProxy[1], DirtyProxy[2].lower()
		#如果代理is down，则访问的时候是会默认使用源IP的
		proxies = { protocol: ip+":"+str(port) }

		#暂时先从icanhazip获取IP，后期会进行更改
		try:
			MaskedIP = str(requests.get("http://icanhazip.com", timeout=self.REQ_TIMEOUT, proxies=proxies).content, "utf-8").replace("\n","")
		except requests.exceptions.ProxyError:
			#一般情况下是代理挂掉了，直接删除
			db.Database().delete(ip,port,protocol)
			return
		except UnicodeDecodeError:
			#一般解码错误的原因是中文字符，例如：“错误：您所请求的网址（URL）无法获取”，因代理对访问的url存在限制，故此处直接删除
			response = str(requests.get("http://icanhazip.com", timeout=self.REQ_TIMEOUT, proxies=proxies).content, "GBK").replace("\n","")
			#print(ip+": "+response)
			db.Database().delete(ip,port,protocol)
			return
		except ConnectionResetError:
			#连接被重置，一般是服务器那边拒绝连接，直接删除
			db.Database().delete(ip,port,protocol)
			return
		except Exception as e:
			if "timeout" in str(e).lower():
				#代理超时了，删掉换下一个
				db.Database().delete(ip,port,protocol)
				return
			else:
				#一切意外尽在此处捕捉
				print("[!] Unexpected Error: "+str(e))
				return

		if MaskedIP != ip:
			#如果返回的IP和代理ip不一样，则调用数据库接口删除此条代理记录
			db.Database().delete(ip,port,protocol)
		else:
			print("[!] "+ip+":"+str(port)+" is Good!")

	def fetch_info(self):
		#后期更新再开发此功能
		pass

	def ProxyWash(self):
		#调用数据库模块的接口，获取全部代理，并启动多线程验证其有效性
		DirtyProxyList = db.Database().fetch_all()
		print("Current Proxies Count: "+str(len(DirtyProxyList)))
		for ProxyRecord_tuples in DirtyProxyList:
			#如果同时存在多于100个线程，则等待10秒再开新线程
			while threading.activeCount() > 100:
				print("Overloading, waiting for 5 seconds")
				sleep(5)
			ProxyCheckerThread(ProxyRecord_tuples).start()

		


while True:
	#仅当所有子线程都运行完毕的时候再开始新一轮的验证
	if threading.activeCount() == 1:
		#print("Starting a new round of Proxy washing...")
		Proxy().ProxyWash()
	sleep(2)
'''
proxies = { "http": "80.1.116.80"+":"+str(80) }
print(requests.get("http://icanhazip.com", timeout = 8, proxies = proxies).content)
'''