/**
 * @file bounded_buffer_moniter.cpp
 * @author QuadnucYard
 * @brief 有界缓冲区问题，管程解决方案
 * @version 0.1
 * @date 2022-06-17
 *
 * @copyright Copyright (c) 2022
 *
 */
#include "common_sync.h"

const int N = 10;
const int N_PRODUCER = 3, N_CONSUMER = 4;
int buffer[N];
int nextin{ 0 }, nextout{ 0 }, count{ 0 };
std::condition_variable notfull, notempty;
std::mutex mtx;

void append(int x) {
	std::unique_lock<std::mutex> lk(mtx);
	if (count == N) notfull.wait(lk);
	buffer[nextin] = x;
	nextin = (nextin + 1) % N;
	count++;
	printf("  append %d\n", x);
	notempty.notify_one();
}

int take() {
	std::unique_lock<std::mutex> lk(mtx);
	if (count == 0) notempty.wait(lk);
	int x = buffer[nextout];
	nextout = (nextout + 1) % N;
	count--;
	printf("  take %d\n", x);
	notfull.notify_one();
	return x;
}

void producer(int id) {
	while (true) {
		int x = random_item();
		printf("Prodece[%d]: %d\n", id, x);
		append(x);
		std::this_thread::sleep_for(random_ms(10, 100));
	}
}

void consumer(int id) {
	while (true) {
		int x = take();
		printf("Consume[%d]: %d\n", id, x);
		std::this_thread::sleep_for(random_ms(10, 100));
	}
}

int main() {
	std::thread t_producers[N_PRODUCER];
	std::thread t_consumers[N_CONSUMER];
	for (int i = 0; i < N_PRODUCER; i++)
		t_producers[i] = std::thread(producer, i);
	for (int i = 0; i < N_CONSUMER; i++)
		t_consumers[i] = std::thread(consumer, i);
	std::thread t_exit = std::thread(auto_exit, 1000);
	t_exit.join();
	for (int i = 0; i < N_PRODUCER; i++)
		t_producers[i].join();
	for (int i = 0; i < N_CONSUMER; i++)
		t_consumers[i].join();
	printf("Safe exit\n");
	return 0;
}