#!/usr/bin/env python3# -*- coding: utf-8 -*-"""Created on 2017/6/12 下午3:51@author: zhechengma"""from getip import *import requestsfrom lxml.html import etreeimport pymysqlfor i in ip_pool:	proxy=iconn=pymysql.connect(host='192.168.32.48',user='root',password='123456',port=3306,db='washingdata',charset='utf8')cur=conn.cursor()for i in range(1,90,1):	for j in range(0,201,1):		res=requests.get('http://search.114chn.com/searchresult.aspx?type=1&areaid={}&pattern=2&page={}'.format(i,j),proxies=proxy)		contetn=res.text		tree=etree.HTML(contetn)		name=tree.xpath('/html/body/div/div[3]/div[1]//div[@class="f"]/a/text()')		for n in name:			try:				cur.execute('insert into names_list_info_mation (name) values ("{}")'.format(n))				conn.commit()			except Exception as ee:				print(ee)				pass