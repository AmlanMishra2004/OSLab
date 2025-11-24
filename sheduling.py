# -----------------------------------------------------------
# CPU Scheduling: FCFS, SJF, SRTN, Priority, Round Robin
# Menu-driven program with manual input
# -----------------------------------------------------------

def calculate_metrics(processes, bt, ct, at):
    tat = [0] * len(processes)
    wt = [0] * len(processes)
    for i in range(len(processes)):
        tat[i] = ct[i] - at[i]
        wt[i] = tat[i] - bt[i]
    return tat, wt


# -----------------------------------------------------------
# 1. FCFS
# -----------------------------------------------------------
def fcfs(processes, at, bt):
    n = len(processes)
    ct = [0]*n
    gantt = []

    time = 0
    for i in range(n):
        if time < at[i]:
            time = at[i]
        time += bt[i]
        ct[i] = time
        gantt.append(f"P{processes[i]}({ct[i]})")

    tat, wt = calculate_metrics(processes, bt, ct, at)
    return ct, tat, wt, gantt


# -----------------------------------------------------------
# 2. SJF (Non-preemptive)
# -----------------------------------------------------------
def sjf(processes, at, bt):
    n = len(processes)
    done = [False] * n
    ct = [0]*n
    time = 0
    completed = 0
    gantt = []

    while completed != n:
        idx = -1
        mn = float("inf")

        for i in range(n):
            if not done[i] and at[i] <= time and bt[i] < mn:
                mn = bt[i]
                idx = i

        if idx == -1:
            time += 1
            continue

        time += bt[idx]
        ct[idx] = time
        done[idx] = True
        completed += 1
        gantt.append(f"P{processes[idx]}({ct[idx]})")

    tat, wt = calculate_metrics(processes, bt, ct, at)
    return ct, tat, wt, gantt


# -----------------------------------------------------------
# 3. SRTN (Preemptive SJF)
# -----------------------------------------------------------
def srtn(processes, at, bt):
    n = len(processes)
    rt = bt.copy()
    ct = [0]*n
    time = 0
    completed = 0
    gantt = []
    prev = -1

    while completed != n:
        idx = -1
        mn = float("inf")
        for i in range(n):
            if at[i] <= time and rt[i] > 0 and rt[i] < mn:
                mn = rt[i]
                idx = i

        if idx == -1:
            time += 1
            continue

        rt[idx] -= 1
        if prev != idx:
            gantt.append(f"P{processes[idx]}->")
            prev = idx

        if rt[idx] == 0:
            ct[idx] = time + 1
            completed += 1

        time += 1

    tat, wt = calculate_metrics(processes, bt, ct, at)
    return ct, tat, wt, gantt


# -----------------------------------------------------------
# 4. Priority Scheduling (Non-preemptive)
# -----------------------------------------------------------
def priority_scheduling(processes, at, bt, priority):
    n = len(processes)
    done = [False] * n
    ct = [0]*n
    time = 0
    completed = 0
    gantt = []

    while completed != n:
        idx = -1
        best_p = float("inf")

        for i in range(n):
            if not done[i] and at[i] <= time and priority[i] < best_p:
                best_p = priority[i]
                idx = i

        if idx == -1:
            time += 1
            continue

        time += bt[idx]
        ct[idx] = time
        done[idx] = True
        completed += 1
        gantt.append(f"P{processes[idx]}({ct[idx]})")

    tat, wt = calculate_metrics(processes, bt, ct, at)
    return ct, tat, wt, gantt


# -----------------------------------------------------------
# 5. Round Robin
# -----------------------------------------------------------
def round_robin(processes, at, bt, quantum):
    n = len(processes)
    rt = bt.copy()
    ct = [0]*n
    time = 0
    ready = []
    gantt = []

    while True:
        for i in range(n):
            if at[i] <= time and rt[i] > 0 and i not in ready:
                ready.append(i)

        if not ready:
            time += 1
            continue

        idx = ready.pop(0)

        if rt[idx] > quantum:
            time += quantum
            rt[idx] -= quantum
            gantt.append(f"P{processes[idx]}->")
        else:
            time += rt[idx]
            rt[idx] = 0
            ct[idx] = time
            gantt.append(f"P{processes[idx]}({ct[idx]})")

        for i in range(n):
            if at[i] <= time and rt[i] > 0 and i not in ready:
                ready.append(i)

        if all(r == 0 for r in rt):
            break

    tat, wt = calculate_metrics(processes, bt, ct, at)
    return ct, tat, wt, gantt


# -----------------------------------------------------------
# MAIN MENU-DRIVEN PROGRAM
# -----------------------------------------------------------

print("===== CPU Scheduling Menu =====")

# Input number of processes
n = int(input("Enter number of processes: "))

processes = list(range(n))
at = []
bt = []
priority = []

print("\nEnter Arrival Time, Burst Time & Priority:")
for i in range(n):
    a = int(input(f"AT of P{i}: "))
    b = int(input(f"BT of P{i}: "))
    p = int(input(f"Priority of P{i} (smaller = higher): "))
    at.append(a)
    bt.append(b)
    priority.append(p)
    print()

quantum = int(input("Enter Quantum for Round Robin: "))

# Menu
while True:
    print("\nChoose Scheduling Algorithm:")
    print("1. FCFS")
    print("2. SJF")
    print("3. SRTN")
    print("4. Priority Scheduling")
    print("5. Round Robin")
    print("6. Exit")

    ch = int(input("Enter choice: "))

    if ch == 1:
        ct, tat, wt, gantt = fcfs(processes, at, bt)
    elif ch == 2:
        ct, tat, wt, gantt = sjf(processes, at, bt)
    elif ch == 3:
        ct, tat, wt, gantt = srtn(processes, at, bt)
    elif ch == 4:
        ct, tat, wt, gantt = priority_scheduling(processes, at, bt, priority)
    elif ch == 5:
        ct, tat, wt, gantt = round_robin(processes, at, bt, quantum)
    elif ch == 6:
        print("Exiting...")
        break
    else:
        print("Invalid Choice!")
        continue

    print("\n===== RESULT =====")
    print("Completion Time:", ct)
    print("Turnaround Time:", tat)
    print("Waiting Time:", wt)
    print("Gantt Chart:", gantt)
