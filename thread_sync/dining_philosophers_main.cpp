int main() {
	std::thread t_philos[N];
	for (int i = 0; i < N; i++)
		t_philos[i] = std::thread(philosopher, i);
	std::thread t_exit = std::thread(auto_exit, 1000);
	t_exit.join();
	for (int i = 0; i < N; i++)
		t_philos[i].join();
	printf("Safe exit\n");
	return 0;
}