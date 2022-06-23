import random
from threading import Barrier, Lock, Semaphore, Thread
import time

mutex = Semaphore(1)
hready = Semaphore(0)
oready = Semaphore(0)
barrier = Barrier(3)  # 这个应该可以不需要
hcount = 0
ocount = 0
print_mutex = Lock()


def tprint(str, *args, **kwargs):
    with print_mutex:
        print(str, *args, **kwargs)


def hthread(id):
    global hcount, ocount
    time.sleep(random.random())
    tprint(f"H {id}")
    mutex.acquire()
    hcount += 1
    if hcount >= 2 and ocount >= 1:
        hready.release()
        hready.release()
        hcount -= 2
        oready.release()
        ocount -= 1
    else:
        mutex.release()
    hready.acquire()
    # 这样有一个问题，无法知道对方放进来的是什么
    tprint(f"makewater H {id}")
    #barrier.wait()


def othread(id):
    global hcount, ocount
    time.sleep(random.random())
    tprint(f"O {id}")
    mutex.acquire()
    ocount += 1
    if hcount >= 2 and ocount >= 1:
        hready.release()
        hready.release()
        hcount -= 2
        oready.release()
        ocount -= 1
    else:
        mutex.release()
    oready.acquire()
    tprint(f"makewater O {id}")
    #barrier.wait()
    mutex.release()


if __name__ == "__main__":
    for i in range(20):
        Thread(target=hthread, args=[i]).start()
    for i in range(10):
        Thread(target=othread, args=[i]).start()
