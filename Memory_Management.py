import subprocess
import shlex
import copy

# --- VISUALIZATION FUNCTION ---

def display_memory_diagram(blocks_list):
    """
    Displays a simple text/ASCII visualization of the memory partitions.
    """
    print("\n--- Memory Allocation Diagram ---")
    
    # Find the maximum block size for consistent width
    max_size = max(b["size"] for b in blocks_list) if blocks_list else 100
    total_size = sum(b["size"] for b in blocks_list)
    
    # Scale factor for visualization
    scale = 60 / total_size

    for block in blocks_list:
        status = "FREE" if block["allocated_to"] is None else f"USED ({block['allocated_to']})"
        width = int(block["size"] * scale)
        
        # Use a simple ASCII block representation
        line = f"|{'=' * width}| Block {block['id']} ({block['size']}MB): {status}"
        print(line)
    
    print("---------------------------------")


# --- MEMORY MANAGEMENT ALGORITHM FUNCTIONS ---

def allocate_memory(blocks, processes_sizes, strategy, last_allocated_block_id=0):
    """General function to allocate memory based on a specified strategy."""
    print(f"### Allocation Strategy: {strategy}")
    
    # Create a list of dictionaries to track the status and fragmentation of blocks
    blocks_list = [{"id": i, "size": size, "allocated_to": None} for i, size in enumerate(blocks)]
    
    total_internal_fragmentation = 0
    allocation_summary = {}
    
    # Initialize pointer for Next-Fit
    next_fit_pointer = last_allocated_block_id

    for i, process_size in enumerate(processes_sizes):
        process_name = f"P{i+1}"
        
        # 1. Identify Candidate Blocks (blocks that are free and large enough)
        candidates = [
            (j, block) for j, block in enumerate(blocks_list) 
            if block["allocated_to"] is None and block["size"] >= process_size
        ]

        if not candidates:
            allocation_summary[process_name] = {"status": "Not Allocated (No fit found)"}
            continue

        selected_index = -1
        
        if strategy == "First-Fit":
            selected_index = candidates[0][0] # Select the first one found (candidates are already ordered by index)
            
        elif strategy == "Best-Fit":
            # Select block that minimizes fragmentation
            candidates.sort(key=lambda x: x[1]['size'] - process_size)
            selected_index = candidates[0][0]
            
        elif strategy == "Worst-Fit":
            # Select block that maximizes fragmentation
            candidates.sort(key=lambda x: x[1]['size'] - process_size, reverse=True)
            selected_index = candidates[0][0]

        elif strategy == "Next-Fit":
            # Start search from the block *after* the last allocation (next_fit_pointer)
            num_blocks = len(blocks_list)
            
            # Search from pointer to end
            for j in range(next_fit_pointer, num_blocks):
                block = blocks_list[j]
                if block["allocated_to"] is None and block["size"] >= process_size:
                    selected_index = j
                    break
            
            # If no fit found, wrap search from start to pointer
            if selected_index == -1:
                for j in range(next_fit_pointer):
                    block = blocks_list[j]
                    if block["allocated_to"] is None and block["size"] >= process_size:
                        selected_index = j
                        break
            
            # If still no fit, Next-Fit fails, or it was the only option already selected.
            # If allocated, update the pointer for the next process to the *next* block
            if selected_index != -1:
                next_fit_pointer = (selected_index + 1) % num_blocks
        
        # 3. Perform Allocation
        
        if selected_index != -1:
            allocated_block = blocks_list[selected_index]
            allocated_block["allocated_to"] = process_name
            
            internal_fragmentation = allocated_block["size"] - process_size
            total_internal_fragmentation += internal_fragmentation
            
            allocation_summary[process_name] = {
                "block_id": allocated_block["id"],
                "block_size": allocated_block["size"],
                "fragmentation": internal_fragmentation
            }

    # --- Display Metrics ---
    
    print("Allocation Decisions:")
    for proc, data in allocation_summary.items():
        if "status" in data:
            print(f"  {proc:<20}: {data['status']}")
        else:
            print(f"  {proc:<20}: Block {data['block_id']} ({data['block_size']}MB). Fragment: {data['fragmentation']}MB")

    # Calculate External Fragmentation
    external_fragmentation = sum(block["size"] for block in blocks_list if block["allocated_to"] is None)
    
    print(f"\n* Total Internal Fragmentation: {total_internal_fragmentation} MB")
    print(f"* Total External Fragmentation (Sum of Available): {external_fragmentation} MB")
    display_memory_diagram(blocks_list)
    print("-------------------------------------------------------")
    
    return total_internal_fragmentation


# --- LINUX INTEGRATION FUNCTION ---

def get_real_memory_status():
    """
    Executes the 'free -h' Linux command to get real system memory usage statistics.
    """
    print("\n## 2. Linux System Output: Detailed Real-Time Memory Status")
    print("-------------------------------------------------------")
    
    command = "free -h"
    args = shlex.split(command)
    
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        
        # Display the real-world memory information (detailed stuff)
        print(result.stdout)
        
        print("\n--- Comparison Tip ---")
        print("Compare your calculated fragmentation results to the real system's use of 'buffers/cache'.")
        
    except Exception as e:
        print(f"Error executing Linux command 'free -h': {e}")
        print("Please ensure this script is run on a Linux environment or WSL.")


# --- MAIN EXECUTION ---

if __name__ == "__main__":
    print("## Memory Management Simulator and Linux Integrator")
    
    # Test case data: (Memory Blocks/Partitions sizes, Process sizes)
    test_blocks = [100, 500, 200, 300, 600]
    test_processes = [212, 417, 112, 426]

    # --- SIMULATION SECTION ---
    print("\n------------------------------------------------------------------")
    print("RUNNING FIRST-FIT SIMULATION:")
    print("------------------------------------------------------------------")
    allocate_memory(copy.deepcopy(test_blocks), test_processes, "First-Fit")

    print("\n------------------------------------------------------------------")
    print("RUNNING BEST-FIT SIMULATION:")
    print("------------------------------------------------------------------")
    allocate_memory(copy.deepcopy(test_blocks), test_processes, "Best-Fit")

    print("\n------------------------------------------------------------------")
    print("RUNNING WORST-FIT SIMULATION:")
    print("------------------------------------------------------------------")
    allocate_memory(copy.deepcopy(test_blocks), test_processes, "Worst-Fit")

    print("\n------------------------------------------------------------------")
    print("RUNNING NEXT-FIT SIMULATION:")
    print("------------------------------------------------------------------")
    # For Next-Fit, the starting pointer (last_allocated_block_id) matters. 
    # Here, we start searching from block 0.
    allocate_memory(copy.deepcopy(test_blocks), test_processes, "Next-Fit", last_allocated_block_id=0)
    
    # --- LINUX INTEGRATION SECTION ---
    get_real_memory_status()
