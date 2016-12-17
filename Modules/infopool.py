#-*- coding:UTF-8 -*-
#信息池模块
#Author: 苍冥 e0t3rx

import scraper_manager
import proxy
import db
from time import sleep
import threading
from os import system as cmd

#启动爬虫与代理验证模块
print("[!] 启动爬虫模块...")
threading.Thread(target=scraper_manager.start, name='Scraper Manager').start()
print("[!] 启动验证模块...")
threading.Thread(target=proxy.start, name='Proxy Manager').start()
sleep(2)

#实时获取各模块信息
while True:
	TotalProxies = db.Database().fetch_all()
	NumProxies = len(TotalProxies) if TotalProxies is not None else "Read Error Database Locked"
	NumProxyCheckThreads = threading.activeCount()-proxy.InitialThreadNum
	cmd("cls")
	print("[!] 目前数据库中有%s个代理"%NumProxies)
	print("[!] 当前代理验证线程数量为: %s" %(NumProxyCheckThreads))
