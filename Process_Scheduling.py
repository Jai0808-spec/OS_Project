import subprocess
import shlex
import copy
from collections import deque
import time

# --- VISUALIZATION FUNCTION ---

def display_gantt_chart(gantt_chart_data, algorithm_name):
    """
    Displays a simple text/ASCII Gantt Chart based on execution history.
    gantt_chart_data is a list of tuples: [(process_name, start_time, end_time), ...]
    """
    if not gantt_chart_data:
        print("Gantt Chart: No processes executed.")
        return

    # Filter out IDLE periods for accurate chart generation (though they can be useful)
    gantt_chart_data = [(n, s, e) for n, s, e in gantt_chart_data if n != "IDLE"]
    if not gantt_chart_data:
        print("Gantt Chart: Only IDLE periods observed.")
        return

    # Sort data by start time
    gantt_chart_data.sort(key=lambda x: x[1])

    chart_line = "|"
    time_line = "0"
    
    current_time = 0

    for name, start, end in gantt_chart_data:
        # Handle Idle Time
        if start > current_time:
            idle_duration = start - current_time
            chart_line += " IDLE " + " " * (idle_duration - 1) + "|"
            time_line += " " * (len(" IDLE ") + idle_duration - 1)
            # The time scale is complex to draw perfectly with variable width; 
            # we simply advance the time line mark.
            current_time = start

        # Draw the process block
        duration = end - start
        block_text = f" {name} "
        
        # Adjust padding for visual alignment (simplified for ASCII)
        block_width = max(len(block_text), duration) 
        
        chart_line += block_text.center(block_width, '=') + "|"
        time_line += "-" * block_width
        time_line += str(end)
        current_time = end

    print(f"\n--- Gantt Chart: {algorithm_name} ---")
    print(chart_line)
    print(time_line)
    print("---------------------------------")


# --- SCHEDULING ALGORITHM FUNCTIONS ---

def simulate_fcfs(processes_data):
    """Implements the First-Come, First-Served (FCFS) Scheduling Algorithm."""
    print("### Algorithm: FCFS")
    processes_data.sort(key=lambda x: x[1]) 
    
    total_waiting_time = 0
    total_turnaround_time = 0
    completion_time = 0
    # Updated results list: (Name, AT, BT, CT, WT, TT)
    results = []
    gantt_chart = []

    for name, arrival, burst in processes_data:
        start_time = max(completion_time, arrival)
        waiting_time = start_time - arrival
        completion_time = start_time + burst
        turnaround_time = completion_time - arrival
        
        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time
        results.append((name, arrival, burst, completion_time, waiting_time, turnaround_time))
        gantt_chart.append((name, start_time, completion_time))

    num_processes = len(processes_data)
    avg_waiting_time = total_waiting_time / num_processes
    avg_turnaround_time = total_turnaround_time / num_processes

    # Updated Output Table
    print("Process | AT | BT | CT | Waiting Time (ms) | Turnaround Time (ms)")
    print("-" * 65)
    for name, at, bt, ct, wt, tt in results:
        print(f"{name:<7} | {at:<2} | {bt:<2} | {ct:<2} | {wt:<17} | {tt}")
        
    print(f"\n* Average Waiting Time: {avg_waiting_time:.2f} ms")
    print(f"* Average Turnaround Time: {avg_turnaround_time:.2f} ms")
    display_gantt_chart(gantt_chart, "FCFS")


def simulate_sjf(processes_data):
    """Implements the non-preemptive Shortest Job First (SJF) Scheduling Algorithm."""
    print("### Algorithm: SJF (Non-Preemptive)")
    processes_data.sort(key=lambda x: x[1]) 
    
    current_time = 0
    total_waiting_time = 0
    total_turnaround_time = 0
    completed_processes = 0
    num_processes = len(processes_data)
    
    working_list = [list(p) + [False] for p in processes_data] # [Name, Arrival, Burst, is_completed]
    results = []
    gantt_chart = []
    
    while completed_processes < num_processes:
        available_jobs = [p for p in working_list if p[1] <= current_time and p[3] == False]
        
        if not available_jobs:
            if completed_processes < num_processes:
                next_arrival = min(p[1] for p in working_list if p[3] == False)
                gantt_chart.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
            continue

        # Select the shortest job (SJF criterion)
        available_jobs.sort(key=lambda x: x[2])
        selected_job = available_jobs[0]
        
        name, arrival, burst, _ = selected_job
        
        start_time = current_time
        completion_time = start_time + burst
        waiting_time = start_time - arrival
        turnaround_time = completion_time - arrival
        
        current_time = completion_time
        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time
        
        for p in working_list:
            if p[0] == name and p[3] == False:
                p[3] = True
                break
                
        results.append((name, arrival, burst, completion_time, waiting_time, turnaround_time))
        gantt_chart.append((name, start_time, completion_time))
        completed_processes += 1

    avg_waiting_time = total_waiting_time / num_processes
    avg_turnaround_time = total_turnaround_time / num_processes

    # Updated Output Table
    print("Process | AT | BT | CT | Waiting Time (ms) | Turnaround Time (ms)")
    print("-" * 65)
    for name, at, bt, ct, wt, tt in results:
        print(f"{name:<7} | {at:<2} | {bt:<2} | {ct:<2} | {wt:<17} | {tt}")
        
    print(f"\n* Average Waiting Time: {avg_waiting_time:.2f} ms")
    print(f"* Average Turnaround Time: {avg_turnaround_time:.2f} ms")
    display_gantt_chart(gantt_chart, "SJF")


