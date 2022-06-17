/**
 * @file dining_philosophers_1.cpp
 * @author QuadnucYard
 * @brief 哲学家吃饭问题：房间最多容纳N-1人
 * @version 0.1
 * @date 2022-06-16
 *
 * @copyright Copyright (c) 2022
 *
 */
#include <iostream>
#include "common_sync.h"

const int N = 5;
std::binary_semaphore chopsticks[N]{ std::binary_semaphore(1),  std::binary_semaphore(1),  std::binary_semaphore(1),  std::binary_semaphore(1),  std::binary_semaphore(1) };
std::counting_semaphore<N - 1> room(N - 1);

void philosopher(int i) {
	while (true) {
		std::this_thread::sleep_for(random_ms(10, 100));
		printf("Philosopher %d: Want to eat\n", i);

		room.acquire();
		chopsticks[i].acquire();
		chopsticks[(i + 1) % N].acquire();

		printf("Philosopher %d: Eating\n", i);

		chopsticks[i].release();
		chopsticks[(i + 1) % N].release();
		room.release();
	}
}

#include "dining_philosophers_main.cpp"