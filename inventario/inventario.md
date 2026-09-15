# Inventário do ambiente

Coletado em: 2026-09-14 19:17:57

## uname
```
Linux MATEUS 6.18.33.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun 18 21:54:43 UTC 2026 x86_64 GNU/Linux
```

## os release
```
PRETTY_NAME="Ubuntu 26.04 LTS"
NAME="Ubuntu"
VERSION_ID="26.04"
VERSION="26.04 (Resolute Raccoon)"
VERSION_CODENAME=resolute
ID=ubuntu
ID_LIKE=debian
HOME_URL="https://www.ubuntu.com/"
SUPPORT_URL="https://help.ubuntu.com/"
BUG_REPORT_URL="https://bugs.launchpad.net/ubuntu/"
PRIVACY_POLICY_URL="https://www.ubuntu.com/legal/terms-and-policies/privacy-policy"
UBUNTU_CODENAME=resolute
LOGO=ubuntu-logo
```

## ambiente wsl
```
Linux version 6.18.33.2-microsoft-standard-WSL2 (root@f1bbfb02316b) (gcc (GCC) 13.2.0, GNU ld (GNU Binutils) 2.41) #1 SMP PREEMPT_DYNAMIC Thu Jun 18 21:54:43 UTC 2026
```

## lscpu
```
Architecture:                            x86_64
CPU op-mode(s):                          32-bit, 64-bit
Address sizes:                           46 bits physical, 48 bits virtual
Byte Order:                              Little Endian
CPU(s):                                  28
On-line CPU(s) list:                     0-27
Vendor ID:                               GenuineIntel
Model name:                              Intel(R) Xeon(R) CPU E5-2680 v4 @ 2.40GHz
CPU family:                              6
Model:                                   79
Thread(s) per core:                      2
Core(s) per socket:                      14
Socket(s):                               1
Stepping:                                1
BogoMIPS:                                4788.90
Flags:                                   fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ss ht syscall nx pdpe1gb rdtscp lm arch_perfmon rep_good nopl xtopology cpuid tsc_known_freq pni pclmulqdq vmx ssse3 fma cx16 pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt aes xsave avx f16c rdrand hypervisor lahf_lm abm 3dnowprefetch pti ssbd ibrs ibpb stibp tpr_shadow ept vpid ept_ad fsgsbase bmi1 hle avx2 smep bmi2 erms invpcid rtm rdseed adx smap xsaveopt vnmi md_clear flush_l1d arch_capabilities
Virtualization:                          VT-x
Hypervisor vendor:                       Microsoft
Virtualization type:                     full
L1d cache:                               448 KiB (14 instances)
L1i cache:                               448 KiB (14 instances)
L2 cache:                                3.5 MiB (14 instances)
L3 cache:                                35 MiB (1 instance)
NUMA node(s):                            1
NUMA node0 CPU(s):                       0-27
Vulnerability Gather data sampling:      Not affected
Vulnerability Ghostwrite:                Not affected
Vulnerability Indirect target selection: Mitigation; Aligned branch/return thunks
Vulnerability Itlb multihit:             KVM: Mitigation: Split huge pages
Vulnerability L1tf:                      Mitigation; PTE Inversion; VMX conditional cache flushes, SMT vulnerable
Vulnerability Mds:                       Mitigation; Clear CPU buffers; SMT Host state unknown
Vulnerability Meltdown:                  Mitigation; PTI
Vulnerability Mmio stale data:           Mitigation; Clear CPU buffers; SMT Host state unknown
Vulnerability Old microcode:             Not affected
Vulnerability Reg file data sampling:    Not affected
Vulnerability Retbleed:                  Not affected
Vulnerability Spec rstack overflow:      Not affected
Vulnerability Spec store bypass:         Mitigation; Speculative Store Bypass disabled via prctl
Vulnerability Spectre v1:                Mitigation; usercopy/swapgs barriers and __user pointer sanitization
Vulnerability Spectre v2:                Mitigation; Retpolines; IBPB conditional; IBRS_FW; STIBP conditional; RSB filling; PBRSB-eIBRS Not affected; BHI Retpoline
Vulnerability Srbds:                     Not affected
Vulnerability Tsa:                       Not affected
Vulnerability Tsx async abort:           Mitigation; Clear CPU buffers; SMT Host state unknown
Vulnerability Vmscape:                   Not affected
```

