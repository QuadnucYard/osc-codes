/**
 * @file common_sync.h
 * @author QuadnucYard
 * @brief 线程同步公用函数
 * @version 0.1
 * @date 2022-06-16
 *
 * @copyright Copyright (c) 2022
 *
 */
#include <random>
#include <thread>
#include <semaphore>
#include <atomic>
#include <condition_variable>

std::chrono::milliseconds random_ms(int lo, int hi) {
	static std::default_random_engine rng(time(0));
	std::uniform_int_distribution distrib(lo, hi);
	return std::chrono::milliseconds(distrib(rng));
}

int random_item() {
	static std::default_random_engine rng(time(0));
	static std::uniform_int_distribution distrib(0, 99);
	return distrib(rng);
}

void auto_exit(int duration) {
	std::this_thread::sleep_for(std::chrono::milliseconds(duration));
	printf("Auto exit\n");
	std::exit(0);
}
