import subprocess
import shlex
import copy
from collections import deque

# --- SCHEDULING ALGORITHM FUNCTIONS ---

def simulate_fcfs(processes_data):
    """Implements the First-Come, First-Served (FCFS) Scheduling Algorithm."""
    print("### Algorithm: FCFS")
    
    # Sort processes by Arrival Time
    processes_data.sort(key=lambda x: x[1]) 
    
    total_waiting_time = 0
    total_turnaround_time = 0
    completion_time = 0
    results = []

    for name, arrival, burst in processes_data:
        start_time = max(completion_time, arrival)
        waiting_time = start_time - arrival
        completion_time = start_time + burst
        turnaround_time = completion_time - arrival
        
        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time
        results.append((name, waiting_time, turnaround_time))

    num_processes = len(processes_data)
    avg_waiting_time = total_waiting_time / num_processes
    avg_turnaround_time = total_turnaround_time / num_processes

    print("Process | Waiting Time (ms) | Turnaround Time (ms)")
    print("-" * 45)
    for name, wt, tt in results:
        print(f"{name:<7} | {wt:<17} | {tt}")
        
    print(f"\n* Average Waiting Time: {avg_waiting_time:.2f} ms")
    print(f"* Average Turnaround Time: {avg_turnaround_time:.2f} ms")
    # 

[Image of FCFS Gantt Chart]
 is not relevant here as the image is about Critical Path Method (CPM).
    print("[Placeholder: Insert your FCFS Gantt Chart visualization here]")


def simulate_sjf(processes_data):
    """Implements the non-preemptive Shortest Job First (SJF) Scheduling Algorithm."""
    print("### Algorithm: SJF (Non-Preemptive)")
    
    processes_data.sort(key=lambda x: x[1]) # Sort by Arrival Time initially
    
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    completed_processes = 0
    num_processes = len(processes_data)
    
    # Working list: [Name, Arrival, Burst, is_completed]
    working_list = [list(p) + [False] for p in processes_data]
    results = []
    
    while completed_processes < num_processes:
        # Find available jobs
        available_jobs = [p for p in working_list if p[1] <= current_time and p[3] == False]
        
        if not available_jobs:
            # If CPU is idle, advance time to the next arrival
            if completed_processes < num_processes:
                next_arrival = min(p[1] for p in working_list if p[3] == False)
                current_time = next_arrival
            continue

        # Select the shortest job (SJF criterion)
        available_jobs.sort(key=lambda x: x[2])
        selected_job = available_jobs[0]
        
        name, arrival, burst, _ = selected_job
        
        # Calculate metrics
        start_time = current_time
        completion_time = start_time + burst
        waiting_time = start_time - arrival
        turnaround_time = completion_time - arrival
        
        # Update state
        current_time = completion_time
        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time
        
        # Mark the job as completed
        for p in working_list:
            if p[0] == name and p[3] == False:
                p[3] = True
                break
                
        results.append((name, waiting_time, turnaround_time))
        completed_processes += 1

    # Display Metrics
    avg_waiting_time = total_waiting_time / num_processes
    avg_turnaround_time = total_turnaround_time / num_processes

    print("Process | Waiting Time (ms) | Turnaround Time (ms)")
    print("-" * 45)
    for name, wt, tt in results:
        print(f"{name:<7} | {wt:<17} | {tt}")
        
    print(f"\n* Average Waiting Time: {avg_waiting_time:.2f} ms")
    print(f"* Average Turnaround Time: {avg_turnaround_time:.2f} ms")
    # 

[Image of SJF Gantt Chart]
 is not relevant here as the image is about trigonometric values.
    print("[Placeholder: Insert your SJF Gantt Chart visualization here]")


