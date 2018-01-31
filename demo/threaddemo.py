import time
from multiprocessing import Pool
from multiprocessing.dummy import Pool as TheaderPool

def test4():
    for n in range(1000000):
        def test5(i):
            n += i
    tpool = TheaderPool(processes=1)
    tpool.map_async(test5,range(1000000))
    tpool.close()
    tpool.join()
start = time.clock()
test4()
print(str(time.clock()-start) + "秒")