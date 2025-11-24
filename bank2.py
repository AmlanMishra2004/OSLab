"""
Banker's Algorithm program with:
1) Safety check
2) Request algorithm
3) Generate ALL safe sequences (backtracking)
4) Resource release (on process completion)
Menu-driven and accepts user input for matrices.
"""

from typing import List, Tuple
import sys

def input_matrix(rows: int, cols: int, name: str) -> List[List[int]]:
    print(f"\nEnter {name} matrix ({rows} rows, {cols} cols).")
    print(f"Each row: {cols} integers separated by spaces")
    mat = []
    for i in range(rows):
        while True:
            line = input(f"{name}[P{i}]: ").strip()
            parts = line.split()
            if len(parts) != cols:
                print(f"Expected {cols} integers; got {len(parts)}. Try again.")
                continue
            try:
                row = [int(x) for x in parts]
            except ValueError:
                print("All values must be integers. Try again.")
                continue
            mat.append(row)
            break
    return mat

def input_vector(cols: int, name: str) -> List[int]:
    while True:
        line = input(f"\nEnter {name} vector ({cols} integers separated by spaces): ").strip()
        parts = line.split()
        if len(parts) != cols:
            print(f"Expected {cols} integers; got {len(parts)}. Try again.")
            continue
        try:
            vec = [int(x) for x in parts]
        except ValueError:
            print("All values must be integers. Try again.")
            continue
        return vec

def compute_need(maxm: List[List[int]], alloc: List[List[int]]) -> List[List[int]]:
    n = len(maxm)
    m = len(maxm[0]) if n>0 else 0
    need = [[maxm[i][j] - alloc[i][j] for j in range(m)] for i in range(n)]
    return need

def is_less_or_equal(a: List[int], b: List[int]) -> bool:
    return all(x <= y for x, y in zip(a, b))

def add_vec(a: List[int], b: List[int]) -> List[int]:
    return [x + y for x, y in zip(a, b)]

def sub_vec(a: List[int], b: List[int]) -> List[int]:
    return [x - y for x, y in zip(a, b)]

def safety_check(maxm: List[List[int]], alloc: List[List[int]], available: List[int]) -> Tuple[bool, List[int]]:
    """
    Return (is_safe, safe_sequence). If unsafe, safe_sequence = []
    Implements the standard Banker's safety algorithm and returns one valid safe sequence.
    """
    n = len(maxm)
    m = len(available)
    need = compute_need(maxm, alloc)
    work = available.copy()
    finish = [False]*n
    safe_seq = []

    while len(safe_seq) < n:
        progressed = False
        for i in range(n):
            if not finish[i] and is_less_or_equal(need[i], work):
                # simulate finishing process i
                work = add_vec(work, alloc[i])
                finish[i] = True
                safe_seq.append(i)
                progressed = True
        if not progressed:
            return False, []
    return True, safe_seq

def find_all_safe_sequences(maxm: List[List[int]], alloc: List[List[int]], available: List[int]) -> List[List[int]]:
    """
    Return list of all safe sequences (each sequence is a list of process indices).
    Uses recursion/backtracking.
    """
    n = len(maxm)
    need = compute_need(maxm, alloc)
    work = available.copy()
    finish = [False]*n
    all_seq = []
    seq = []

    def backtrack(work, finish, seq):
        if len(seq) == n:
            all_seq.append(seq.copy())
            return
        progressed = False
        for i in range(n):
            if not finish[i] and is_less_or_equal(need[i], work):
                progressed = True
                # choose i
                finish[i] = True
                new_work = add_vec(work, alloc[i])
                seq.append(i)
                backtrack(new_work, finish, seq)
                # undo
                seq.pop()
                finish[i] = False
        # if no available choice, this path dies (no action)

    backtrack(work, finish, seq)
    return all_seq

def request_resources(maxm: List[List[int]], alloc: List[List[int]], available: List[int], pid: int, req: List[int]) -> Tuple[bool, str]:
    """
    Attempt to grant request req for process pid using Banker's Request Algorithm.
    Returns (granted_bool, message).
    """
    n = len(maxm)
    if pid < 0 or pid >= n:
        return False, "Invalid process id."
    need = compute_need(maxm, alloc)
    # 1. If request > need -> error
    if not is_less_or_equal(req, need[pid]):
        return False, f"Process P{pid} has request greater than its need. Denied."
    # 2. If request > available -> must wait
    if not is_less_or_equal(req, available):
        return False, f"Resources not available now; process must wait (request > available)."
    # 3. Tentatively allocate
    available_after = sub_vec(available, req)
    alloc_after = [row.copy() for row in alloc]
    alloc_after[pid] = add_vec(alloc_after[pid], req)
    # 4. Check safety
    safe, seq = safety_check(maxm, alloc_after, available_after)
    if safe:
        # commit changes to original structures (caller should update them if granted)
        return True, f"Request can be safely granted. Safe sequence after allocation: {['P'+str(x) for x in seq]}"
    else:
        return False, "Granting request would lead to unsafe state. Request denied."

def release_process(maxm: List[List[int]], alloc: List[List[int]], available: List[int], pid: int) -> Tuple[bool, str]:
    """
    Simulate process pid completion: release its allocated resources back to available,
    zero its allocation and update need (need will be max - alloc).
    Returns (True, message) on success.
    """
    n = len(maxm)
    if pid < 0 or pid >= n:
        return False, "Invalid process id."
    # release
    available[:] = add_vec(available, alloc[pid])
    alloc[pid] = [0]*len(available)
    # need will be recomputed by caller using compute_need
    safe, seq = safety_check(maxm, alloc, available)
    if safe:
        return True, f"Released resources from P{pid}. System remains safe. Example safe seq: {['P'+str(x) for x in seq]}"
    else:
        # Should be rare: releasing resources can't make the system unsafe normally,
        # but if you want to model "process removed from system", it's safe.
        return True, f"Released resources from P{pid}. Safety check returned UNSAFE (check inputs)."

