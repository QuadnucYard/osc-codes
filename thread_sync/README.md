# thread_sync

线程同步算法。

注意，所有文件名有 `main` 的 cpp 文件均不可执行，您应当执行其他代码内包含相应 main 的 cpp 文件。

## common_sync.h

公用头文件和函数，包括生成随机延时、产生随机物品。

## critsec_algo*.cpp

临界区问题基础算法。1 使用 `test_and_set`，2 使用 `swap`，3 使用 `test_and_set` 且正确。

## hardware_*.cpp

临界区问题的硬件解决方案，使用 `atomic`。

## reader_writer_*.cpp

第一/二读者写者问题。一为读者优先，二为写者优先。

## dining_philosophers_*.cpp

哲学家吃饭问题的 3 种解决方案：限制人数，原子操作，奇偶先后。

## bounded_buffer_monitor.cpp

有界缓冲区问题的管程解决方案，使用 `condition_variable`。

## dining_philosophers_monitor.cpp

哲学家吃饭问题的管程解决方案，使用 `condition_variable`。