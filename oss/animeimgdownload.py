# -*- coding: utf-8 -*-
import sys
import  os
import threading
sys.path.append(os.getcwd() + '/db')
import traceback
from queue import Queue
from saveMysql import db

def animeimgdownload():
    file_path = 'D:/animeimg'
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
          if not queue.empty():
              animeimg = queue.get()
              lock
              print(animeimg)
    
    getanimeimgurlfrommysql()
    threads = []
    for i in range(10):
        thread = threading.Thread(target=downloadimg)
        thread.setDaemon(True)
        thread.start()
        threads.append(thread)
        time.sleep(3)
    for t in threads:
        t.join()
if __name__ == "__main__":
    animeimgdownload()