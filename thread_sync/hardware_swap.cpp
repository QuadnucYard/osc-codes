/**
 * @file hardware_swap.cpp
 * @author QuadnucYard
 * @brief 临界区问题的硬件解决方案（swap）：满足有空让进，不满足有限等待（每次放进的不确定）
 * @version 0.1
 * @date 2022-06-16
 *
 * @copyright Copyright (c) 2022
 *
 */
#include "common_sync.h"

const int N = 5, M = 10000;
std::atomic_bool lock(false);
int cnt;

void process(int i) {
	using namespace std::chrono_literals;
	bool key;
	for (int _i = 0; _i < M; _i++) {
		key = true;
		while (key) key = lock.exchange(key);
		//printf("Process %d\n", i);
		++cnt;
		lock = false;
		//std::this_thread::sleep_for(100ms);
	}
}

#include "critsec_main.cpp"