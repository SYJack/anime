# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 20:39:01 2018

@author: jack
"""

import requests
import random
import time,traceback
import sys
import os
sys.path.append(os.getcwd() + '/db')
from saveMysql import db

class download():
    def __init__(self):
        db.execute('select * from proxyls',None);
        self.proxyLs = db.fetchall()
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
                "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",\
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
            ]
    def get(self,url,timeout,host,referer,proxy = None,num_retries = 6):
        UA =random.choice(self.user_agent_list)
        headers = {
                'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                'Accept-Encoding': "gzip, deflate",
                'Accept-Language': "zh-CN,zh;q=0.8",
                'Connection': "keep-alive",
                'Host':host,
                'Referer':referer,
                'User-Agent':UA}
#        if proxy == None:##代理为空
#            try:
#                return requests.get(url,headers = headers,timeout = timeout)
#            except: ##如果上面的代码执行报错则执行下面的代码
#                if num_retries > 0:
#                    time.sleep(10)
#                    print(u'获取网页出错，10s将倒数第',num_retries,u'次')
#                    return self.get(url,timeout,num_retries-1)
#                else:
#                    print(u'开始使用代理')
#                    time.sleep(10)
#                    proxyIp = random.choice(self.ipList)
#                    proxy = {proxyIp['type']:'http://'+proxyIp['ip']+':'+str(proxyIp['port'])}
#                    return self.get(url,timeout,proxy,)
#                            
#        else : ##代理不为空
        try:
            proxyIp = random.choice(self.proxyLs)
            proxy = {proxyIp[1]:'http://'+proxyIp[2]+':'+str(proxyIp[3])}
            content = requests.get(url,headers = headers,proxies = proxy,timeout = timeout)
            if content.status_code == requests.codes.ok:
                return content
            else:
                print(u'重新选择代理...')
                return self.get(url,timeout,host,referer)
        except Exception as e:
            traceback.print_exc()
            time.sleep(10)
            proxyIp = random.choice(self.proxyLs)
            proxy = {proxyIp[1]:'http://'+proxyIp[2]+':'+str(proxyIp[3])}
            print(u'正在更换代理......')
            print(u'当前使用的代理是：',proxy)
            return self.get(url,timeout,host,referer,proxy,)
request = download()
#content = request.get('https://www.baidu.com/',5,'www.baidu.com',None)
#print(content.text)