# -*- coding: utf-8 -*-
"""
@author: jack
"""

import time
import datetime
import traceback
import hashlib
import json
import sys
import os
sys.path.append(os.getcwd() + '/db')
sys.path.append(os.getcwd() + '/proxyrequest')
from saveMysql import db
from proxyDownLoad import request

class animetimetable(object):
  def __init__(self):
      pass
  
  def getData(self,url):
      content = self.requestbyproxy(url)
      dataJson = json.loads(content.text)
      if dataJson['status'] == 200:
        if len(dataJson['data']['page']['list']):
            values=[]
            for i in dataJson['data']['page']['list']:
                anime_bid = int(i['bid'])
                anime_name = i['title']
                anime_cover = i['cover']
                anime_vertical_cover = i['verticalCover']
                anime_play_date = i['playDate']
                anime_play_time = i['playTime']
                anime_origin_time = i['originTime']
                anime_play_site = i['playSite']
                anime_origin_station = i['originStation']
                anime_play_url = i['playUrl']
                anime_play_episode = i['episode']
                values.append([anime_bid,None,anime_name,anime_cover,anime_vertical_cover,anime_play_date,anime_play_time,anime_origin_time,anime_play_site,anime_origin_station,anime_play_url,anime_play_episode])
            try:
              db.executemany('insert into anime_timetable(ANIME_BID,ANIME_ID,ANIME_NAME,ANIME_COVER,ANIME_VERTICAL_COVER,ANIME_PLAY_DATE,ANIME_PLAY_TIME,ANIME_ORIGIN_TIME,ANIME_PLAY_SITE,ANIME_ORIGIN_STATION,ANIME_PLAY_URL,ANIME_PLAY_EPISODE) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',values)
            except Exception as e:
              traceback.print_exc()
            finally:
              db.commit()
              time.sleep(1)
        else:
            pass
      else:
        pass

  def requestbyproxy(self,url):
      content = request.get(url,5,'app.anitama.net','http://www.anitama.cn/')
      content.encoding = 'utf-8'
      return content
  def main(self):
      self.getData('https://app.anitama.net/bangumi?pageNo=1&isEnd=&year=')
      # content = self.requestbyproxy('https://app.anitama.net/bangumi?pageNo=1&isEnd=&year=')
      # dataJson = json.loads(content.text)
      # for p in range(1,(round(int(dataJson['data']['page']['totalCount'])/20)+1)):
      #     print(p)
      # for d in range(7):
      #     today = datetime.date.today()
      #     tomorrow = today + datetime.timedelta(days=d)
      #     self.getData('https://app.anitama.net/guide/{}'.format(tomorrow.strftime("%Y%m%d"))

if __name__ == '__main__':
  animetimetable = animetimetable()
  animetimetable.main()