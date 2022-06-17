/**
 * @file dining_philosophers_1.cpp
 * @author QuadnucYard
 * @brief 哲学家吃饭问题：管程解决方案
 * @version 0.1
 * @date 2022-06-16
 *
 * @copyright Copyright (c) 2022
 *
 */
#include "common_sync.h"

const int N = 5;
enum class State {
	thinking, hungry, eating
} state[N];
std::condition_variable self[N];
std::mutex mtx;

void test(int i) {
	if (state[i] == State::hungry
		&& state[(i + N - 1) % N] != State::eating
		&& state[(i + 1) % N] != State::eating) {
		state[i] = State::eating;
		self[i].notify_one();
	}
}

void pickup(int i) {
	state[i] = State::hungry;
	test(i);
	std::unique_lock<std::mutex> lk(mtx);
	if (state[i] != State::eating) self[i].wait(lk);
}

void putdown(int i) {
	state[i] = State::thinking;
	test((i + N - 1) % N);
	test((i + 1) % N);
}

void philosopher(int i) {
	state[i] = State::thinking;
	while (true) {
		std::this_thread::sleep_for(random_ms(10, 100));
		printf("Philosopher %d: Want to eat\n", i);
		pickup(i);
		printf("Philosopher %d: Eating\n", i);
		std::this_thread::sleep_for(random_ms(10, 100));
		printf("Philosopher %d: Eating finished\n", i);
		putdown(i);
		printf("Philosopher %d: Put down\n", i);
	}
}

#include "dining_philosophers_main.cpp"