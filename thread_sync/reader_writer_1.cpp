/**
 * @file reader_writer_1.cpp
 * @author QuadnucYard
 * @brief 第一 Reader-Wrtier 问题，读者优先。
 * @version 0.1
 * @date 2022-06-16
 *
 * @copyright Copyright (c) 2022
 *
 */
#include <iostream>
#include "common_sync.h"

const int N_WRITERS = 2;
const int N_READERS = 3;
std::binary_semaphore mutex(1), wrt(1);
int readcount(0);
int shared_item;

void writer(int id) {
	printf("writer %d\n", id);
	while (true) {
		std::this_thread::sleep_for(random_ms(10, 100));
		wrt.acquire();
		shared_item = random_item();
		printf("Writing is performed by %d: %d\n", id, shared_item);
		wrt.release();
	}
}

void reader(int id) {
	printf("reader %d\n", id);
	while (true) {
		std::this_thread::sleep_for(random_ms(10, 100));
		mutex.acquire();
		if (readcount++ == 0) wrt.acquire();
		mutex.release();
		printf("Reading is performed by %d: %d\n", id, shared_item);
		mutex.acquire();
		if (--readcount == 0) wrt.release();
		mutex.release();
	}
}

#include "reader_writer_main.cpp"