def simulate_round_robin(processes_data, quantum=2):
    """Implements the Round Robin Scheduling Algorithm."""
    print(f"### Algorithm: Round Robin (Quantum={quantum}ms)")
    
    proc_details = {p[0]: {'arrival': p[1], 'burst': p[2], 'remaining': p[2], 'start_time': -1, 'wait': 0, 'turnaround': 0, 'completed': False} for p in processes_data}
    sorted_processes = sorted(processes_data, key=lambda x: x[1])
    ready_queue = deque()
    gantt_chart = []
    
    current_time = 0
    process_index = 0
    
    while process_index < len(sorted_processes) or ready_queue:
        
        # 1. Check for new arrivals
        while process_index < len(sorted_processes) and sorted_processes[process_index][1] <= current_time:
            ready_queue.append(sorted_processes[process_index][0])
            process_index += 1
            
        if ready_queue:
            current_proc_name = ready_queue.popleft()
            details = proc_details[current_proc_name]

            time_slice = min(quantum, details['remaining'])
            
            if details['start_time'] == -1:
                details['start_time'] = current_time
            
            start_of_slice = current_time
            current_time += time_slice
            details['remaining'] -= time_slice
            
            gantt_chart.append((current_proc_name, start_of_slice, current_time))
            
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
                details['completion_time'] = current_time # Store CT
            else:
                ready_queue.append(current_proc_name)
        else:
            # CPU idle
            if process_index < len(sorted_processes):
                next_arrival = sorted_processes[process_index][1]
                gantt_chart.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
            else:
                break 

    # Display Metrics
    total_wait = sum(d['wait'] for d in proc_details.values())
    total_turnaround = sum(d['turnaround'] for d in proc_details.values())
    num_processes = len(processes_data)
    avg_waiting_time = total_wait / num_processes
    avg_turnaround_time = total_turnaround / num_processes

    # Updated Output Table
    print("Process | AT | BT | CT | Waiting Time (ms) | Turnaround Time (ms)")
    print("-" * 65)
    for name, d in sorted(proc_details.items(), key=lambda item: item[1]['arrival']):
        ct = d.get('completion_time', 'N/A')
        print(f"{name:<7} | {d['arrival']:<2} | {d['burst']:<2} | {ct:<2} | {d['wait']:<17} | {d['turnaround']}")
        
    print(f"\n* Average Waiting Time: {avg_waiting_time:.2f} ms")
    print(f"* Average Turnaround Time: {avg_turnaround_time:.2f} ms")
    display_gantt_chart(gantt_chart, f"Round Robin (Q={quantum})")


