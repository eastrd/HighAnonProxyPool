import lib
import requests
import re
from bs4 import BeautifulSoup as bs

#I have been playing this file around, which it currently won't insert records into the database
#If you want it to function fully, feel free to modify it, as it shouldn't be difficult :p

Pool = lib.ProxyPool("ProxyPoolDB")

RE_Pattern_IPaddr = re.compile("[0-9\.].*")

soup = bs(requests.get("https://incloak.com/proxy-list/?anon=234#list").content,"html.parser")
for RAW_ProxyInfo in soup.find_all("tr"):
	#Length is checked so not to include the skeleton frame <td>
	if len(RAW_ProxyInfo.find_all("td")) == 7:
		IP = str(RAW_ProxyInfo.find("td",{"class":"tdl"})).replace("<td class=\"tdl\">","").replace("</td>","")
		PORT = str(RAW_ProxyInfo.find("td",None)).replace("<td>","").replace("</td>","")
		PROTOCOL = RAW_ProxyInfo.find_all("td")[4].text
		print PROTOCOL+" -> "+IP+":"+PORT+" "*3+"Length: "+str(len(PROTOCOL))






