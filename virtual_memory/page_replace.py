from typing import *
import numpy as np
from matplotlib import pyplot as plt


def FIFO(frame_size: int, refstr: List[int]) -> List[int]:
    '''返回结果是每次置换的帧号'''
    frames = [-1] * frame_size
    repl = []
    i = 0
    for p in refstr:
        if not p in frames:
            repl.append(i)
            frames[i] = p
            i = (i + 1) % frame_size
        else:
            repl.append(-1)
    return repl


def OPT(frame_size: int, refstr: List[int]) -> List[int]:
    frames = [-1] * frame_size
    repl = []
    for i, p in enumerate(refstr):
        if not p in frames:
            j = np.argmax([refstr.index(x, i) if x in refstr[i :] else len(refstr) for x in frames])
            repl.append(j)
            frames[j] = p
        else:
            repl.append(-1)
    #print(repl)
    return repl


def LRU_c(frame_size: int, refstr: List[int]) -> List[int]:
    frames = [-1] * frame_size
    repl = []
    counter = np.full(np.max(refstr) + 1, -1)
    for i, p in enumerate(refstr):
        if not p in frames:
            j = np.argmin([counter[x] if x in frames and x != -1 else -1 for x in frames])
            repl.append(j)
            frames[j] = p
        else:
            repl.append(-1)
        counter[p] = i
    return repl


def LRU_s(frame_size: int, refstr: List[int]) -> List[int]:
    frames = [-1] * frame_size
    repl = []
    stack = list(range(frame_size))  # 存frame的第几个
    for i, p in enumerate(refstr):
        if not p in frames:
            j = stack[0]
            del stack[0]
            repl.append(j)
            frames[j] = p
        else:
            repl.append(-1)
            j = frames.index(p)
            stack.remove(j)
        stack.append(j)
    return repl


def LRU_arb(frame_size: int, refstr: List[int]) -> List[int]:
    frames = [-1] * frame_size
    repl = []
    arb = np.full(np.max(refstr) + 1, 0)
    rb = np.zeros(np.max(refstr) + 1, dtype=np.int)
    for i, p in enumerate(refstr):
        rb[p] = 1
        if not p in frames:
            j = np.argmin([arb[x] if x in frames and x != -1 else -1 for x in frames])
            repl.append(j)
            frames[j] = p
        else:
            repl.append(-1)
        if (i + 1) % 4 == 0:
            arb >>= 1
            arb |= rb << 7
    return repl


def LRU_clock(frame_size: int, refstr: List[int]) -> List[int]:
    frames = [-1] * frame_size
    repl = []
    rb = [0] * frame_size
    j = 0
    for i, p in enumerate(refstr):
        if not p in frames:
            # 找到第一个rb=0的，顺路改成0
            while rb[j] == 1:
                rb[j] = 0
                j = (j + 1) % frame_size
            # 现在rb[j]为0
            repl.append(j)
            frames[j] = p
            rb[j] = 1
            j = (j + 1) % frame_size  #指针后移
        else:
            rb[frames.index(p)] = 1
            repl.append(-1)
    return repl


def demo(frame_size: int, refstr: List[int], repl: List[int]) -> None:
    frames = [-1] * frame_size
    for i in range(len(refstr)):
        if repl[i] != -1:
            frames[repl[i]] = refstr[i]
            print(i, frames)
        else:
            print(i)


def demo2(frame_size: int, refstr: List[int], fun, **kwargs) -> None:
    demo(frame_size, refstr, fun(frame_size, refstr, **kwargs))


def randrefstr(high: int, length: int) -> List[int]:
    return list(np.random.randint(low=high, size=length))


def plotcomp(refstr: List[int], algos: list):
    for fun, label in algos:
        x = range(1, max(refstr) + 2)
        y = [len(refstr) - fun(x_, refstr).count(-1) for x_ in x]
        plt.plot(x, y, '-o', label=label)
    plt.ylim(bottom=0)
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    refstr = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]
    #demo(3, refstr, FIFO(3, refstr))
    #demo2(4, refstr, OPT)
    #demo2(3, [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1], LRU_arb)
    #demo2(3, [1, 4, 3, 1, 2, 5, 1, 4, 2, 1, 4, 5], LRU_clock)
    #print()
    plotcomp(
        randrefstr(20, 100),
        [
            (FIFO, "FIFO"),
            (OPT, "OPT"),
            (LRU_c, "LRU"),
            #(LRU_s, "LRU_stack"),
            (LRU_arb, "LRU_arb"),
            (LRU_clock, "LRU_clock"),
        ]
    )
