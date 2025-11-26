#  OS Project: Scheduling and Memory Management Simulation

##  Project Overview

This project implements and simulates core algorithms from Operating Systems (OS) and demonstrates their practical relevance by integrating with system-level data from a Linux environment[cite: 3, 4].
[cite_start]The simulations are written entirely in Python and cover two main focus areas[cite: 11]:
* [cite_start]**Process Scheduling:** Simulating different CPU scheduling policies[cite: 6].
* [cite_start]**Memory Management:** Simulating different memory allocation strategies[cite: 6].

### Learning Objectives

* [cite_start]To strengthen the understanding of OS fundamentals (scheduling, memory management, etc.)[cite: 6].
* [cite_start]To gain practical exposure to Linux commands and system-level resource management[cite: 7, 4].

---

## 🛠️ Focus Areas and Algorithms

### 1. Process Scheduling Module (`Process_Scheduling.py`)

[cite_start]This module implements and compares four primary scheduling algorithms[cite: 12]:

| Algorithm | Type | Description |
| :--- | :--- | :--- |
| **FCFS** (First-Come, First-Served) | Non-Preemptive | Processes are executed in the order of their arrival time. |
| **SJF** (Shortest Job First) | Non-Preemptive | The process with the smallest CPU burst time is executed next. |
| **Round Robin** | Preemptive | [cite_start]Each process is given a fixed time slice (quantum) to execute before being preempted[cite: 12]. |
| **Priority Scheduling** | Preemptive/Non-Preemptive | The process with the highest priority level is executed first. |

**Linux Integration:**
[cite_start]The script executes the `ps aux` command via the `subprocess` module to fetch a real-time snapshot of active processes on the host machine[cite: 18]. [cite_start]The simulated performance metrics (e.g., Average Waiting Time) are then compared against the actual CPU scheduling complexity of the Linux kernel[cite: 19].

### 2. Memory Management Module (`Memory_Management.py`)

[cite_start]This module implements and compares four key memory allocation strategies[cite: 13]:

| Algorithm | Strategy | Description |
| :--- | :--- | :--- |
| **First-Fit** | Dynamic Partition | [cite_start]Allocates the process to the first memory partition large enough to hold it[cite: 13]. |
| **Best-Fit** | Dynamic Partition | [cite_start]Allocates the process to the smallest memory partition that is large enough, minimizing internal fragmentation[cite: 13]. |
| **Worst-Fit** | Dynamic Partition | [cite_start]Allocates the process to the largest available memory partition, maximizing remaining space[cite: 13]. |
| **Next-Fit** | Dynamic Partition | A variation of First-Fit that starts searching for the next suitable block from where the last search ended. |

**Linux Integration:**
[cite_start]The script executes the `free -h` command to display the host machine's memory usage (Total, Used, Free)[cite: 18]. [cite_start]This is used to compare theoretical fragmentation calculations with the kernel's real-time memory management (including buffers and cache)[cite: 19].

---

## 🚀 Getting Started

### Prerequisites

* A **Linux environment** (Ubuntu, Debian, WSL, etc.)
* **Python 3.x** installed


### Usage

Run either simulation file directly using Python 3.

* **Run Process Scheduling Simulation:**
    ```bash
    python3 Process_Scheduling.py
    ```
    (Output includes FCFS, SJF, RR, Priority metrics and the live `ps aux` output.)
* **Run Memory Management Simulation:**
    ```bash
    python3 Memory_Management.py
    ```
    (Output includes First-Fit, Best-Fit, Worst-Fit, Next-Fit allocation tables and the live `free -h` output.)
---

## 📞 Contact and Contributions

* **Owner:** [Your GitHub Username]
* **Project Link:** [Your full GitHub URL]
