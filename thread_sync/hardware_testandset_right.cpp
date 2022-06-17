/**
 * @file hardware_testandset.cpp
 * @author QuadnucYard
 * @brief 临界区问题的硬件解决方案（testandset）：成功解决
 * @version 0.1
 * @date 2022-06-16
 *
 * @copyright Copyright (c) 2022
 *
 */
#include "common_sync.h"

const int N = 5, M = 10000;
std::atomic_flag lock;
bool waiting[N];
int cnt;

void process(int i) {
	using namespace std::chrono_literals;
	bool key;
	for (int _i = 0; _i < M; _i++) {
		waiting[i] = true;
		key = true;
		while (waiting[i] && key) key = lock.test_and_set();
		waiting[i] = false;

		//printf("Process %d\n", i);
		++cnt;

		int j = (i + 1) % N;
		while (j != i && !waiting[j]) j = (j + 1) % N;
		if (j == i) lock.clear();
		else waiting[j] = false;

		//std::this_thread::sleep_for(100ms);
	}
}

#include "critsec_main.cpp"