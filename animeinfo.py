# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 23:42:31 2018

@author: jack
"""

import requests
from lxml import etree
from saveMysql import db

class animeinfo():
    
    def __init__(self):
         #self.animeLs = db.execute('select * from animeinfo',None);
         self.headers = {'User-Agent':'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'}
         pass
     
    def getcontent(self):
        db.execute('select ANIME_LINE from anime_home where ID = 15 limit 1',None)
        animeurl = db.fetchone()
        content = self.request(animeurl[0])
        print(content.text)
    
    #多线程获取
    def getanimeinfobythread(self):
        self.getcontent()
    #解析html
    def xpathresolve(self,content,expression):
        page=etree.HTML(content.text)
        return page.xpath(expression)
    
    def request(self,url):
        content=requests.get(url,headers=self.headers)
        content.encoding='utf-8'
        return content

animeinfo = animeinfo()
animeinfo.getanimeinfobythread()