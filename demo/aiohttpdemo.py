import aiohttp
import asyncio
import async_timeout
import sys
import os
sys.path.append(os.getcwd() + '/db')
sys.path.append(os.getcwd() + '/proxyrequest')
from saveMysql import db
# from asyncproxydownload import asyncrequest

class aiohttpdemo(object):
  def __init__(self):
      self.animequeue=None
      self.file_path = 'D:/animeimg/animeimg/'
      self.coro_count = 20
  
  async def get_animequeue(self):
      db.execute('SELECT a.ANIME_ID,a.ANIME_IMAGE FROM anime_home a',None)
      records = db.fetchall()
      animequeue = asyncio.Queue()
      if records:
        for r in records:
            await animequeue.put(r)
        self.animequeue = animequeue
        if not os.path.exists(self.file_path):
            print ('文件夹',self.file_path,'不存在，重新建立')
            os.makedirs(self.file_path)
        return animequeue

  async def downloadimg(self, anime_queue):
      if isinstance(anime_queue,asyncio.Queue()):
        while not self.animequeue.empty():
            try:
                animeimg = await anime_queue.get()
                r = self.url_open('http://donghua.dmzj.com{}'.format(animeimg[1]))
                # print(animeimg)
                if r.status_code == 200:
                  anime_img_name = file_path +'animepic_{}.jpg'.format(animeimg[0])
                  async with open(anime_img_name,"wb") as f:
                      await f.write(r.content)
                  await asyncio.sleep(0.5)
            except Exception as e:
              traceback.print_exc()
            finally:
              pass
  def url_open(self,url):
      """
      爬取网页
      """
      req = asyncrequest._asyncget(url,5,'donghua.dmzj.com',None)
      return req

  async def fetch(self,session, url):
      with async_timeout.timeout(5):
          async with session.get(url,proxy="http://203.210.7.45:80") as response:
              return await response.text()

  async def request(self):
      async with aiohttp.ClientSession() as session:
          html = await self.fetch(session, 'http://www.baidu.com/')
          print(html)
  
  async def start(self):
      anime_queue = await self.get_animequeue()
      to_validate=[self.downloadimg(anime_queue) for _ in range(self.coro_count)]
      await asyncio.wait(to_validate)
  def main(self):
      loop = asyncio.get_event_loop()
      loop.run_until_complete(self.request())

if __name__ == '__main__':
    aiohttpdemo = aiohttpdemo()
    aiohttpdemo.main()
  