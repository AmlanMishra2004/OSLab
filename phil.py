import threading
import time
import random

N=5
THINKING=0
HUNGRY=1
EATING=2

state=[THINKING] * N
condition=[threading.Condition() for _ in range(N)]
lock=threading.Lock()

def left(i):
    return (i+N-1) % N

def right(i):
    return (i+1) % N

def test(i):
    if (state[i]==HUNGRY and state[left(i)]!=EATING and state[right(i)]!=EATING):
        state[i]=EATING
        condition[i].notify
        
def take_forks(i):
    with lock:
        state[i]=HUNGRY
        print(f'Philosopher {i} is HUNGRY')
        
        test(i)
        
        while state[i]!=EATING:
            condition[i].wait()
            
def put_forks(i):
    with lock:
        state[i]=THINKING
        print(f"Philosopher {i} PUTS DOWN forks and is THINKING")

        test(left(i))
        test(right(i))
        
        
def philosopher(i):
    while True:
        print(f"Philosopher {i} is THINKING")
        time.sleep(random.uniform(1, 3))
        
        take_forks(i)
        
        print(f"Philosopher {i} is EATING")
        time.sleep(random.uniform(1, 2))

        put_forks(i)
        
        
threads=[]
for i in range(N):
    t=threading.Thread(target=philosopher, args=(i,))
    threads.append(t)
    t.start()