/**
 * @file critsec_algo3.cpp
 * @author QuadnucYard
 * @brief 临界区问题算法3（Peterson）：解决临界区问题
 * @version 0.1
 * @date 2022-06-16
 *
 * @copyright Copyright (c) 2022
 *
 */
#include "common_sync.h"

const int N = 2, M = 10000;
int cnt;
bool flag[N];
int turn;

void process(int i) {
	using namespace std::chrono_literals;
	int j = 1 - i;
	for (int _i = 0; _i < M; _i++) {
		flag[i] = true;
		turn = j;
		while (flag[j] && turn == j);
		//printf("Process %d\n", i);
		++cnt;
		flag[i] = false;
		//std::this_thread::sleep_for(100ms);
	}
}

#include "critsec_main.cpp"