#  OS Project: Scheduling and Memory Management Simulation

This repository is where processes stop waiting and memory stops wasting. 

##  Project Overview

This project implements and simulates core algorithms from Operating Systems (OS) and demonstrates their practical relevance by integrating with system-level data from a Linux environment.
The simulations are written entirely in Python and cover two main focus areas:
**Process Scheduling:** Simulating different CPU scheduling policies.
 **Memory Management:** Simulating different memory allocation strategies.

### Learning Objectives

To strengthen the understanding of OS fundamentals (scheduling, memory management, etc.).
To gain practical exposure to Linux commands and system-level resource management.

---

##  Focus Areas and Algorithms

### 1. Process Scheduling Module (`Process_Scheduling.py`)

This module implements and compares four primary scheduling algorithms:

| Algorithm | Type | Description |
| :--- | :--- | :--- |
| **FCFS** (First-Come, First-Served) | Non-Preemptive | Processes are executed in the order of their arrival time. |
| **SJF** (Shortest Job First) | Non-Preemptive | The process with the smallest CPU burst time is executed next. |
| **Round Robin** | Preemptive | Each process is given a fixed time slice (quantum) to execute before being preempted. |
| **Priority Scheduling** | Preemptive/Non-Preemptive | The process with the highest priority level is executed first. |

**Linux Integration:**
The script executes the `ps aux` command via the `subprocess` module to fetch a real-time snapshot of active processes on the host machine. The simulated performance metrics (e.g., Average Waiting Time) are then compared against the actual CPU scheduling complexity of the Linux kernel.

### 2. Memory Management Module (`Memory_Management.py`)

This module implements and compares four key memory allocation strategies:

| Algorithm | Strategy | Description |
| :--- | :--- | :--- |
| **First-Fit** | Dynamic Partition | Allocates the process to the first memory partition large enough to hold it. |
| **Best-Fit** | Dynamic Partition | Allocates the process to the smallest memory partition that is large enough, minimizing internal fragmentation. |
| **Worst-Fit** | Dynamic Partition | Allocates the process to the largest available memory partition, maximizing remaining space. |
| **Next-Fit** | Dynamic Partition | A variation of First-Fit that starts searching for the next suitable block from where the last search ended. |

**Linux Integration:**
The script executes the `free -h` command to display the host machine's memory usage (Total, Used, Free). This is used to compare theoretical fragmentation calculations with the kernel's real-time memory management (including buffers and cache).

---

##  Getting Started

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

##  Group Members:

* *Jai Lodha*
* *Yuvaraj Guliani*
* *Gurpreetsingh Sangari*
* *Aaryaveer Katoch*
* *Eashaan Marwah*
  
