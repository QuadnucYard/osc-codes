/**
 * @file hardware_testandset.cpp
 * @author QuadnucYard
 * @brief 临界区问题的硬件解决方案（testandset）：满足有空让进，不满足有限等待（每次放进的不确定）
 * @version 0.1
 * @date 2022-06-16
 *
 * @copyright Copyright (c) 2022
 *
 */
#include "common_sync.h"

const int N = 5, M = 10000;
std::atomic_flag lock;
int cnt;

void process(int i) {
	using namespace std::chrono_literals;
	for (int _i = 0; _i < M; _i++) {
		while (lock.test_and_set());
		//printf("Process %d\n", i);
		++cnt;
		lock.clear();
		//std::this_thread::sleep_for(100ms);
	}
}

#include "critsec_main.cpp"