def simulate_round_robin(processes_data, quantum=2):
    """Implements the Round Robin Scheduling Algorithm."""
    print(f"### Algorithm: Round Robin (Quantum={quantum}ms)")
    
    # [Name, Arrival, Remaining Burst, Original Burst]
    ready_queue = deque()
    # Copy and augment data: [Name, Arrival, Remaining Burst, Original Burst, Waiting Time, Turnaround Time]
    proc_details = {p[0]: {'arrival': p[1], 'burst': p[2], 'remaining': p[2], 'start_time': -1, 'wait': 0, 'turnaround': 0, 'completed': False} for p in processes_data}

    # Sort processes by arrival time for initial queue loading
    sorted_processes = sorted(processes_data, key=lambda x: x[1])
    
    current_time = 0
    process_index = 0
    
    while process_index < len(sorted_processes) or ready_queue:
        
        # 1. Check for new arrivals and add them to the queue
        while process_index < len(sorted_processes) and sorted_processes[process_index][1] <= current_time:
            ready_queue.append(sorted_processes[process_index][0])
            process_index += 1
            
        if ready_queue:
            current_proc_name = ready_queue.popleft()
            details = proc_details[current_proc_name]

            # Determine the execution time slice
            time_slice = min(quantum, details['remaining'])
            
            # Update start time if this is the first execution
            if details['start_time'] == -1:
                details['start_time'] = current_time
            
            # Execute for time_slice
            current_time += time_slice
            details['remaining'] -= time_slice
            
            # 2. Add any processes that arrived during this time slice
            while process_index < len(sorted_processes) and sorted_processes[process_index][1] <= current_time:
                ready_queue.append(sorted_processes[process_index][0])
                process_index += 1
            
            # 3. Check for completion and requeue
            if details['remaining'] == 0:
                # Completed
                details['completed'] = True
                details['turnaround'] = current_time - details['arrival']
                details['wait'] = details['turnaround'] - details['burst']
            else:
                # Not completed, add back to the end of the queue
                ready_queue.append(current_proc_name)
        else:
            # CPU idle, advance time to the next arrival
            if process_index < len(sorted_processes):
                current_time = sorted_processes[process_index][1]
            else:
                # Should not happen if all processes are accounted for
                break 

    # Display Metrics
    total_wait = sum(d['wait'] for d in proc_details.values())
    total_turnaround = sum(d['turnaround'] for d in proc_details.values())
    num_processes = len(processes_data)
    avg_waiting_time = total_wait / num_processes
    avg_turnaround_time = total_turnaround / num_processes

    print("Process | Waiting Time (ms) | Turnaround Time (ms)")
    print("-" * 45)
    for name, d in sorted(proc_details.items(), key=lambda item: item[1]['arrival']):
        print(f"{name:<7} | {d['wait']:<17} | {d['turnaround']}")
        
    print(f"\n* Average Waiting Time: {avg_waiting_time:.2f} ms")
    print(f"* Average Turnaround Time: {avg_turnaround_time:.2f} ms")
    print("[Placeholder: Insert your Round Robin Gantt Chart visualization here]")


# --- LINUX INTEGRATION FUNCTION ---

def get_real_process_snapshot():
    """
    Executes the 'ps aux' Linux command to get a snapshot of running processes.
    """
    print("\n## 2. Linux System Output: Real-Time Process Snapshot")
    print("-------------------------------------------------------")
    
    command = "ps aux"
    args = shlex.split(command)
    
    try:
        result = subprocess.run(args, capture_output=True, text=True, check=True)
        
        output_lines = result.stdout.splitlines()
        
        print("PID - USER - %CPU - %MEM - START TIME - COMMAND")
        print('\n'.join(output_lines[:1]))
        print('\n'.join(output_lines[1:6]))
        print(f"... (Showing first 5 processes of {len(output_lines)-1} total) ...")
        
        print("\n--- Comparison Tip ---")
        print("Compare your calculated theoretical metrics (e.g., response time for RR) against the real-world complexity of process priority and resource usage shown above.")
        
    except Exception as e:
        print(f"Error executing Linux command 'ps aux': {e}")
        print("Please ensure this script is run on a Linux environment or WSL.")
        
# --- MAIN EXECUTION ---

if __name__ == "__main__":
    print("## Process Scheduling Simulator and Linux Integrator")
    
    # Test case data: (Process Name, Arrival Time, Burst Time)
    test_processes = [("P1", 0, 7), ("P2", 2, 4), ("P3", 4, 1), ("P4", 5, 4)]

    # --- SIMULATION SECTION ---
    print("\n------------------------------------------------------------------")
    print("RUNNING FCFS SIMULATION:")
    print("------------------------------------------------------------------")
    simulate_fcfs(copy.deepcopy(test_processes))

    print("\n------------------------------------------------------------------")
    print("RUNNING SJF SIMULATION:")
    print("------------------------------------------------------------------")
    simulate_sjf(copy.deepcopy(test_processes))
    
    print("\n------------------------------------------------------------------")
    print("RUNNING ROUND ROBIN SIMULATION:")
    print("------------------------------------------------------------------")
    simulate_round_robin(copy.deepcopy(test_processes), quantum=2)
    
    # --- LINUX INTEGRATION SECTION ---
    get_real_process_snapshot()
