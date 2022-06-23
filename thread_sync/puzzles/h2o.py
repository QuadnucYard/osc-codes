import random
from threading import Barrier, Lock, Semaphore, Thread
import time

mutex = Semaphore(1)
h_wait = Semaphore(0)
o_wait = Semaphore(0)
count = 0

print_mutex = Lock()


def tprint(str, *args, **kwargs):
    with print_mutex:
        print(str, *args, **kwargs)


def hthread(id):
    global count
    time.sleep(random.random())
    tprint(f"H {id}")
    mutex.acquire()
    count += 1
    if count % 2 == 0:
        o_wait.release()  # H够了，告诉O可以合成
    mutex.release()
    h_wait.acquire()  # 等待O的通知
    tprint(f"makewater H {id}")


def othread(id):
    time.sleep(random.random())
    tprint(f"O {id}")
    o_wait.acquire()  # 等待H够
    tprint(f"makewater O {id}")
    h_wait.release()  # 告知2个H来合成
    h_wait.release()


if __name__ == "__main__":
    for i in range(20):
        Thread(target=hthread, args=[i]).start()
    for i in range(10):
        Thread(target=othread, args=[i]).start()
