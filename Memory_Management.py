import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
# CORRECTED LINE: Import field along with dataclass
from dataclasses import dataclass, field 
from typing import List, Optional, Tuple, Dict

# Detect if the script is running in a headless environment
HEADLESS = not os.environ.get("DISPLAY")

# --- Configuration for Simulation ---
# Max size for random memory blocks and processes (to keep numbers sane)
MAX_SIZE = 500
NUM_BLOCKS = 5
NUM_PROCESSES = 4


# ----------------------------
# STEP 1: MEMORY DATA STRUCTURES
# ----------------------------
@dataclass
class Block:
    """Represents a free memory block."""
    bid: int
    size: int
    initial_size: int = field(init=False)
    allocated_to: Optional[int] = None # Stores PID if allocated

    def __post_init__(self):
        # Initial size is stored to calculate fragmentation later
        self.initial_size = self.size

@dataclass
class Process:
    """Represents a process requesting memory."""
    pid: int
    size: int
    status: str = "PENDING"
    allocated_block_id: Optional[int] = None
    fragmentation: Optional[int] = None

# ----------------------------
# STEP 2: INPUT GENERATION
# ----------------------------

def generate_input_data() -> Tuple[List[Block], List[Process]]:
    """
    Generates deterministic or random input data for memory blocks and processes.

    Returns
    -------
    (List[Block], List[Process])
    """
    # Use deterministic data for consistent testing
    BLOCK_SIZES = [100, 500, 200, 300, 600]
    PROCESS_SIZES = [212, 417, 112, 426] # Total: 1167

    # Create Blocks
    blocks = [Block(bid=i+1, size=s) for i, s in enumerate(BLOCK_SIZES)]
    
    # Create Processes
    processes = [Process(pid=i+1, size=s) for i, s in enumerate(PROCESS_SIZES)]
    
    return blocks, processes


# ----------------------------
# STEP 3: ALLOCATION ALGORITHMS
# ----------------------------

def clone_memory(blocks: List[Block], processes: List[Process]) -> Tuple[List[Block], List[Process]]:
    """Create deep copies of memory blocks and processes for a fresh simulation run."""
    new_blocks = [Block(b.bid, b.size) for b in blocks]
    new_processes = [Process(p.pid, p.size) for p in processes]
    # Use a dictionary for fast block lookup by BID during allocation
    block_map = {b.bid: b for b in new_blocks}
    return new_blocks, new_processes, block_map

def allocate(
    blocks: List[Block], 
    processes: List[Process], 
    allocation_fn: callable,
    algo_name: str
) -> Tuple[List[Block], List[Process]]:
    """
    Generic allocation driver function.

    Parameters
    ----------
    blocks : List[Block]
    processes : List[Process]
    allocation_fn : callable
        One of the fit functions (first_fit_logic, best_fit_logic, worst_fit_logic).
    algo_name : str
        Name of the algorithm for logging.

    Returns
    -------
    (List[Block], List[Process])
    """
    # Clone data structures to ensure runs are independent
    current_blocks, current_processes, block_map = clone_memory(blocks, processes)
    
    # Sort processes for consistent order, though it doesn't affect the result
    current_processes.sort(key=lambda x: x.pid)

    for p in current_processes:
        # Find the best block index using the specific logic function
        block_to_use_id = allocation_fn(current_blocks, p.size)

        if block_to_use_id != -1:
            # Allocation successful
            block = block_map[block_to_use_id]
            
            p.status = "ALLOCATED"
            p.allocated_block_id = block.bid
            p.fragmentation = block.size - p.size # Internal Fragmentation
            
            # Update the block size (remaining space)
            block.size -= p.size
            block.allocated_to = p.pid

        else:
            # Allocation failed
            p.status = "FAILED"
    
    return current_blocks, current_processes


# --- Allocation Logic Functions ---

def first_fit_logic(blocks: List[Block], p_size: int) -> int:
    """Finds the ID of the first block large enough."""
    for block in blocks:
        if block.size >= p_size:
            return block.bid
    return -1

