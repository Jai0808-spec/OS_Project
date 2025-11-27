# EC2_SETUP.md
## AWS EC2 Setup Guide for OS Scheduling Project

This document explains how to:

- Launch an EC2 instance  
- Connect using SSH  
- Upload project files  
- Install Python & dependencies  
- Run the scheduling simulator  
- Download Gantt charts  

---

# 1. Launch EC2 Instance

### Step 1 — Open AWS Console  
![Step 1 AWS Console](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20191436.png)

1. Go to **AWS Console → EC2**  

### Step 2 — Open EC2 Dashboard and Click Launch Instance
![Step 3 EC2 Dashboard](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20191600.png)

2. After Clicking Launch Instance 

![Launch Instance](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20191640.png)
![Key Value Pair](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20191835.png)


3. Choose AMI → **Red Hat Linux**  
4. Instance type → **t3.micro (Free-tier eligible)**  
5. Create/Select Key Pair → download `.pem` file  
6. Configure security group:  
   - Allow **SSH (port 22)** from *My IP*  
7. Click **Launch Instance** then Click 'Connect'

![Instance Details](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20191931.png)


---

# 2. Fix Permissions for .pem Key (Windows)

Open PowerShell in the folder containing your keypair.pem:

```powershell
icacls keypair.pem /inheritance:r
icacls keypair.pem /grant:r "$($env:UserName):(R)"
```

---

![SSH Instructions](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20192004.png)

# 3. SSH Into EC2

Use your EC2 public DNS:

```powershell
ssh -i "os_group_project.pem" ec2-user@ec2-3-236-17-16.compute-1.amazonaws.com
```

If prompted → type **yes**.

You are now inside the Linux machine.

---
![Step 1 AWS Console]([img/IMAGE!7.jpg](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20192118.png))

# 4. Upload Project Files to EC2 (SCP)

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


# 5. Install Python & Required Libraries

Inside the EC2 terminal:

```bash
sudo yum install -y python3 python3-pip
pip3 install pandas matplotlib
```

---
![Python Install Screenshot](https://github.com/Jai0808-spec/OS_Project/blob/main/images/Screenshot%202025-11-27%20192820.png)

# 6. Run the Scheduling Simulator

```bash
python3 Process_Scheduling.py
python3 Memory_Scheduling.py
```

This will:

- Fetch live Linux processes  
- Run FCFS, SJF, Priority, RR  
- Produce comparison tables  
- Generate Gantt charts as `.png` images
- Run Memory menagement algorithms
- Fetch Memory of processes on linux

Check generated images:

```bash
ls *.png
```

---

# 7. Download Gantt Charts to Your Laptop

From your local system:

```powershell
scp -i "keypair.pem" ec2-user@ec2-44-212-94-109.compute-1.amazonaws.com:/home/ec2-user/*.png .
```

This downloads all charts into your current folder.

---

# Notes

- Use **ec2-user** for Red Hat Linux  
- Ensure port 22 SSH is allowed  
- EC2 is headless → charts are saved, not displayed  
- You can screenshot generated images later for your report  

---

# Done!

