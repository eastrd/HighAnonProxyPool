#-*- coding:UTF-8 -*-
#信息池模块
#Author: 苍冥 e0t3rx

import scraper_manager
import proxy
import db
from time import sleep
import threading
from os import system as cmd
import msvcrt

LOGO = 6*"_"+"                   "+6*"_"+"           _ \n| ___ \                  | ___ \         | |\n| |_/ _ __ _____  ___   _| |_/ ___   ___ | |\n\
|  __| '__/ _ \ \/ | | | |  __/ _ \ / _ \| |\n| |  | | | (_) >  <| |_| | | | (_) | (_) | |\n\_|  |_|  \___/_/\_\\__,  \_|  \___/ \___/|_|\n\
                     __/ |                  \n                    |___/                   \n               _____ _   _____              \n\
              |  _  | | |____ |             \n "+6*"_"+"    ___| |/' | |_    / /_ ____  __   \n|"+6*"_"+"|  / _ |  /| | __|   \ | '__\ \/ /   \n\
         |  __\ |_/ | |_.___/ | |   >  <    \n          \___|\___/ \__\____/|_|  /_/\_\ \n"

MENU = "\n功能菜单："+"\n\t"+"[W] 启动本地WEB服务器"+"\n\t"+"[T]修改验证线程数量"+"\n\t"+"[I]查看使用说明"+"\n\t"+"[M]功能菜单"
modeChoice = "MENU"
modeMapping = {"M":"MENU","T":"THREAD","I":"INSTRUCTION","W":"WEB"}
INSTRUCTION = "高匿代理池说明："

def Input():
	#如果忘记加Global关键字，就不会修改modeChoice的值
	global modeChoice
	while True:
		#忽略特殊按键引起的异常
		try:
			#读取用户输入的按键，并对功能菜单的选项进行映射
			getch = str(msvcrt.getch(),"utf-8")
			if getch.upper() in modeMapping:
				modeChoice = modeMapping[getch.upper()]
		except:
			pass


def Output():
	#实时获取各模块信息并提供命令行交互
	while True:
		TotalProxies = db.Database().fetch_all()
		NumProxies = len(TotalProxies) if TotalProxies is not None else "Read Error Database Locked"
		NumProxyCheckThreads = threading.activeCount()-proxy.InitialThreadNum
		cmd("cls")
		def showInfo():
			print("[!] 目前数据库中有%s个代理"%NumProxies)
			print("[!] 当前代理验证线程数量为: %s\n" %(NumProxyCheckThreads))
		#下面输出界面交互部分
		if modeChoice == "MENU":
			print(LOGO)
			showInfo()
			print(MENU)
		elif modeChoice == "INSTRUCTION":
			showInfo()
			print(INSTRUCTION)
			print(MENU)
		elif modeChoice == "WEB":
			showInfo()
			print("[!] Web功能目前还在开发中，敬请期待："+"\n\t"+"http://github.com/eastrd/HighAnonProxyPool")
			print(MENU)
		elif modeChoice == "THREAD":
			showInfo()
			print("[!] 线程设置功能目前还在开发中，敬请期待："+"\n\t"+"http://github.com/eastrd/HighAnonProxyPool")
			print(MENU)

def Initialise():
	#启动爬虫与代理验证模块
	print("[!] 启动爬虫模块...")
	threading.Thread(target=scraper_manager.start, name='Scraper Manager').start()
	print("[!] 启动验证模块...")
	threading.Thread(target=proxy.start, name='Proxy Manager').start()
	#启动命令行界面交互模块
	threading.Thread(target=Input).start()
	threading.Thread(target=Output).start()
	while True:
		sleep(300)

Initialise()