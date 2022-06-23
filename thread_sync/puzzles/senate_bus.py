import random
from threading import Lock, Semaphore, Thread
import time

C = 5
waiting = 0
mutex = Semaphore(1)
bus = Semaphore(0)
boarded = Semaphore(0)
riders = []

print_mutex = Lock()


def tprint(str):
    print_mutex.acquire()
    print(str, flush=True)
    print_mutex.release()


def Bus(id):
    global waiting, riders
    time.sleep(random.random())
    tprint(f"Bus {id}")

    # 排队的人不允许再变化，能上车的都是过了 mutex 的
    mutex.acquire()
    riders = []
    for i in range(min(waiting, C)):
        bus.release()
        boarded.acquire()

    waiting = max(waiting - C, 0)
    tprint(f"Depart {id}: {riders}")
    mutex.release()


def Rider(id):
    global waiting
    time.sleep(random.random())
    tprint(f"Rider {id}")

    mutex.acquire()
    waiting += 1
    mutex.release()

    bus.acquire()
    riders.append(id)
    #mutex.acquire()
    tprint(f"Board {id}")
    #mutex.release()
    boarded.release()


if __name__ == "__main__":
    for i in range(5):
        Thread(target=Bus, args=[i]).start()
    for i in range(40):
        Thread(target=Rider, args=[i]).start()
