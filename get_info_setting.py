#!/usr/bin/env python3# -*- coding: utf-8 -*-"""Created on 2017/6/21 下午7:26@author: zhechengma"""from db import *import threadingimport requestsfrom lxml.html import etreeimport urllib.parseimport timefrom getip import *import apidb=MyselfDB()lines=db.select('c_base')proxy = {"http":"http//{}".format(ip_address)}testtable=lines.head(5)['name']def passingby():	url='http://mobile.shuidixy.com/needcode'	s=requests.session()	headers={		'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "		               "Chrome/52.0.2743.116 Safari/537.36"	}	res=s.get(url,headers,proxies=proxy)	f=open('1.jpg','wb')	f.write(res.content)	f.close()	result=api.main('1.jpg')	print(result)	res=requests.get('http://mobile.shuidixy.com/?action=check_code&code={}'.format(result))	res=requests.post(result)def show(lock):	time.sleep(3)	for i in list(testtable):		url='http://www.shuidixy.com/search?key={}&searchType=all'.format(urllib.parse.quote(i))		res=requests.get(url = url,proxies=proxy)		tree = etree.HTML(res.text)		date=tree.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[3]/div/div[2]/div[1]/span[2]/text()")		name=tree.xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div[2]/div/div[2]/a/em/text()")		name=name[0]		date=date[0]		print(name,date)for i in range(1):	t=threading.Thread(target = show,args = (i,))	t.start()