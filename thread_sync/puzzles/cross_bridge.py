import random
from threading import Lock, Semaphore, Thread
import time

ab = 0
ba = 0
s1 = Semaphore(1)
s2 = Semaphore(1)
sab = Semaphore(1)

print_mutex = Lock()


def tprint(str):
    print_mutex.acquire()
    print(str, flush=True)
    print_mutex.release()


def Pab(id):
    global ab
    time.sleep(random.random())
    #tprint(f"Pab {id}")

    s1.acquire()
    if ab == 0: sab.acquire()
    ab += 1
    s1.release()

    tprint(f"Go A->B {id}")

    s1.acquire()
    ab -= 1
    if ab == 0: sab.release()
    s1.release()


def Pba(id):
    global ba
    time.sleep(random.random())
    #tprint(f"Pab {id}")

    s2.acquire()
    if ba == 0: sab.acquire()
    ba += 1
    s2.release()

    tprint(f"Go B->A {id}")

    s2.acquire()
    ba -= 1
    if ab == 0: sab.release()
    s2.release()


if __name__ == "__main__":
    for i in range(20):
        Thread(target=Pab, args=[i]).start()
    for i in range(20):
        Thread(target=Pba, args=[i]).start()
