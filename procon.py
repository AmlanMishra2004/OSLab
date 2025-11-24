from threading import Thread, Semaphore, Lock
import time
import random

buffer=[]
n=5

empty=Semaphore(n)
full=Semaphore(0)
mutex=Lock()

def producer():
    while True:
        item=random.randint(1,100)
        
        empty.acquire()
        mutex.acquire()
        
        if len(buffer) == n:
            print("Error: Buffer full")   
        
        buffer.append(item)
        print("Produced item:", item)
        
        mutex.release()
        full.release()
        
        time.sleep(random.random())
        
        
def consumer():
    while True:
        item=random.randint(1,100)
        
        full.acquire()
        mutex.acquire()
        
        if len(buffer) == 0:
            print("Error: Buffer empty")  
        
        item=buffer.pop(0)
        print("Consumed item:", item)
        
        mutex.release()
        empty.release()
        
        time.sleep(random.random())
        
p=Thread(target=producer)
c=Thread(target=consumer)

p.start()
c.start()