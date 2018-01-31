import gevent
import sys
import  os
import time
import requests
sys.path.append(os.getcwd() + '/db')
sys.path.append(os.getcwd() + '/proxyrequest')
import traceback
from gevent import monkey; monkey.patch_all()
from gevent.queue import Queue
from saveMysql import db
from proxyDownLoad import request

class geventimg(object):
    def __init__(self):
        self.file_path = 'D:/animeimg/animeimg2/'
        self.queue = Queue()

    def getanimeimgurlfrommysql(self):
      try:
        if not os.path.exists(self.file_path):
            print ('文件夹',self.file_path,'不存在，重新建立')
            os.makedirs(self.file_path)
        db.execute('SELECT a.ANIME_ID,a.ANIME_IMAGE FROM anime_home a',None)
        records = db.fetchall()
        if records:
          for r in records:
              self.queue.put_nowait(r)
      except Exception as e:
        pass
      else:
        pass
      finally:
        pass
      pass
    def downloadimg(self,n):
        while not self.queue.empty():
            try:
                animeimg = self.queue.get_nowait()
                r = self.url_open('http://donghua.dmzj.com{}'.format(animeimg[1]))
                # print(animeimg)
                anime_img_name = self.file_path +'animepic_{}.jpg'.format(animeimg[0])
                with open(anime_img_name,"wb") as f:
                    f.write(r.content)
                    f.flush()
                f.close()
                gevent.sleep(1)
            except Exception as e:
              traceback.print_exc()
            finally:
              pass
    def url_open(self,url):
      """
      爬取网页
      """
      req = request.get(url,5,'donghua.dmzj.com',None)
      return req

    def main(self):
      gevent.spawn(self.getanimeimgurlfrommysql).join()
      # gevent.spawn(self.downloadimg).join()

      pool = gevent.pool.Pool(5)
      threads = []
      for r in range(5):
          threads.append(pool.spawn(self.downloadimg,r))
      gevent.joinall(threads)

if __name__ == '__main__':
  geventimg = geventimg()
  geventimg.main()