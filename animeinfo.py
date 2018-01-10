# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 23:42:31 2018

@author: jack
"""

import requests
import re
import traceback
from lxml import etree
from saveMysql import db

class animeinfo():
    
    def __init__(self):
         #self.animeLs = db.execute('select * from animeinfo',None);
         self.headers = {'User-Agent':'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'}
    #获取动漫类型
    def getanmieType(self):
        content = self.request('http://donghua.dmzj.com/acg_donghua/')
        if content.status_code != requests.codes.ok:
            print(u'获取失败!请检测网络连接情况或者是否能正常访问该网站...')
            return
        result = self.xpathresolve(content,"//a[@name='nav_item_category']/@id|//a[@name='nav_item_category']/@title")
        typeList = []
        typeLs = []
        for i in range(0,len(result),2):
            typeList.append(result[i:i+2])
        if len(typeList)>0:
            for i in typeList:
                type_id = re.sub('\D', '', str(i[0]))
                if type_id:
                    typeLs.append([int(type_id),i[1]])
                else:
                    print(i[0],i[1])
        try:
            db.executemany('insert into anime_type(ANIME_TYPE_ID,ANIME_TYPE_NAME) values (%s,%s)',typeLs)
        except Exception as e:
            traceback.print_exc()
            db.rollback()
        else:
            pass
        finally:
            db.commit()
            db.close()
    def getcontent(self):
        db.execute('select ANIME_LINE from anime_home where ID = 15 limit 1',None)
        animeurl = db.fetchone()
        content = self.request(animeurl[0])
        if content.status_code != requests.codes.ok:
            print(u'获取失败!请检测网络连接情况或者是否能正常访问该网站...')
            return
        result = self.xpathresolve(content,"//a[@name='nav_item_category']/@id|//a[@name='nav_item_category']/@title")
    
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