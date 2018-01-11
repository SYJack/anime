# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 23:33:22 2018

@author: jack
"""

import requests
import random
import json
import time,traceback
import hashlib
import threading
from queue import Queue
from saveMysql import db
from lxml import etree
from proxyDownLoad import request

class proxypool:
    
    def __init__(self):
        self.timeout = 5
        self.lock = threading.Lock() #建立一个锁
        self.queue = Queue()
        self.headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36"}
    #获取代理列表
    def getProxyLs(self):
        try:
            html = requests.get('http://47.97.7.119:8080/proxypool/proxys/0',timeout =self.timeout)
            db.conn()
            proxyLs = []
            if html.status_code != requests.codes.ok:
                print(u'获取代理失败!')
                return
            proxyDataLs = json.loads(html.text)['data']
            for proxy in proxyDataLs:
                proxyLs.append([proxy['type'],proxy['ip'],str(proxy['port']),round(time.time()*1000),None,self.md5Encode(proxy['ip'])])
            try:
                db.executemany('replace into proxyls(PROXY_TYPE,PROXY_ADDR,PROXY_PORT,PROXY_ADD_TIME,PROXY_CHECK_TIME,PROXY_MD5) values (%s,%s,%s,%s,%s,%s)',proxyLs)
            except Exception as e:
                traceback.print_exc()
                db.rollback()
            else:
                db.commit()
                time.sleep(3)
                print(u'爬取完毕')
        except Exception as e:
            traceback.print_exc()
        time.sleep(2)
        print(u'开始检验代理...')
        self.testbythread()
    #获取西刺代理
    def getxiciProxy(self,i):
        proxyList=[]
        proxyLs=[]
        print(u'获取第',i,'页数据')
        html=self.request('http://www.xicidaili.com/nn/'+str(i),i)
        all_proxy=self.xpathResolve(html,"//table[@id='ip_list']/tr[@class][position()>1]//td[6]|//table[@id='ip_list']/tr[@class][position()>1]//td[2]|//table[@id='ip_list']/tr[@class][position()>1]//td[3]")
        if len(all_proxy)>0:
            for i in range(0,len(all_proxy),3):
                proxyList.append(all_proxy[i:i+3])
        if len(proxyList)>0:
            for i in proxyList:
                proxyLs.append([i[2].text.lower(),i[0].text,str(i[1].text),round(time.time()*1000),None,self.md5Encode(i[0].text)])
        self.lock.acquire()  
        try:
            db.executemany('insert into proxyls(PROXY_TYPE,PROXY_ADDR,PROXY_PORT,PROXY_ADD_TIME,PROXY_CHECK_TIME,PROXY_MD5) values (%s,%s,%s,%s,%s,%s)',proxyLs)
        except Exception as e:
            traceback.print_exc()
            db.rollback()
        else:
            db.commit()
        self.lock.release() 
        
#    def request(self,url):
#        content=requests.get(url,headers=self.headers)
#        content.encoding='utf-8'
#        return content
#    #请求
    def request(self, url,i):
        content = request.get(url,10,'www.xicidaili.com','http://www.xicidaili.com/nn/'+str(i))
        content.encoding = 'utf-8'
        return content
    #解析
    def xpathResolve(self,content,expression):
        page=etree.HTML(content.text)
        return page.xpath(expression)    
    
    def synchronous(self,f):  
        def call(*args, **kwargs):  
            self.lock.acquire()  
            try:  
                return f(*args, **kwargs)  
            finally:  
                self.lock.release()  
        return call
    #检验代理
    def checkproxy(self):
            while True:
                if not self.queue.empty():
                    proxy = self.queue.get()
                else:
                    return
                try:
                    requests.get('https://www.baidu.com/', proxies={proxy[1]:'http://'+proxy[2]+':'+proxy[3]},timeout =5)
                    print(u'验证'+proxy[1]+':'+'http://'+proxy[2]+':'+proxy[3])
                except Exception as e:
                    traceback.print_exc()
                    self.lock.acquire()#获得锁
                    self.delproxy(proxy[0])
                    self.lock.release() #释放锁
                else:
                    self.lock.acquire()#获得锁
                    self.writeproxy(proxy[0])
                    self.lock.release() #释放锁
                finally:
                     time.sleep(1)
                     #线程告知任务完成使用task_done
                     self.queue.task_done()
                   
    def writeproxy(self,id):
        try:
            db.execute('update proxyls p set p.PROXY_CHECK_TIME = %s where p.ID = %s' % (round(time.time()*1000),id),None)
        except:
            db.rollback()
        
    def delproxy(self,id):
        try:
            db.execute('delete from proxyls where ID = %s' % (id),None)
        except:
            db.rollback()
        
    def md5Encode(self,str):
        m = hashlib.md5()
        m.update(str.encode('utf-8'))
        return m.hexdigest()
    #多线程获取西刺代理
    def xiciproxythread(self):
        threads = []
        start = time.clock()
        for i in range(1,11):
            thread = threading.Thread(target=self.getxiciProxy,args=[i])
            thread.setDaemon(True)
            thread.start() #启动线程
            threads.append(thread)
            time.sleep(2)
        #结束线程
        for thread in threads:
            thread.join()
        db.close()
        print(str(time.clock()-start) + "秒")
        print(u'验证完毕')
    
    #多线程验证
    def testbythread(self):
        threads=[]
        db.execute('select * from proxyls',None);
        proxyLs = db.fetchall()
        start = time.clock()
        for p in proxyLs:
            self.queue.put(p)
        for i in range(5):
            thread = threading.Thread(target=self.checkproxy)
            thread.setDaemon(True)
            thread.start() #启动线程
            threads.append(thread)
        #结束线程
        for thread in threads:
            thread.join()
         #等待所有任务完成
        self.queue.join()  
        db.commit()
        db.close()
        print(str(time.clock()-start) + "秒")
        print(u'验证完毕')
    #单线程验证
    def checkproxy2(self):
         start = time.clock()
         print(start)
         for result in self.proxyLs:
             try:
                 content = requests.get('https://www.baidu.com/', proxies={result[1]:'http://'+result[2]+':'+result[3]},timeout =5)
                 print(u'验证'+result[1]+':'+'http://'+result[2]+':'+result[3])
             except Exception as e:
                traceback.print_exc()
                print('false')
                self.delproxy(result[0])
             else:
                if content.status_code == requests.codes.ok:
                    self.writeproxy(result[0])
                else:
                    self.delproxy(result[0])
             finally:
                db.commit()
                db.close
         print(str(time.clock()-start) + "秒")
         print(u'验证完毕')
    def testdb(self):
        db.execute('delete from proxy where ID = %s' % (73),None)
        db.commit()
        db.close()        
proxypool = proxypool()
proxypool.getProxyLs()

