# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 23:42:31 2018

@author: jack
"""

import re
import traceback
import threading
import time
import requests
from lxml import etree
from lxml import html
from saveMysql import db
from animequeue import queue
from proxyDownLoad import request

# class animeinfo():
    
#     def __init__(self):
#          #self.animeLs = db.execute('select * from animeinfo',None);
#          self.headers = {'User-Agent':'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'}
#     #获取动漫类型
#     def getanmieType(self):
#         content = self.request('http://donghua.dmzj.com/acg_donghua/')
#         if content.status_code != requests.codes.ok:
#             print(u'获取失败!请检测网络连接情况或者是否能正常访问该网站...')
#             return
#         result = self.xpathresolve(content,"//a[@name='nav_item_category']/@id|//a[@name='nav_item_category']/@title")
#         typeList = []
#         typeLs = []
#         for i in range(0,len(result),2):
#             typeList.append(result[i:i+2])
#         if len(typeList)>0:
#             for i in typeList:
#                 type_id = re.sub('\D', '', str(i[0]))
#                 if type_id:
#                     typeLs.append([int(type_id),i[1]])
#                 else:
#                     print(i[0],i[1])
#         try:
#             db.executemany('insert into anime_type(ANIME_TYPE_ID,ANIME_TYPE_NAME) values (%s,%s)',typeLs)
#         except Exception as e:
#             traceback.print_exc()
#             db.rollback()
#         else:
#             pass
#         finally:
#             db.commit()
#             db.close()
#     def getcontent(self):
#         db.execute('select ANIME_LINE from anime_home where ID = 15 limit 1',None)
#         animeurl = db.fetchone()
#         content = self.request("http://donghua.dmzj.com/donghua_info/3203.html")
#         if content.status_code != requests.codes.ok:
#             print(u'获取失败!请检测网络连接情况或者是否能正常访问该网站...')
#             return
#         anime_html = self.xpathresolve(content)
#         anime_id_text = anime_html.xpath("//span[@id='comic_id']")
#         if anime_id_text:
#             #获取动漫id
#             anime_id = anime_id_text[0].text
#             #获取动漫名称
#             anime_name = anime_html.xpath("//span[@class='anim_title_text']/h1")[0].text
#             #获取动漫描述
#             anime_desc = anime_html.xpath("//span[@id='gamedescall']")[0].text.strip()
#             anime_base_info_li = anime_html.xpath("//div[@class='anim_attributenew']/div[2]/ul/li")
#             #获取动漫首播时间
#             anime_premiere = ''
#             #获取动漫类型
#             anime_type = ''
#             for result in anime_base_info_li:
#                 result_split = result.text.split(":")
#                 if result_split[0].strip() == '首播时间':
#                     anime_premiere = result_split[1].strip()
#                 if result_split[0].strip() == '剧情类型':
#                     anime_type_html = html.fromstring(etree.tostring(result).decode('utf-8'))
#                     anime_type_ls = anime_type_html.xpath("//li/a/@href")
#                     #列表推导式获取类型
#                     anime_type = '-'.join([re.search('(?<=/acg_donghua/0-0-0-0-all-)\d+',i).group(0) for i in anime_type_ls])
#             #获取动漫评分
#             anime_score = anime_html.xpath("//span[@class='points_text']")[0].text.strip()
#             #获取动漫评分人数
#             anime_score_number = re.sub('\D', '', anime_html.xpath("//span[@id='score_count_span']")[0].text.strip())
#             print(anime_score_number)

#         else:
#             print(u'404错误!')
        
    
#     #多线程获取
#     def getanimeinfobythread(self):
#         self.getcontent()
#     #解析html
#     def xpathresolve(self,content):
#         page = html.fromstring(content.text)
#         return page
    
#     def request(self,url):
#         content=requests.get(url,headers=self.headers)
#         content.encoding='utf-8'
#         return content

# animeinfo = animeinfo()
# animeinfo.getanimeinfobythread()
def thread_craler(max_threads=10):

    queue1 = queue.pop()

    lock = threading.Lock() #建立一个锁

    def requestinfo():
        while True:
            if not queue1.empty():
                anime_info = queue1.get()
            else:
                return
            try:
                print('正在爬取',anime_info[1])
                content = requestbyproxy(anime_info[1],anime_info[1])
                lock.acquire()  
                getcontent(content)
                lock.release()  
            except Exception as e:
                traceback.print_exc()
            else:
                pass
            finally:
                 #线程告知任务完成使用task_done
                 queue1.task_done()

    def getcontent(content):
        if content.status_code != requests.codes.ok:
            print(u'获取失败!请检测网络连接情况或者是否能正常访问该网站...')
            return
        anime_html = xpathresolve(content)
        anime_id_text = anime_html.xpath("//span[@id='comic_id']")
        if anime_id_text:
            #获取动漫id
            anime_id = anime_id_text[0].text
            #获取动漫名称
            anime_name = anime_html.xpath("//span[@class='anim_title_text']/h1")[0].text
            #获取动漫描述
            anime_desc = anime_html.xpath("//span[@id='gamedescall']")[0].text.strip()
            anime_base_info_li = anime_html.xpath("//div[@class='anim_attributenew']/div[2]/ul/li")
            #获取动漫首播时间
            anime_premiere = ''
            #获取动漫类型
            anime_type = ''
            for result in anime_base_info_li:
                result_split = result.text.split(":")
                if result_split[0].strip() == '首播时间':
                    anime_premiere = result_split[1].strip()
                if result_split[0].strip() == '剧情类型':
                    anime_type_html = html.fromstring(etree.tostring(result).decode('utf-8'))
                    anime_type_ls = anime_type_html.xpath("//li/a/@href")
                    #列表推导式获取类型
                    anime_type = '-'.join([re.search('(?<=/acg_donghua/0-0-0-0-all-)\d+',i).group(0) for i in anime_type_ls])
            #获取动漫评分
            anime_score = anime_html.xpath("//span[@class='points_text']")[0].text.strip()
            #获取动漫评分人数
            anime_score_number = re.sub('\D', '', anime_html.xpath("//span[@id='score_count_span']")[0].text.strip())
            print(anime_desc)
        else:
            print(u'404错误!')

    #解析html
    def xpathresolve(self,content):
        page = html.fromstring(content.text)
        return page

    def requestbyproxy(url,referer):
        content = request.get(url,5,'s.acg.dmzj.com',referer)
        content.encoding = 'utf-8'
        return content

    threads = []
    for i in range(10):
        thread = threading.Thread(target=requestinfo)
        thread.setDaemon(True)
        thread.start() #启动线程
        threads.append(thread)
        time.sleep(1)

    for t in threads:
        t.join()

def test():
    queue1 = queue.pop()
    print(queue1.get())

if __name__ == "__main__":
    thread_craler()