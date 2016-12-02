import lib
import requests
import re
from bs4 import BeautifulSoup as bs

Pool = lib.ProxyPool()

RE_Pattern_IPaddr = re.compile("[0-9\.].*")
soup = bs(requests.get("https://incloak.com/proxy-list/?anon=234#list").content,"html.parser")

for RAW_ProxyInfo in soup.find_all("tr"):
	#Length is checked so not to include the skeleton frame <td>
	if len(RAW_ProxyInfo.find_all("td")) == 7:
		IP = str(RAW_ProxyInfo.find("td",{"class":"tdl"})).replace("<td class=\"tdl\">","").replace("</td>","")
		PORT = str(RAW_ProxyInfo.find("td",None)).replace("<td>","").replace("</td>","")
		PROTOCOL = RAW_ProxyInfo.find_all("td")[4].text
		if "HTTPS" in PROTOCOL:
			Pool.addProxy(IP,PORT,"HTTPS")