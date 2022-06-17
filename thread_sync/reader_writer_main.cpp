int main() {
	std::thread t_writers[N_WRITERS];
	std::thread t_readers[N_READERS];
	for (int i = 0; i < N_WRITERS; i++)
		t_writers[i] = std::thread(writer, i);
	for (int i = 0; i < N_READERS; i++)
		t_readers[i] = std::thread(reader, i);
	std::thread t_exit = std::thread(auto_exit, 1000);
	t_exit.join();
	for (int i = 0; i < N_WRITERS; i++)
		t_writers[i].join();
	for (int i = 0; i < N_READERS; i++)
		t_readers[i].join();
	printf("Safe exit\n");
	return 0;
}