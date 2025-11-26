import subprocess
import shlex
import copy

# --- MEMORY MANAGEMENT ALGORITHM FUNCTIONS ---

def allocate_memory(blocks, processes_sizes, strategy):
    """General function to allocate memory based on a specified strategy."""
    print(f"### Allocation Strategy: {strategy}")
    
    # Create a list of dictionaries to track the status and fragmentation of blocks
    blocks_list = [{"id": i, "size": size, "allocated_to": None} for i, size in enumerate(blocks)]
    
    total_internal_fragmentation = 0
    allocation_summary = {}

    for i, process_size in enumerate(processes_sizes):
        process_name = f"P{i+1}"
        allocated = False
        
        # 1. Identify Candidate Blocks (blocks that are free and large enough)
        candidates = [
            (j, block) for j, block in enumerate(blocks_list) 
            if block["allocated_to"] is None and block["size"] >= process_size
        ]

        if not candidates:
            allocation_summary[process_name] = {"status": "Not Allocated (No fit found)"}
            continue

        # 2. Select Allocation Block based on Strategy
        
        selected_index = -1
        
        if strategy == "First-Fit":
            selected_index = candidates[0][0] # Select the first one found
            
        elif strategy == "Best-Fit":
            # Select block that minimizes fragmentation (smallest remaining space)
            candidates.sort(key=lambda x: x[1]['size'] - process_size)
            selected_index = candidates[0][0]
            
        elif strategy == "Worst-Fit":
            # Select block that maximizes fragmentation (largest remaining space)
            candidates.sort(key=lambda x: x[1]['size'] - process_size, reverse=True)
            selected_index = candidates[0][0]

        # 3. Perform Allocation
        
        if selected_index != -1:
            allocated_block = blocks_list[selected_index]
            allocated_block["allocated_to"] = process_name
            
            # Calculate internal fragmentation
            internal_fragmentation = allocated_block["size"] - process_size
            total_internal_fragmentation += internal_fragmentation
            
            allocation_summary[process_name] = {
                "block_id": allocated_block["id"],
                "block_size": allocated_block["size"],
                "fragmentation": internal_fragmentation
            }
            allocated = True

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
    print("[Placeholder: Insert your Memory Allocation Diagram visualization here]")
    print("-------------------------------------------------------")
    
    return total_internal_fragmentation


# --- LINUX INTEGRATION FUNCTION ---

def get_real_memory_status():
    """
    Executes the 'free -h' Linux command to get real system memory usage statistics.
    """
    print("\n## 2. Linux System Output: Real-Time Memory Status")
    print("-------------------------------------------------------")
    
    command = "free -h"
    args = shlex.split(command)
    
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        
        # Display the real-world memory information
        print(result.stdout)
        
        print("\n--- Comparison Tip ---")
        print("Compare your calculated fragmentation results to the real system's use of 'buffers/cache', which is a technique used to mitigate the fragmentation problems your simulation attempts to solve.")
        
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
    
    # --- LINUX INTEGRATION SECTION ---
    get_real_memory_status()
