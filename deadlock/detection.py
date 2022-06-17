import numpy as np
from typing import *


def detect(alloc: np.ndarray, request: np.ndarray, available: np.ndarray) -> Union[np.ndarray, None]:
    '''检测是否有死锁，若无则返回执行序列'''
    n = len(alloc)  # 进程数
    seq = np.empty(n)
    finished = np.zeros(n, dtype=np.bool)
    for i in range(n):
        found = False
        for j in range(n):
            if not finished[j] and np.all(request[j] <= available):
                found = True
                available += alloc[j]
                seq[i] = j
                finished[j] = True
                break
        if not found:
            return None
    return seq


if __name__ == "__main__":
    alloc = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 3], [2, 1, 1], [0, 0, 2]])
    request = np.array([[0, 0, 0], [2, 0, 2], [0, 0, 0], [1, 0, 0], [0, 0, 2]])
    available = np.array([0, 0, 0])
    print(detect(alloc, request, available))