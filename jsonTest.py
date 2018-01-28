# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 17:21:04 2018

@author: Administrator
"""
import threading
import re
import time,traceback
import queue
import random
#data = re.sub("\D", "", "/donghua_info/2036.html")
#print(data)

L = ['219.138.58.188', '3128', 'HTTPS','219.138.58.200', '8080', 'HTTP','219.138.58.188', '3128', 'HTTPS','219.138.58.188', '3128', 'HTTPS','219.138.58.188', '3128', 'HTTPS','219.138.58.188', '3128', 'HTTPS','219.138.58.188', '3128', 'HTTPS','219.138.58.188', '3128', 'HTTPS','219.138.58.188', '3128', 'HTTPS','219.138.58.188', '3128', 'HTTPS','219.138.58.188', '3128', 'HTTPS','219.138.58.188', '3128', 'HTTPS']

#L = [x for x in range(1,100)]
#print(L)
#L2 = L[::3]
#print(L2)
#L3 = []
#for i in L2:
#    L3.append(L[i-1:i+2]) #切片是从0计数 所以从i-1 开始
#print(L3)
#L2 = []
#L2=[]
#L3=[]
#for i in range(1,len(L),3):
#    L2.append(i)
#for i in L2:
#    L3.append(L[i-1:i+2])
#print(L3)
#
#def partition_by_n(lst, n):
#    groups = []
#    for idx in range(len(lst)):
#        if idx%3 == 0:
#            groups.append(lst[idx:idx+3])
#    return groups
#for i in range(0,len(L),3):
#    print(L[i:i+3])

# print([L[i:i+3] for i in range(0,len(L),3)])


# class test():
#    def __init__(self):
#        self.lock = threading.Lock() #建立一个锁
       
#    def testThread(self,i):
#        self.lock.acquire()  
#        print(i)
#        time.sleep(1)
#        self.lock.release()  
       
#    def testbythread(self):
#            threads=[]
#            start = time.clock()
#            for i in range(1,11):
#                thread = threading.Thread(target=self.testThread,args=[i])
#                thread.setDaemon(True)
#                thread.start() #启动线程
#                threads.append(thread)
#            #结束线程
#            for thread in threads:
#                thread.join()
#            print(str(time.clock()-start) + "秒")
#            print(u'验证完毕')
# test = test()
# test.testbythread()
print("aaa")
#SHARE_Q = queue.Queue()  #构造一个不限制大小的的队列
#_WORKER_THREAD_NUM = 3   #设置线程个数
#
#class MyThread(threading.Thread) :
#
#    def __init__(self, func) :
#        super(MyThread, self).__init__()
#        self.func = func
#
#    def run(self) :
#        self.func()
#
#def worker() :
#    global SHARE_Q
#    while not SHARE_Q.empty():
#        item = SHARE_Q.get() #获得任务
#        print ("Processing : ", item)
#        time.sleep(1)
#
#def main() :
#    global SHARE_Q
#    threads = []
#    for task in range(5) :  #向队列中放入任务
#        SHARE_Q.put(task)
#    for i in range(_WORKER_THREAD_NUM) :
#        thread = MyThread(worker)
#        thread.start()
#        threads.append(thread)
#        time.sleep(1)
#    for thread in threads :
#        thread.join()
#
#if __name__ == '__main__':
#    main()


# def getUrl(todo):
#     todo = todo
#     def iters(todo=todo):
#         if todo!= []:
#             if todo[0][1] == 0:
#                 todo.pop(0)
#             url = todo[0][0] + str(todo[0][1])
#             todo[0][1] -= 1
#             print(url)
#             return str(url)
#     return iters

# urlF = getUrl([[ 'http://www.xicidaili.com/nn/',145]])
# print(urlF)
# def consumer():
#     r = ''
#     while True:
#         n = yield r
#         if not n:
#             return
#         print('[CONSUMER] Consuming %s...' % n)
#         r = '200 OK'

# def produce(c):
#     c.send(None)
#     n = 0
#     while n < 5:
#         n = n + 1
#         print('[PRODUCER] Producing %s...' % n)
#         r = c.send(n)
#         print('[PRODUCER] Consumer return: %s' % r)
#     c.close()

# c = consumer()
# produce(c)


# from saveMysql import db

# db.execute('select h.ANIME_ID from anime_home h LEFT JOIN anime_info i on h.ANIME_ID = i.ANIME_ID where i.ANIME_ID is not null AND h.ANIME_INFO_DOWNLOAD_STATUS = 1',None)
# record = db.fetchall()
# for r in record:
#     db.execute('UPDATE anime_home h SET h.ANIME_INFO_DOWNLOAD_STATUS = 2 WHERE h.ANIME_ID = %s' % (r[0]),None)
# db.commit()
# db.close()
from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')