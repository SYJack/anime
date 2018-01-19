# -*- coding: utf-8 -*-
"""

@author: jack
"""
import traceback
import time
from queue import Queue
from saveMysql import db

class animequeue(object):
	"""docstring for ClassName"""

    # OUTSTANDING = 0 ##初始状态
    # PROCESSING = 1 ##正在下载状态
    # COMPLETE = 2 ##下载完成状态

	def __init__(self, timeout=300000):
		self.timeout = timeout
		self.queue = Queue()

	def __bool__(self):
		record = db.execute('SELECT 1 FROM anime_home a WHERE a.ANIME_INFO_DOWNLOAD_STATUS != 2 LIMIT 1',None)
		return True if record else False

	def pop(self):
		try:
			db.execute('SELECT a.ID,a.ANIME_LINE,a.ANIME_INFO_DOWNLOAD_STATUS FROM anime_home a WHERE a.ANIME_INFO_DOWNLOAD_STATUS = 0',None)
			records = db.fetchall()
			db.execute('UPDATE anime_home a SET a.ANIME_INFO_DOWNLOAD_STATUS = 1 WHERE a.ANIME_INFO_DOWNLOAD_STATUS = 0',None)
			if records:
				for r in records:
					self.queue.put(r)
				return self.queue
			# else:
			# 	self.repair()
			# 	raise KeyError
		except Exception as e:
			db.rollback()
			raise e
		finally:
			db.commit()

	def peek(self):
		record = db.execute('SELECT ID FROM anime_home a WHERE a.ANIME_INFO_DOWNLOAD_STATUS != 2 LIMIT 1',None)
		return record

	def complete(self, animeid):
		"""这个函数是更新已完成的URL完成"""
		try:
			db.execute('UPDATE anime_home a SET a.ANIME_INFO_DOWNLOAD_STATUS = 2 where a.ANIME_ID = %s' % (animeid),None)
		except Exception as e:
			db.rollback()
			raise e
		finally:
			db.commit()

	def repair(self):
		try:
			db.execute('SELECT h.* FROM anime_home h LEFT JOIN anime_info i on (h.ANIME_ID = i.ANIME_ID) WHERE i.ANIME_ID IS NOT NULL',None)
			records = db.fetchall()
			if records:
				for index,r in enumerate(records):
					db.execute('UPDATE anime_home a SET a.ANIME_INFO_DOWNLOAD_STATUS = 2 WHERE a.ID = %s' % (r[0]),None)
			db.execute('UPDATE anime_home h SET h.ANIME_INFO_DOWNLOAD_STATUS = 0 WHERE h.ANIME_INFO_DOWNLOAD_STATUS =1',None)
		except Exception as e:
			db.rollback()
			raise e
		finally:
			db.commit()
queue = animequeue()