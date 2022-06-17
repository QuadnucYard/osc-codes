/**
 * @file dining_philosophers_2.cpp
 * @author QuadnucYard
 * @brief 哲学家吃饭问题：拿筷子为原子操作，需要加锁
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
std::binary_semaphore mutex(1);

void philosopher(int i) {
	while (true) {
		std::this_thread::sleep_for(random_ms(1, 20));
		printf("Philosopher %d: Want to eat\n", i);

		mutex.acquire();
		chopsticks[i].acquire();
		chopsticks[(i + 1) % N].acquire();
		mutex.release();

		printf("Philosopher %d: Eating\n", i);
		std::this_thread::sleep_for(random_ms(100, 100));
		printf("Philosopher %d: Finished\n", i);

		chopsticks[i].release();
		chopsticks[(i + 1) % N].release();
	}
}

#include "dining_philosophers_main.cpp"