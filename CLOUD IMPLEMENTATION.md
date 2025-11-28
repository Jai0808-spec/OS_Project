# CLOUD IMPLEMENTATION.md
## AWS EC2 Setup Guide for OS: Process Scheduling and Memory Management Project

This document explains how to:

- Launch an EC2 instance  
- Connect using SSH  
- Upload project files  
- Install Python & dependencies  
- Run the scheduling simulator  
- Run the Memory Management simulator
- Fetch live Linux processes data  

---

# 1. Launch EC2 Instance

### Step 1 — Open AWS Console  
![Step 1 AWS Console](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20191436.png)

### Step 2 — Open EC2 Dashboard and Click Launch Instance
![Step 3 EC2 Dashboard](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20191600.png)

After Clicking Launch Instance 

![Launch Instance](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-28%20215606.png)

Choose AMI → **Red Hat Linux**  
Instance type → **t3.micro (Free-tier eligible)**  
Create/Select Key Pair → download `.pem` file
   
![Key Value Pair](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20191835.png)

Configure security group:  
   - Allow **SSH (port 22)** from *My IP*  
Click **Launch Instance** then Click 'Connect'

![Instance Details](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20191931.png)


---

# 2.  Connection using SSH Client


![SSH Instructions](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20192004.png)

# 3. SSH Into EC2

Use your EC2 public DNS:

```powershell
ssh -i "os_group_project.pem" ec2-user@<your-public-dns>

```

If prompted → type **yes**.

You are now inside the Linux machine.

---
![Step 1 AWS Console](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20192118.png)

# 4. Upload Github Repository into EC2 Instance

From your laptop:

```powershell
ssh -i "os_group_project.pem" ec2-user@ec2-3-236-17-16.compute-1.amazonaws.com
```

Verify on EC2:

```bash
ls
```

---
![Upload Files Screenshot](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20192547.png)


# 5. Installation of Python and Necessary Libraries

Inside the EC2 terminal:

```bash
sudo yum install -y python3
python3-pip
pip3 install pandas matplotlib
```

---
![Python Install Screenshot](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20192820.png)

# 6. Run Both Simulators along the Linux Integration

```bash
python3 Process_Scheduling.py
python3 Memory_Management.py
```

This will:

- Fetch live Linux processes  
- Run FCFS, SJF, Pre-emptive Priority(SRTF), Round Robin  
- Produce comparison tables  
- Generate Gantt charts
- Generate Turnaround Time and Waiting Time
- Run Memory management algorithms
- Produce Memory Allocation Diagrams
- Generate Internal and External Fragmentation
- Fetch Memory of processes on linux



# Notes

- Use **ec2-user** for Red Hat Linux  
- Ensure port 22 SSH is allowed  

