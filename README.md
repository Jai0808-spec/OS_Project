# ⚙️ OS Project: Scheduling and Memory Management Simulation

## 🚀 Project Overview

This project implements and simulates core algorithms from Operating Systems (OS) and demonstrates their practical relevance by integrating with system-level data from a Linux environment.

The simulations are written entirely in Python and cover two main focus areas:

1.  **Process Scheduling:** Simulating different CPU scheduling policies.
2.  **Memory Management:** Simulating different memory allocation strategies.

### Learning Objectives

* To strengthen the understanding of OS fundamentals (scheduling, memory management).
* To gain practical exposure to Linux commands and system-level resource management.

---

## 🛠️ Focus Areas and Algorithms

### 1. Process Scheduling Module (`Process_Scheduling.py`)

| Algorithm | Type | Description |
| :--- | :--- | :--- |
| **FCFS** | Non-Preemptive | Processes are executed in the order of their arrival time. |
| **SJF** | Non-Preemptive | The process with the smallest CPU burst time is executed next. |
| **Round Robin** | Preemptive | Each process is given a fixed time slice (quantum) to execute. |

**Linux Integration:**
The script executes the `ps aux` command via the `subprocess` module to fetch a real-time snapshot of active processes on the host machine. The simulated performance metrics (e.g., Average Waiting Time) are then compared against the **actual CPU scheduling complexity** of the Linux kernel.

### 2. Memory Management Module (`Memory_Management.py`)

| Algorithm | Strategy | Description |
| :--- | :--- | :--- |
| **First-Fit** | Dynamic Partition | Allocates the process to the first memory partition large enough to hold it. |
| **Best-Fit** | Dynamic Partition | Allocates the process to the smallest memory partition that is large enough, minimizing internal fragmentation. |
| **Worst-Fit** | Dynamic Partition | Allocates the process to the largest available memory partition, maximizing remaining space. |

**Linux Integration:**
The script executes the `free -h` command to display the host machine's memory usage (Total, Used, Free). This is used to compare theoretical fragmentation calculations with the kernel's **real-time memory management** (including buffers and cache).

---

## 🚀 Getting Started

### Prerequisites

* A Linux environment (Ubuntu, Debian, WSL, etc.)
* Python 3.x installed

### Installation

No special libraries are required beyond Python's built-in modules (`subprocess`, `shlex`, `copy`, `collections`) used for the algorithms and Linux integration.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your_username/OS_Project.git](https://github.com/your_username/OS_Project.git)
    cd OS_Project
    ```

### Usage

Run either simulation file directly using Python 3.

1.  **Run Process Scheduling Simulation:**
    ```bash
    python3 Process_Scheduling.py
    ```
    *(Output includes FCFS, SJF, RR metrics and the live `ps aux` output.)*

2.  **Run Memory Management Simulation:**
    ```bash
    python3 Memory_Management.py
    ```
    *(Output includes Best-Fit, First-Fit, Worst-Fit allocation tables and the live `free -h` output.)*

---

## 📊 Results and Comparison

The final project requires visual outputs and a critical comparison:

* **Process Scheduling:** Tabular outputs of waiting/turnaround times and **Gantt Charts** must be generated.
* **Memory Management:** Tabular outputs and **Memory Allocation Diagrams** must be generated.

Screenshots of the Python output running alongside the relevant Linux command output are a required deliverable.

---

## 📞 Contact and Contributions

* **Owner:** [Your GitHub Username]
* **Project Link:** [Your full GitHub URL]
* *(Optional: Add a section on how to report issues or suggest features)*
