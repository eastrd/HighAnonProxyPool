#-*- coding:UTF-8 -*-
#命令行界面模块
#Author: 苍冥 e0t3rx

import scraper_manager
import proxy
import db
from time import sleep
import threading

#启动爬虫与代理验证模块
print("[!] 启动爬虫模块...")
threading.Thread(target=scraper_manager.start, name='Scraper Manager').start()
print("[!] 启动验证模块...")
threading.Thread(target=proxy.start, name='Proxy Manager').start()

#CUI界面循环
while True:
	print("目前数据库中有%s个代理"%len(db.Database().fetch_all()))
	sleep(1)
