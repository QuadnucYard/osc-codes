void on_exit() {
	printf("On exit, cnt=%d\n", cnt);
}

int main() {
	std::atexit(on_exit);
	std::thread t_process[N];
	for (int i = 0; i < N; i++) t_process[i] = std::thread(process, i);
	std::thread t_exit = std::thread(auto_exit, 1000);
	t_exit.join();
	for (int i = 0; i < N; i++) t_process[i].join();
	printf("Safe exit\n");
	return 0;
}