## nproc
```
28
```

## free
```
               total        used        free      shared  buff/cache   available
Mem:            15Gi       1.7Gi        12Gi       3.9Mi       1.3Gi        13Gi
Swap:          4.0Gi          0B       4.0Gi
```

## df
```
Filesystem      Size  Used Avail Use% Mounted on
none            7.8G     0  7.8G   0% /usr/lib/modules/6.18.33.2-microsoft-standard-WSL2
none            7.8G  4.0K  7.8G   1% /mnt/wsl
drivers         931G  499G  432G  54% /usr/lib/wsl/drivers
/dev/sdd       1007G   33G  924G   4% /
none            7.8G   40K  7.8G   1% /mnt/wslg
none            7.8G     0  7.8G   0% /usr/lib/wsl/lib
rootfs          7.8G  2.8M  7.8G   1% /init
none            7.8G  944K  7.8G   1% /run
none            7.8G     0  7.8G   0% /run/lock
none            7.8G     0  7.8G   0% /run/shm
none            7.8G   80K  7.8G   1% /mnt/wslg/versions.txt
none            7.8G   80K  7.8G   1% /mnt/wslg/doc
C:\             931G  499G  432G  54% /mnt/c
D:\             931G  727G  205G  79% /mnt/d
none            1.0M     0  1.0M   0% /run/credentials/systemd-journald.service
tmpfs           7.8G     0  7.8G   0% /tmp
none            1.0M     0  1.0M   0% /run/credentials/systemd-resolved.service
none            1.0M     0  1.0M   0% /run/credentials/getty@tty1.service
tmpfs           1.6G   12K  1.6G   1% /run/user/1000
```

## lsblk
```
NAME MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
sda    8:0    0 356.9M  1 disk 
sdb    8:16   0 159.4M  1 disk 
sdc    8:32   0     4G  0 disk [SWAP]
sdd    8:48   0     1T  0 disk /var/lib/docker
                               /mnt/wslg/distro
                               /
```

## nvidia smi
```
Mon Sep 14 19:17:52 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 615.65.07              KMD Version: 616.64        CUDA UMD Version: 13.4     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 3060        On  |   00000000:03:00.0  On |                  N/A |
|  0%   39C    P5             18W /  170W |    1234MiB /  12288MiB |      9%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A              26      G   /Xwayland                             N/A      |
+-----------------------------------------------------------------------------------------+
```

## docker version
```
Docker version 29.8.0, build 88096ef
```

## docker ps
```
CONTAINER ID   IMAGE                                COMMAND               CREATED      STATUS                       PORTS                                             NAMES
6766198befd6   ghcr.io/open-webui/open-webui:main   "bash start.sh"       2 days ago   Up About an hour (healthy)                                                     open-webui
2827752980a5   ollama/ollama                        "/bin/ollama serve"   2 days ago   Up About an hour             0.0.0.0:11435->11434/tcp, [::]:11435->11434/tcp   ollama-cpu
30713ba09baa   ollama/ollama                        "/bin/ollama serve"   2 days ago   Up About an hour             0.0.0.0:11434->11434/tcp, [::]:11434->11434/tcp   ollama-gpu
```

## python version
```
Python 3.14.4
```

## ollama version ollama-cpu
```
ollama version is 0.34.0
```

## ollama version ollama-gpu
```
ollama version is 0.34.0
```

## ollama list ollama-cpu
```
NAME                 ID              SIZE      MODIFIED          
granite3.1-moe:3b    b43d80d7fca7    2.0 GB    About an hour ago    
phi4-mini:latest     78fad5d182a7    2.5 GB    2 days ago           
```

## ollama list ollama-gpu
```
NAME                 ID              SIZE      MODIFIED          
granite3.1-moe:3b    b43d80d7fca7    2.0 GB    About an hour ago    
phi4-mini:latest     78fad5d182a7    2.5 GB    2 days ago           
```

## open webui imagem
```
ghcr.io/open-webui/open-webui:main | Criado em: 2026-09-12T15:32:42.646143061Z | Digest: sha256:1a6399d237dc392a2313e0ca826020b3fd5d22536357840eb63393d18dc8b924
```

