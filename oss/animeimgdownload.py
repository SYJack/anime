# -*- coding: utf-8 -*-
import sys
import  os
import time
import threading
import requests
sys.path.append(os.getcwd() + '/db')
sys.path.append(os.getcwd() + '/proxyrequest')
import traceback
from queue import Queue
from saveMysql import db
from proxyDownLoad import request

def animeimgdownload():
    file_path = 'F:/python/animeimg2/'
    queue = Queue()
    #同步锁装饰器  
    lock = threading.Lock()
    def getanimeimgurlfrommysql():
      try:
        db.execute('SELECT a.ANIME_ID,a.ANIME_IMAGE FROM anime_home a',None)
        records = db.fetchall()
        if records:
          for r in records:
              queue.put(r)
        if not os.path.exists(file_path):
            print ('文件夹',file_path,'不存在，重新建立')
            os.makedirs(file_path)
      except Exception as e:
        pass
      else:
        pass
      finally:
        pass
      pass
    def downloadimg():
      while True:
          try:
            if not queue.empty():
              animeimg = queue.get()
              r = url_open('http://donghua.dmzj.com{}'.format(animeimg[1]))
              # print(animeimg)
              lock.acquire()#获得锁
              if r.status_code == requests.codes.ok:
                anime_img_name = file_path +'animepic_{}.jpg'.format(animeimg[0])
                with open(anime_img_name,"wb") as f:
                    f.write(r.content)
                    f.flush()
                f.close()
                queue.task_done()
                time.sleep(0.5)
              lock.release() #释放锁
            else:
              break
          except Exception as e:
            traceback.print_exc()
          finally:
            pass
    def url_open(url):
      """
      爬取网页
      """
      req = request.get(url,5,'donghua.dmzj.com',None)
      return req

    
    getanimeimgurlfrommysql()
    threads = []
    for i in range(10):
        thread = threading.Thread(target=downloadimg)
        thread.setDaemon(True)
        thread.start()
        threads.append(thread)
        time.sleep(1)

    for t in threads:
        t.join()
if __name__ == "__main__":
    animeimgdownload()