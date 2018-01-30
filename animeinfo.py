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
from db.saveMysql import db
from animequeue.animequeue import queue
from proxyrequest.proxyDownLoad import request

def thread_craler(max_threads=10):
    queue1 = queue.pop()
    lock = threading.Lock() #建立一个锁

    def requestinfo():
        while True:
            if not queue1.empty():
                anime_info = queue1.get()
            else:
                print("进入循环检验")
                return
            try:
                # 代理爬取
                content = requestbyproxy(anime_info[1],anime_info[1])
                # content = request(anime_info[1])
                if content:
                    print('正在爬取',anime_info[1])
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

            try:
                db.execute('INSERT INTO anime_info(ANIME_ID,ANIME_NAME,ANIME_DESC,ANIME_TYPE_ID_LS,ANIME_PREMIERE,ANIME_SCORE,ANIME_SCORE_NUMBER) VALUES (%s,%s,%s,%s,%s,%s,%s)',(int(anime_id),anime_name,anime_desc,anime_type,anime_premiere,anime_score,int(anime_score_number)))
            except Exception as e:
                traceback.print_exc()
                db.rollback()
            finally:
                print(u'爬取成功...')
                queue.complete(int(anime_id))
                db.commit()
        else:
            print(u'404错误!')
    #解析html
    def xpathresolve(content):
        page = html.fromstring(content.text)
        return page

    def requestbyproxy(url,referer):
        content = request.get(url,5,'s.acg.dmzj.com',referer)
        content.encoding = 'utf-8'
        return content

    # def request(url):
    #     content=requests.get(url,headers={'User-Agent':"Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"})
    #     content.encoding='utf-8'
    #     return content

    threads = []
    db.conn()
    for i in range(10):
        thread = threading.Thread(target=requestinfo)
        thread.setDaemon(True)
        thread.start() #启动线程
        threads.append(thread)
        time.sleep(3)

    for t in threads:
        t.join()
    db.close()

def test():
    queue1 = queue.pop()
    print(queue1.get())

if __name__ == "__main__":
    thread_craler()
    time.sleep(5)
    if queue.peek() == 0:
      print("完成")
    else:
      queue.repair()
      print("重置完成")
    # thread_craler()
    # r = queue.peek()
    # print(r)