def simulate_priority_preemptive(processes_data):
    """
    Implements Preemptive Priority Scheduling (SRTF-style preemption based on priority).
    processes_data: [(name, arrival, burst, priority), ...]
    Lower number = Higher Priority.
    """
    print("### Algorithm: Preemptive Priority (SRTF-style)")

    current_time = 0
    num_processes = len(processes_data)
    
    # [Name, Arrival, Burst, Priority, Remaining, Completed, StartTime, FinishTime]
    details = {p[0]: {'arrival': p[1], 'burst': p[2], 'priority': p[3], 'remaining': p[2], 
                      'completed': False, 'start_time': -1, 'finish_time': -1} for p in processes_data}
    
    gantt_chart = []
    
    # Calculate max time for simulation boundary
    max_arrival = max(p[1] for p in processes_data)
    total_burst = sum(p[2] for p in processes_data)
    max_time = max_arrival + total_burst + 1 # Add one for safety
    
    while current_time < max_time and sum(1 for d in details.values() if not d['completed']) > 0:
        
        # 1. Identify all available processes (arrived and not completed)
        available = [name for name, d in details.items() 
                     if d['arrival'] <= current_time and not d['completed']]
        
        if not available:
            # CPU is idle: advance time to the next arrival
            if current_time < max_arrival:
                next_arrival = min(d['arrival'] for d in details.values() if d['arrival'] > current_time)
                gantt_chart.append(("IDLE", current_time, next_arrival))
                current_time = next_arrival
            else:
                current_time += 1
            continue

        # 2. Select the highest priority process (lower priority number = higher priority)
        current_process = min(available, key=lambda name: details[name]['priority'])
        current_details = details[current_process]
        
        # 3. Find the next event time (next arrival of a HIGHER priority process or completion)
        
        # Time until the current process finishes
        time_to_finish = current_details['remaining']

        # Next event time is initially completion time
        next_event_time = current_time + time_to_finish
        
        # Check for future arrivals of processes with higher priority (lower number)
        for name, d in details.items():
            if d['arrival'] > current_time and d['priority'] < current_details['priority']:
                # Preemption point is the arrival time of the higher priority process
                if d['arrival'] < next_event_time:
                    next_event_time = d['arrival']
        
        time_slice = next_event_time - current_time
        
        # 4. Execute for the calculated time slice
        if current_details['start_time'] == -1:
            current_details['start_time'] = current_time

        gantt_chart.append((current_process, current_time, current_time + time_slice))
        current_time += time_slice
        current_details['remaining'] -= time_slice
        
        # 5. Check for completion
        if current_details['remaining'] == 0:
            current_details['completed'] = True
            current_details['finish_time'] = current_time

    # Calculate final metrics
    total_wait = 0
    total_turnaround = 0
    results = []

    for name, d in details.items():
        turnaround = d['finish_time'] - d['arrival']
        wait = turnaround - d['burst']
        total_wait += wait
        total_turnaround += turnaround
        results.append((name, d['arrival'], d['burst'], d['priority'], d['finish_time'], wait, turnaround))

    avg_waiting_time = total_wait / num_processes
    avg_turnaround_time = total_turnaround / num_processes

    # Updated Output Table
    print("Process | AT | BT | Priority | CT | Waiting Time (ms) | Turnaround Time (ms)")
    print("-" * 78)
    for name, at, bt, p, ct, wt, tt in results:
        print(f"{name:<7} | {at:<2} | {bt:<2} | {p:<8} | {ct:<2} | {wt:<17} | {tt}")

    print(f"\n* Average Waiting Time: {avg_waiting_time:.2f} ms")
    print(f"* Average Turnaround Time: {avg_turnaround_time:.2f} ms")
    display_gantt_chart(gantt_chart, "Preemptive Priority")


# --- LINUX INTEGRATION FUNCTION ---

def get_real_process_snapshot():
    """Executes the 'ps aux' Linux command to get a snapshot of running processes."""
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
        print("Compare your calculated theoretical metrics against the real-world complexity of process priority and resource usage shown above.")
        
    except Exception as e:
        print(f"Error executing Linux command 'ps aux': {e}")
        print("Please ensure this script is run on a Linux environment or WSL.")
        
# --- MAIN EXECUTION ---

if __name__ == "__main__":
    print("## Process Scheduling Simulator and Linux Integrator")
    
    # Test case data: (Process Name, Arrival Time, Burst Time, Priority)
    # Lower number = Higher Priority (e.g., P2 is highest priority)
    test_processes_with_priority = [
        ("P1", 0, 7, 2), 
        ("P2", 2, 4, 1), 
        ("P3", 4, 1, 3), 
        ("P4", 5, 4, 4)
    ]
    # Data without priority for FCFS, SJF, RR
    test_processes_no_priority = [(p[0], p[1], p[2]) for p in test_processes_with_priority]

    # --- SIMULATION SECTION ---
    print("\n------------------------------------------------------------------")
    print("RUNNING FCFS SIMULATION:")
    print("------------------------------------------------------------------")
    simulate_fcfs(copy.deepcopy(test_processes_no_priority))

    print("\n------------------------------------------------------------------")
    print("RUNNING SJF SIMULATION:")
    print("------------------------------------------------------------------")
    simulate_sjf(copy.deepcopy(test_processes_no_priority))
    
    print("\n------------------------------------------------------------------")
    print("RUNNING ROUND ROBIN SIMULATION:")
    print("------------------------------------------------------------------")
    simulate_round_robin(copy.deepcopy(test_processes_no_priority), quantum=2)

    print("\n------------------------------------------------------------------")
    print("RUNNING PREEMPTIVE PRIORITY SIMULATION:")
    print("------------------------------------------------------------------")
    simulate_priority_preemptive(copy.deepcopy(test_processes_with_priority))
    
    # --- LINUX INTEGRATION SECTION ---
    get_real_process_snapshot()
