/**
 * @file critsec_algo1.cpp
 * @author QuadnucYard
 * @brief 临界区问题算法1，满足互斥、有限等待，不满足有空让进。
 * @version 0.1
 * @date 2022-06-16
 *
 * @copyright Copyright (c) 2022
 *
 */
#include "common_sync.h"

const int N = 2, M = 10000;
int cnt;
int turn;

void process(int i) {
	using namespace std::chrono_literals;
	int j = 1 - i;
	for (int _i = 0; _i < M; _i++) {
		while (turn != i);
		//printf("Process %d\n", i);
		++cnt;
		turn = j;
		//std::this_thread::sleep_for(100ms);
	}
}

#include "critsec_main.cpp"