def print_state(maxm: List[List[int]], alloc: List[List[int]], available: List[int]):
    n = len(maxm)
    m = len(available) if n>0 else 0
    need = compute_need(maxm, alloc)
    print("\nCurrent system state:")
    header = ["Proc"] + [f"MaxR{j}" for j in range(m)] + [f"AllocR{j}" for j in range(m)] + [f"NeedR{j}" for j in range(m)]
    print(" | ".join(header))
    for i in range(n):
        row = [f"P{i}"] + [str(x) for x in maxm[i]] + [str(x) for x in alloc[i]] + [str(x) for x in need[i]]
        print(" | ".join(row))
    print("Available:", available)

def parse_int_list(s: str, expected_len: int = None) -> List[int]:
    parts = s.strip().split()
    try:
        vec = [int(x) for x in parts]
    except ValueError:
        raise ValueError("All entries must be integers.")
    if expected_len is not None and len(vec) != expected_len:
        raise ValueError(f"Expected {expected_len} integers, got {len(vec)}.")
    return vec

def main():
    print("=== Banker's Algorithm Simulator ===")
    # Input sizes
    while True:
        try:
            n = int(input("Enter number of processes (n): ").strip())
            m = int(input("Enter number of resource types (m): ").strip())
            if n <= 0 or m <= 0:
                print("n and m must be positive integers.")
                continue
            break
        except ValueError:
            print("Please enter valid integers for n and m.")

    # Input Max and Allocation
    print("\n-- Input Max matrix --")
    maxm = input_matrix(n, m, "Max")
    print("\n-- Input Allocation matrix --")
    alloc = input_matrix(n, m, "Allocation")

    # Validate that allocation <= max for each entry
    for i in range(n):
        for j in range(m):
            if alloc[i][j] > maxm[i][j]:
                print(f"Invalid input: Allocation[{i}][{j}] > Max[{i}][{j}]. Exiting.")
                sys.exit(1)

    # Input Available vector
    available = input_vector(m, "Available")

    # Compute Need implicitly when needed
    while True:
        print("\n=== MENU ===")
        print("1) Show current state (Max, Allocation, Need, Available)")
        print("2) Safety check (is current state safe?)")
        print("3) Generate ALL safe sequences")
        print("4) Make a resource REQUEST (simulate Request Algorithm)")
        print("5) Release a process (simulate completion and resource release)")
        print("6) Re-enter matrices (start over)")
        print("7) Exit")
        choice = input("Choose (1-7): ").strip()

        if choice == "1":
            print_state(maxm, alloc, available)

        elif choice == "2":
            safe, seq = safety_check(maxm, alloc, available)
            if safe:
                print("System is in a SAFE state.")
                print("One safe sequence:", ["P"+str(x) for x in seq])
            else:
                print("System is NOT in a safe state (unsafe).")

        elif choice == "3":
            sequences = find_all_safe_sequences(maxm, alloc, available)
            if not sequences:
                print("No safe sequences exist for the current state.")
            else:
                print(f"Found {len(sequences)} safe sequence(s):")
                for idx, s in enumerate(sequences, 1):
                    print(f"{idx}: ", " -> ".join("P"+str(x) for x in s))

        elif choice == "4":
            try:
                pid = int(input("Enter process id making request (0..n-1): ").strip())
            except ValueError:
                print("Invalid process id.")
                continue
            try:
                line = input(f"Enter request vector of length {m} (space separated): ")
                req = parse_int_list(line, expected_len=m)
            except ValueError as e:
                print("Bad input:", e)
                continue
            # run request algorithm tentatively
            granted, msg = request_resources(maxm, alloc, available, pid, req)
            print(msg)
            if granted:
                # commit the tentative allocation
                available[:] = sub_vec(available, req)
                alloc[pid] = add_vec(alloc[pid], req)
                print("Request committed (resources allocated).")
                safe, seq = safety_check(maxm, alloc, available)
                print("Post-allocation safety:", "SAFE" if safe else "UNSAFE")
                if safe:
                    print("Safe sequence:", ["P"+str(x) for x in seq])
            else:
                print("Request not granted. No changes made.")

        elif choice == "5":
            try:
                pid = int(input("Enter process id to release (0..n-1): ").strip())
            except ValueError:
                print("Invalid process id.")
                continue
            ok, msg = release_process(maxm, alloc, available, pid)
            print(msg)
            # after release, need implicitly updated via alloc matrix

        elif choice == "6":
            print("Re-entering matrices...")
            maxm = input_matrix(n, m, "Max")
            alloc = input_matrix(n, m, "Allocation")
            for i in range(n):
                for j in range(m):
                    if alloc[i][j] > maxm[i][j]:
                        print(f"Invalid input: Allocation[{i}][{j}] > Max[{i}][{j}]. Exiting.")
                        sys.exit(1)
            available = input_vector(m, "Available")
            print("New matrices recorded.")

        elif choice == "7":
            print("Exiting. Goodbye.")
            break
        else:
            print("Invalid choice. Enter 1..7.")

if __name__ == "__main__":
    main()
