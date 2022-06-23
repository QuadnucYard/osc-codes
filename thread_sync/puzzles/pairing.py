import random
from threading import Lock, Semaphore, Thread
import time

mutex = Semaphore(1)
num_l = 0
num_f = 0
leader = Semaphore(0)
follower = Semaphore(0)
pairing = Semaphore(1)
print_mutex = Lock()
pair = [-1, -1]


def tprint(values, *args, **kwargs):
    with print_mutex:
        print(values, *args, **kwargs)


def Leader(id):
    time.sleep(random.random() + 1)
    tprint(f"Leader enter {id}")
    follower.release()
    leader.acquire()
    tprint(f"Dance leader {id}")


def Follower(id):
    time.sleep(random.random())
    tprint(f"Follower enter {id}")
    leader.release()
    follower.acquire()
    tprint(f"Dance follower {id}")


if __name__ == "__main__":
    for i in range(5):
        Thread(target=Leader, args=[i]).start()
    for i in range(5):
        Thread(target=Follower, args=[i]).start()