def best_fit_logic(blocks: List[Block], p_size: int) -> int:
    """Finds the ID of the block that leaves the smallest internal fragmentation."""
    best_id = -1
    min_fragmentation = float('inf')

    for block in blocks:
        if block.size >= p_size:
            fragmentation = block.size - p_size
            if fragmentation < min_fragmentation:
                min_fragmentation = fragmentation
                best_id = block.bid
    return best_id

def worst_fit_logic(blocks: List[Block], p_size: int) -> int:
    """Finds the ID of the block that leaves the largest internal fragmentation."""
    worst_id = -1
    max_fragmentation = -1

    for block in blocks:
        if block.size >= p_size:
            fragmentation = block.size - p_size
            if fragmentation > max_fragmentation:
                max_fragmentation = fragmentation
                worst_id = block.bid
    return worst_id


# ----------------------------
# STEP 4: METRICS & VISUALIZATION
# ----------------------------

def compute_metrics(blocks: List[Block], processes: List[Process], initial_blocks: List[Block]) -> Dict:
    """Computes total internal fragmentation and external fragmentation."""
    
    total_internal_frag = sum(p.fragmentation for p in processes if p.status == "ALLOCATED")
    
    # Calculate initial total memory capacity
    initial_capacity = sum(b.initial_size for b in initial_blocks)
    
    # Calculate remaining free space (External Fragmentation potential)
    total_remaining_free = sum(b.size for b in blocks)
    
    # Calculate memory wasted on non-allocated processes (External Fragmentation that is too small)
    failed_processes_size = sum(p.size for p in processes if p.status == "FAILED")

    # Total allocated size to processes (excluding fragmentation)
    total_allocated_size = sum(p.size for p in processes if p.status == "ALLOCATED")

    # Total allocated space including fragmentation
    total_allocated_plus_frag = initial_capacity - total_remaining_free
    
    return {
        "Total_Capacity": initial_capacity,
        "Total_Allocated": total_allocated_size,
        "Total_Internal_Frag": total_internal_frag,
        "Total_External_Frag": total_remaining_free, # Total remaining free blocks
        "Failed_Processes_Size": failed_processes_size,
    }


def plot_memory_map(blocks: List[Block], title: str, initial_blocks: List[Block]):
    """
    Generates a visual representation of the final memory map.
    :param blocks: The final state of memory blocks.
    :param title: Chart title.
    :param initial_blocks: The initial state of memory blocks (for reference).
    """
    fig, ax = plt.subplots(figsize=(6, NUM_BLOCKS * 0.8))
    
    # Create a mapping of PID to a unique color
    unique_pids = {b.allocated_to for b in blocks if b.allocated_to is not None}
    colors = plt.cm.get_cmap('Set1', len(unique_pids) + 1)
    color_map = {pid: colors(i) for i, pid in enumerate(unique_pids, start=1)}
    
    y_pos = 0 # Vertical position counter for bars

    # Create a DataFrame for easy plotting
    plot_data = []
    
    # Ensure blocks are sorted by BID for visual consistency
    blocks.sort(key=lambda x: x.bid)

    for i, block in enumerate(blocks):
        # 1. Plot the allocated segment
        if block.allocated_to is not None:
            allocated_size = initial_blocks[i].initial_size - block.size
            plot_data.append({
                'Block': f'Block {block.bid}', 
                'Start': 0, 
                'Size': allocated_size, 
                'Type': f'P{block.allocated_to} (Used)', 
                'Color': color_map[block.allocated_to]
            })
            
            # 2. Plot the internal fragmentation (leftover free space in the block)
            if block.size > 0:
                plot_data.append({
                    'Block': f'Block {block.bid}', 
                    'Start': allocated_size, 
                    'Size': block.size, 
                    'Type': 'Internal Frag (Free)', 
                    'Color': 'lightgray'
                })
        else:
            # 3. Plot a block that was never used (External Fragmentation)
            plot_data.append({
                'Block': f'Block {block.bid}', 
                'Start': 0, 
                'Size': block.size, 
                'Type': 'External Frag (Free)', 
                'Color': 'darkgray'
            })

    # Plotting the bars
    current_y = 0
    y_tick_labels = []
    
    # Use a set to track which block label has been added
    added_labels = set()
    
    for i, block in enumerate(initial_blocks):
        b_id = block.bid
        
        # Filter plot data for the current block and sort by start position
        block_data = [d for d in plot_data if d['Block'] == f'Block {b_id}']
        block_data.sort(key=lambda x: x['Start'])
        
        # Plot segments for this block
        current_x = 0
        for data in block_data:
            ax.barh(b_id, data['Size'], left=current_x, color=data['Color'], 
                    label=data['Type'] if data['Type'] not in added_labels else "_nolegend_")
            current_x += data['Size']
            added_labels.add(data['Type'])

        # Label for the Y-axis
        y_tick_labels.append(f'Block {b_id} ({block.initial_size}K)')


    # Configure the plot
    ax.set_yticks([b.bid for b in initial_blocks])
    ax.set_yticklabels(y_tick_labels)
    ax.set_xlabel("Memory Size (KB)")
    ax.set_title(title)
    ax.invert_yaxis() # Display Block 1 at the top
    
    # Attempt to show legend but handle potential duplicates
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    ax.legend(unique_labels.values(), unique_labels.keys(), loc='lower right')
    
    plt.tight_layout()

    # Save or show the plot
    if HEADLESS:
        filename = title.replace(" ", "").replace("-", "") + ".png"
        plt.savefig(filename)
        print(f"Saved Memory Map to: {filename}")
    else:
        plt.show()

    plt.close()


