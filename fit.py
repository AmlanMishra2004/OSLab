# -------------------------------------------
# Memory Allocation Algorithms:
# First Fit, Best Fit, Worst Fit, Next Fit
# -------------------------------------------

def first_fit(blocks, processes):
    block_remaining = blocks.copy()
    allocation = [-1] * len(processes)
    internal_frag = [0] * len(processes)

    for i, p in enumerate(processes):
        for j, b in enumerate(block_remaining):
            if b >= p:
                allocation[i] = j
                internal_frag[i] = b - p
                block_remaining[j] -= p
                break

    return allocation, internal_frag, block_remaining


def best_fit(blocks, processes):
    block_remaining = blocks.copy()
    allocation = [-1] * len(processes)
    internal_frag = [0] * len(processes)

    for i, p in enumerate(processes):
        best_idx = -1
        best_size = float('inf')

        for j, b in enumerate(block_remaining):
            if b >= p and b < best_size:
                best_size = b
                best_idx = j

        if best_idx != -1:
            allocation[i] = best_idx
            internal_frag[i] = block_remaining[best_idx] - p
            block_remaining[best_idx] -= p

    return allocation, internal_frag, block_remaining


def worst_fit(blocks, processes):
    block_remaining = blocks.copy()
    allocation = [-1] * len(processes)
    internal_frag = [0] * len(processes)

    for i, p in enumerate(processes):
        worst_idx = -1
        worst_size = -1

        for j, b in enumerate(block_remaining):
            if b >= p and b > worst_size:
                worst_size = b
                worst_idx = j

        if worst_idx != -1:
            allocation[i] = worst_idx
            internal_frag[i] = block_remaining[worst_idx] - p
            block_remaining[worst_idx] -= p

    return allocation, internal_frag, block_remaining


def next_fit(blocks, processes):
    block_remaining = blocks.copy()
    allocation = [-1] * len(processes)
    internal_frag = [0] * len(processes)

    last = 0   # start point

    for i, p in enumerate(processes):
        count = 0
        j = last

        while count < len(block_remaining):
            if block_remaining[j] >= p:
                allocation[i] = j
                internal_frag[i] = block_remaining[j] - p
                block_remaining[j] -= p
                last = j
                break

            j = (j + 1) % len(block_remaining)
            count += 1

    return allocation, internal_frag, block_remaining


# -------------------------------------------
# Function to display results
# -------------------------------------------
def display(method, blocks, processes, allocation, internal_frag, block_remaining):
    print(f"\n--- {method} ---")
    print("Process\tSize\tBlock Allotted\tInternal Frag")

    for i, p in enumerate(processes):
        if allocation[i] != -1:
            print(f"P{i}\t{p}\tB{allocation[i]}\t\t{internal_frag[i]}")
        else:
            print(f"P{i}\t{p}\tNot Allocated\t-")

    total_internal = sum(internal_frag)
    print(f"\nTotal Internal Fragmentation = {total_internal}")

    # External fragmentation = total leftover free blocks
    external = sum(b for b in block_remaining if b > 0)
    print(f"External Fragmentation (total free space) = {external}")


# -------------------------------------------
# Main Program (Modify input here)
# -------------------------------------------
if __name__ == "__main__":

    blocks = [100, 500, 200, 300, 600]      # memory blocks
    processes = [212, 417, 112, 426, 95]    # process sizes

    print("\nMemory Blocks:", blocks)
    print("Processes:", processes)

    # First Fit
    a1, f1, r1 = first_fit(blocks, processes)
    display("First Fit", blocks, processes, a1, f1, r1)

    # Best Fit
    a2, f2, r2 = best_fit(blocks, processes)
    display("Best Fit", blocks, processes, a2, f2, r2)

    # Worst Fit
    a3, f3, r3 = worst_fit(blocks, processes)
    display("Worst Fit", blocks, processes, a3, f3, r3)

    # Next Fit
    a4, f4, r4 = next_fit(blocks, processes)
    display("Next Fit", blocks, processes, a4, f4, r4)
