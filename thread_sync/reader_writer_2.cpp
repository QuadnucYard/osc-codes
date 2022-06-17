/**
 * @file reader_writer_2.cpp
 * @author QuadnucYard
 * @brief 第二 Reader-Wrtier 问题，写者优先。
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
std::binary_semaphore readcount_mutex(1), writecount_mutex(1), read_mutex(1), write_mutex(1);
int readcount(0), writecount(0);
int shared_item;

void writer(int id) {
	printf("writer %d\n", id);
	while (true) {
		std::this_thread::sleep_for(random_ms(10, 100));
		writecount_mutex.acquire();
		if (writecount++ == 0) read_mutex.acquire();
		writecount_mutex.release();

		write_mutex.acquire();
		shared_item = random_item();
		printf("Writing is performed by %d: %d\n", id, shared_item);
		write_mutex.release();

		writecount_mutex.acquire();
		if (--writecount == 0) read_mutex.release();
		writecount_mutex.release();
	}
}

void reader(int id) {
	printf("reader %d\n", id);
	while (true) {
		std::this_thread::sleep_for(random_ms(10, 100));
		read_mutex.acquire();
		readcount_mutex.acquire();
		if (readcount++ == 0) write_mutex.acquire();
		readcount_mutex.release();
		read_mutex.release();

		printf("Reading is performed by %d: %d\n", id, shared_item);

		readcount_mutex.acquire();
		if (--readcount == 0) write_mutex.release();
		readcount_mutex.release();
	}
}

#include "reader_writer_main.cpp"