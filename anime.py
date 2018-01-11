# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 15:24:48 2018

@author: jack
"""

import os
import random
import requests
import sys
import time
import traceback
import re
import hashlib
import json
from saveMysql import db

class anime():
    def all_url(self,baseUrl,referer):
        for i in range(30254,30257):
            self.aa(baseUrl,referer,i)
            time.sleep(10)
            print(u'获取下个地域数据')
        print(u'已经跑完')
        db.close()
       
    def aa(self,baseUrl,referer,i):
        # 格式化请求链接
        if i > 30256:
            db.close()
            print(u'更新数据完毕...')
            sys.exit(0)
        zoneUrl = baseUrl % {'zoneCode': str(i),'page':'1','time': str(round(time.time()*1000))}
        zoneReferer = referer % {'zoneCode': str(i),'page':'1'}
        contentJson = self.request(zoneUrl)
        self.jsonResolve(contentJson.text, baseUrl, i,referer)
            
    def jsonResolve(self, content, baseUrl, zoneCode,referer):
        dataJson = json.loads(content[7:-2])
        if dataJson['status'] == 'OK' :
            for pageNum in range(1,int(dataJson['page_count'])+1):
               #笨方法新增数据
               if pageNum == 2:
                   self.aa(baseUrl,referer,zoneCode+1)
                   break
               try:
                  self.getAnimeLsData(baseUrl, zoneCode,referer,pageNum)
                  time.sleep(3)
               except Exception as e:
                   traceback.print_exc()
                   self.getAnimeLsData(baseUrl, zoneCode,referer,pageNum)
        else:
            return self.jsonResolve(content,baseUrl,zoneCode,referer)
        
    def getAnimeLsData(self, baseUrl, zoneCode,referer,pageNum):
       print(u'获取第',pageNum,'页数据')
       # 每页数据的请求ajax
       pageUrl = baseUrl % {'zoneCode': str(zoneCode),'page':str(pageNum),'time': str(round(time.time()*1000))}
       # 每页数据的请求引用
       pageReferer = referer % {'zoneCode': str(zoneCode),'page':str(pageNum)}
       animeJsonLs = self.request(pageUrl)
       self.getAnimeData(animeJsonLs.text,zoneCode,baseUrl,referer)
       
    def getAnimeData(self, content,zoneCode,baseUrl,referer):
        dataJson = json.loads(content[7:-2])
        if dataJson['status'] == 'OK' :
            #打开数据库连接        
            db.conn()
            #批量存入值
            values=[]
            for anime in dataJson['result']:
                #获取链接
                animeLine ='http://donghua.dmzj.com'+(str(anime['anim_link']))
                #获取动漫id
                amineId = int(re.sub('\D', '', str(anime['anim_link'])))
                #生成动漫链接md5
                animeLineMd5=self.md5Encode(animeLine)
                if db.execute('select 1 from anime_home a where a.ANIME_LINE_MD5 = %s limit 1',(animeLineMd5)) == 0:
                    values.append([amineId,anime['anim_name'],anime['cover'],str(zoneCode),str(animeLine),animeLineMd5])
                else:
                    print(u'已存在')
                    #因为之前已经获取所有了数据，现在只要更新数据，添加return跳出循环，去掉则在最后一页会进入循序
                    #return self.aa(baseUrl,referer,zoneCode+1)
            try:
                db.executemany('insert into anime_home(ANIME_ID,ANIME_NAME,ANIME_IMAGE,ANIME_REGION,ANIME_LINE,ANIME_LINE_MD5,ANIME_INFO_DOWNLOAD_STATUS) values (%s,%s,%s,%s,%s,%s,0)',values)
            except Exception as e:
                traceback.print_exc()
                db.rollback()
            else:
                db.commit()
                time.sleep(5)
    
#    def request(self, url,referer):
#        content = request.get(url,5,'s.acg.dmzj.com',referer)
#        content.encoding = 'utf-8'
#        return content
    def request(self,url):
        content=requests.get(url,headers={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"})
        content.encoding='utf-8'
        return content
    
    def md5Encode(self,str):
        m = hashlib.md5()
        m.update(str.encode('utf-8'))
        return m.hexdigest()
    
    def testDb(self):
        db.conn()
        rs = db.execute('select * from anime_home a where a.ANIME_LINE_MD5 = %s',('8869584a4ef407be3cb3da67d5daf275'))
        print(rs)

Anime = anime()

Anime.all_url('http://s.acg.dmzj.com/dh/index.php?c=msearch&m=multiSearch&play_type=0&status=0&zone=%(zoneCode)s&year=0&initial=all&category=0&_order=t&p=%(page)s&callback=dolist&tt=%(time)s'
              , 'http://donghua.dmzj.com/acg_donghua/0-0-%(zoneCode)s-0-all-0-0-0-%(page)s.html')
#Anime.testDb()
