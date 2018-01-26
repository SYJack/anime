# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 16:13:30 2018

@author: jack
"""

import requests
from lxml import etree
import os,random,time,traceback,hashlib
import pymysql as mdb

DB_HOST = '127.0.0.1'
DB_POST = '3306'
DB_USER = 'root'
# MySQL密码
DB_PASS = '167349951'
# 数据库名称
DB_NAME = 'test'

SPIDER_INTERVAL = 5  # 至少保证10秒以上，否则容易被封

class Db(object):
    def __init__(self):
        self.dbconn = None
        self.dbcurr = None
    def check_conn(self):
        try:
            self.dbconn.ping()
        except:
            return False
        else:
            return True
    def conn(self):
        if not self.dbcurr:
            self.dbconn = mdb.connect(DB_HOST, DB_USER, DB_PASS, DB_NAME, charset='utf8')
            self.dbconn.autocommit(False)
            self.dbcurr = self.dbconn.cursor()
    def fetchone(self):
        return self.dbcurr.fetchone()

    def fetchall(self):
        return self.dbcurr.fetchall()
    def execute(self,sql,args):
        try:
            if args:
                rs = self.dbcurr.execute(sql,args)
            else:
                rs = self.dbcurr.execute(sql)
            return rs
        except Exception as e:
            if self.check_conn():
                print('execute error')
                traceback.print_exc()
            else:
                print('reconnect mysql')
                self.conn()
                if args:
                    rs = self.dbcurr.execute(sql, args)
                else:
                    rs = self.dbcurr.execute(sql)
                return rs
    def rollback(self):
        self.dbconn.rollback()
    def commit(self):
        self.dbconn.commit()
    def close(self):
        self.dbconn.close()
        self.dbcurr.close()
        

class xicidaili():
    def __init__(self):
        self.user_agent_list = [ \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
                "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
                "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
            ]
        UA=random.choice(self.user_agent_list)
        self.headers = {
                'Host':"www.xicidaili.com",#需要修改为当前网站主域名
                'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                'Accept-Encoding': "gzip, deflate",
                'Accept-Language': "zh-CN,zh;q=0.9",
                'Connection': "keep-alive",
                'User-Agent':UA}
    def all_url(self,url):
       return self.request(url)
    def request(self,url):
        content=requests.get(url,self.headers, timeout=20);
        return content
#Xicidaili = xicidaili()
#Xicidaili.all_url("http://www.xicidaili.com/nn/2601")
db = Db()
db.check_conn()
    