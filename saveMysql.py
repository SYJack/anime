# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 11:54:06 2018

@author: Administrator
"""

import pymysql as mdb
import traceback

DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_USER = 'root'
# MySQL密码
DB_PASS = '167349951'
# 数据库名称
DB_NAME = 'animehome'
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
    def executemany(self,sql,args):
        try:
            if args:
                rs = self.dbcurr.executemany(sql,args)
                return rs
        except Exception as e:
            if self.check_conn():
                print('execute error')
                traceback.print_exc()
            else:
                print('reconnect mysql')
                self.conn()
                if args:
                    rs = self.dbcurr.executemany(sql, args)
                    return rs
    def rollback(self):
        self.dbconn.rollback()
    def commit(self):
        self.dbconn.commit()
    def close(self):
        self.dbconn.close()
        self.dbcurr.close()
db = Db()