# ----------------------------
# STEP 5: MAIN
# ----------------------------
def main():
    """
    Main driver function for the memory allocation simulation.
    """
    # 1. Generate input data
    initial_blocks, initial_processes = generate_input_data()
    
    print("## 📄 Input Data")
    print("-----------------------------------------")
    print(f"Initial Free Blocks: {[b.size for b in initial_blocks]} KB")
    print(f"Processes (PID: Size): {[f'P{p.pid}:{p.size}K' for p in initial_processes]}")
    print("-----------------------------------------")

    # 2. Setup algorithms
    algos = {
        "First-Fit": first_fit_logic,
        "Best-Fit": best_fit_logic,
        "Worst-Fit": worst_fit_logic,
    }

    summary = []
    
    # 3. Run and compare algorithms
    for name, func in algos.items():
        # The allocate function ensures we start with fresh copies of blocks/processes
        final_blocks, final_processes = allocate(initial_blocks, initial_processes, func, name)
        
        # Compute metrics
        metrics = compute_metrics(final_blocks, final_processes, initial_blocks)

        # Create DataFrame for process-level results
        p_data = [{
            "PID": p.pid, 
            "Size": p.size, 
            "Status": p.status, 
            "Block ID": p.allocated_block_id if p.status == "ALLOCATED" else '-',
            "Int. Frag": p.fragmentation if p.status == "ALLOCATED" else 0
        } for p in final_processes]
        df_res = pd.DataFrame(p_data)

        print(f"\n--- {name} Allocation Results ---")
        print(df_res)
        print(f"Total Internal Fragmentation: {metrics['Total_Internal_Frag']} KB")
        print(f"Total External Fragmentation (Remaining Free): {metrics['Total_External_Frag']} KB")
        print(f"Total Process Size Failed to Allocate: {metrics['Failed_Processes_Size']} KB")

        # Generate Memory Map visualization
        plot_memory_map(final_blocks, f"Memory Map - {name}", initial_blocks)
        
        # Add to summary
        summary.append((
            name,
            metrics['Total_Internal_Frag'],
            metrics['Total_External_Frag'],
            metrics['Failed_Processes_Size']
        ))

    # 4. Print Summary Comparison
    print("\n## ⚖️ Summary Comparison")
    summary_df = pd.DataFrame(summary, columns=["Algorithm", "Total Int. Frag", "Total Ext. Frag", "Failed Proc. Size"])
    print(summary_df)
    
    print("\n")


# Run the main function only when executed directly
if __name__ == "__main__":
    main()
