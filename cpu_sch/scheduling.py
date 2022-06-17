from copy import copy
import numpy as np
from typing import *
from matplotlib import pyplot as plt
from queue import PriorityQueue
from enum import Enum


class Policy(Enum):
    Default = 0
    FCFS = 1
    SJF = 2
    RR = 3


class Job:
    def __init__(self, id, arrival, burst, priority=0) -> None:
        self.id = id
        self.arrival = arrival
        self.burst = burst
        self.priority = priority

    def __lt__(self, other) -> bool:
        if self.priority != other.priority: return self.priority < other.priority
        if self.arrival != other.arrival: return self.arrival < other.arrival
        if self.burst != other.burst: return self.burst < other.burst
        return self.id < other.id

    def __str__(self) -> str:
        return f"Job({self.id},{self.arrival},{self.burst},{self.priority})"


def schedule(jobs: List[Job], preemptive: bool = False, policy=Policy.Default, time_quantuum: int = 100000) -> List[Tuple[int, int, int]]:
    '''优先级调度  列表参数为 (id, arrival, burst, priority)'''
    # 重排, (priority,arrival,burst,id)
    if policy == Policy.FCFS:
        preemptive = False
    coming = [*sorted(jobs, key=lambda j: (j.arrival, j.burst)), None]  # 补一个哨兵项
    seq = []
    waiting = PriorityQueue()
    now, due = 0, 0
    running: Job = None
    for job in coming:
        # 复制一份
        if job:
            newp: Job = copy(job)
            if policy == Policy.FCFS:
                newp.priority = 0
            if policy == Policy.SJF:
                newp.priority = newp.burst
            arrival = newp.arrival
        else:
            arrival = 0x7fffffff
        # 处理在新job前可以结束的任务
        while running and min(due, now + time_quantuum) <= arrival:
            if running.burst <= time_quantuum:
                seq.append((now, running.burst, running.id))
                now = due
            else:
                seq.append((now, time_quantuum, running.id))
                now += time_quantuum
                running.arrival += time_quantuum * len(jobs)
                running.burst -= time_quantuum
                if policy == Policy.SJF: running.priority = running.burst
                waiting.put(running)
            if not waiting.empty():
                running = waiting.get()
                due = now + running.burst
            else:
                running = None
        if not newp:
            break
        if running:
            # 开始运行
            if newp.priority < running.priority and preemptive:
                if newp.arrival != now:
                    seq.append((now, newp.arrival - now, running.id))
                running.burst = due - newp.arrival
                if policy == Policy.SJF: running.priority = running.burst
                waiting.put(running)
                waiting.put(newp)
                running = waiting.get()
                now = newp.arrival
            else:
                waiting.put(newp)
        else:
            running = newp
            now = newp.arrival
        due = now + running.burst
    return seq


def plotseq(seq: List[Tuple[int, int, int]], y: int, jobs: List[Job] = None) -> None:
    '''
    @param seq (开始，长度, 编号) 序列 \\
    考虑评估指标：turnaround, waiting, response
    '''
    # pid离散化
    all_pid = list({span[2] for span in seq})
    n = len(all_pid)
    rank = {p[1]: p[0] for p in zip(range(n), all_pid)}
    # 统计时间
    first_time: Dict[int, int] = {}
    last_time: Dict[int, int] = {j.id: 0 for j in jobs}
    for span in seq:
        if span[2] not in first_time:
            first_time[span[2]] = span[0]
        last_time[span[2]] = span[0] + span[1]
    # 画图
    turnaround_time = sum([last_time[j.id] - j.arrival for j in jobs])
    waiting_time = sum([last_time[j.id] - j.arrival - j.burst for j in jobs])
    response_time = sum([first_time[j.id] - j.arrival for j in jobs])
    for i, span in enumerate(seq):
        pid = span[2]
        plt.barh(y, span[1], left=span[0], color=plt.get_cmap('rainbow')(rank[pid] / n), label=pid, linewidth=1, edgecolor="gray")
        plt.text(span[0] + span[1] / 2, y, f"P{pid}", verticalalignment="center", horizontalalignment="center")
    plt.text(plt.xlim()[1], y, f" Turnaround: {turnaround_time} \n Waiting: {waiting_time}\n Response: {response_time}", verticalalignment="center")


def plotall(seqs: List[Tuple[List[Tuple[int, int, int]], str]], common_jobs: List[Job]) -> None:
    #print(seqs)
    for i, seq in enumerate(seqs):
        plotseq(seq[0], i, common_jobs)
    plt.yticks(ticks=range(len(seqs)), labels=list(zip(*seqs))[1])
    plt.xlim(left=0)
    plt.grid(axis='x', which='both')
    plt.legend()
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    plt.show()


if __name__ == "__main__":
    jobs = [
        Job(1, 1, 5, -3),
        Job(2, 10, 5, -1),
        Job(3, 12, 7, -2),
        Job(4, 20, 2, -3),
        Job(5, 21, 9, -4),
        Job(6, 22, 2, -4),
        Job(7, 23, 5, -2),
        Job(8, 24, 2, -4),
    ]
    plotall(
        [
            (schedule(jobs, preemptive=True), "Priority-preemptive"),
            (schedule(jobs, preemptive=False), "Priority-nonpreemptive"),
            (schedule(jobs, policy=Policy.FCFS), "FCFS"),
            (schedule(jobs, preemptive=False, policy=Policy.SJF), "SJF-nonpreemptive"),
            (schedule(jobs, preemptive=True, policy=Policy.SJF), "SJF-preemptive"),
            #(schedule(jobs, policy=Policy.Default, time_quantuum=1), "RR-nonpreemptive"),
            (schedule(jobs, policy=Policy.Default, time_quantuum=1, preemptive=True), "RR-preemptive"),
            #(schedule(jobs, policy=Policy.Default, time_quantuum=2), "RR-nonpreemptive"),
            (schedule(jobs, policy=Policy.Default, time_quantuum=2, preemptive=True), "RR-preemptive"),
        ],
        jobs
    )
