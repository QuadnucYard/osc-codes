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


def tprint(str, *args, **kwargs):
    with print_mutex:
        print(str, *args, **kwargs)


def Leader(id):
    global num_f, num_l
    time.sleep(random.random())
    tprint(f"Leader enter {id}")
    mutex.acquire()  # 每次只能通过一个，顺带关门
    # 此时一定有一方缺人，不然不会再放其他人进
    num_l += 1
    if num_f > 0:  # 如果有 follower，配对并告知
        num_l -= 1
        num_f -= 1
        leader.release()  # 放一个 leader 来配对，就是自己
        follower.release()  # 放一个 follower 来配对
    else:  # 没有 follower，等 follower 出现
        mutex.release()  # 开门，让更多人进来
    leader.acquire()  # 等待 follower 的信号
    # 能走到这一步说明已经有配对上的 follower 了
    # 不会有多余的放进来因为有一方是恰好配对
    pairing.acquire()  # 告知已经配对的 follower 可以开始
    tprint(f"Dance leader {id}")
    mutex.release()  # 跳完了，开门


def Follower(id):
    global num_f, num_l
    time.sleep(random.random())
    tprint(f"Follower enter {id}")
    mutex.acquire()
    #tprint(num_f, num_l)
    num_f += 1
    if num_l > 0:
        num_l -= 1
        num_f -= 1
        leader.release()
        follower.release()
    else:
        mutex.release()
    follower.acquire()
    # 能走到这一步说明已经有配对上的 leader 了
    pairing.release()
    tprint(f"Dance follower {id}")


if __name__ == "__main__":
    for i in range(10):
        Thread(target=Leader, args=[i]).start()
    for i in range(10):
        Thread(target=Follower, args=[i]).start()
