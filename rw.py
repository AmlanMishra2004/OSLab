
import threading
import time
import random

read_count = 0        # number of active readers
read_count_lock = threading.Lock()
resource_lock = threading.Lock()   # writers lock


def reader(i):
    global read_count

    while True:
        # entry section for readers
        with read_count_lock:
            read_count += 1
            if read_count == 1:
                resource_lock.acquire()

        print(f"Reader {i} is READING")
        time.sleep(random.uniform(0.5, 1.5))

        # exit section for readers
        with read_count_lock:
            read_count -= 1
            if read_count == 0:
                resource_lock.release()

        time.sleep(random.uniform(0.5, 1.5))


def writer(i):
    while True:
        resource_lock.acquire()

        print(f"Writer {i} is WRITING")
        time.sleep(random.uniform(1, 2))

        resource_lock.release()

        time.sleep(random.uniform(1, 2))


# Start threads
threads = []
for i in range(3):
    t = threading.Thread(target=reader, args=(i,))
    threads.append(t)
    t.start()

for i in range(2):
    t = threading.Thread(target=writer, args=(i,))
    threads.append(t)
    t.start()
