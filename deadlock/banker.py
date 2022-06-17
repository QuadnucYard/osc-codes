import numpy as np
from typing import *


def banker(alloc: np.ndarray, maxa: np.ndarray, available: np.ndarray) -> Union[np.ndarray, None]:
    '''判断是否可以不死锁，若不死锁则返回执行序列'''
    n = len(alloc)  # 进程数
    seq = np.empty(n)
    finished = np.zeros(n, dtype=np.bool)
    for i in range(n):
        found = False
        for j in range(n):
            if not finished[j] and np.all(maxa[j] - alloc[j] <= available):
                found = True
                available += alloc[j]
                seq[i] = j
                finished[j] = True
                break
        if not found:
            return None
    return seq


if __name__ == "__main__":
    alloc = np.array([[0, 3, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]])
    maxa = np.array([[7, 7, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
    available = np.array([3, 3, 2])
    print(banker(alloc, maxa, available))