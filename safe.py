# Banker's Algorithm Implementation in Python

def is_safe(processes, available, max_need, allocation):
    n = len(processes)
    m = len(available)

    # Calculate need matrix
    need = [[max_need[i][j] - allocation[i][j] for j in range(m)] for i in range(n)]

    finish = [False] * n
    safe_seq = []
    work = available.copy()

    while len(safe_seq) < n:
        allocated = False
        for i in range(n):
            if not finish[i]:
                # Check if need <= work
                if all(need[i][j] <= work[j] for j in range(m)):
                    # Allocate resources
                    for j in range(m):
                        work[j] += allocation[i][j]
                    finish[i] = True
                    safe_seq.append(processes[i])
                    allocated = True

        if not allocated:
            return False, []  # Not safe

    return True, safe_seq


# ------------------------------
# Example Input
# ------------------------------
processes = [0, 1, 2, 3, 4]

allocation = [
    [0, 1, 0],  
    [2, 0, 0],  
    [3, 0, 2],  
    [2, 1, 1],  
    [0, 0, 2]
]

max_need = [
    [7, 5, 3],  
    [3, 2, 2],  
    [9, 0, 2],  
    [2, 2, 2],  
    [4, 3, 3]
]

available = [3, 3, 2]


# ------------------------------
# Run Safety Check
# ------------------------------
safe, seq = is_safe(processes, available, max_need, allocation)

print("\n--- BANKER'S ALGORITHM RESULT ---")
if safe:
    print("System is in a SAFE state.")
    print("Safe sequence:", seq)
else:
    print("System is NOT in a safe state (Deadlock Possible).")
