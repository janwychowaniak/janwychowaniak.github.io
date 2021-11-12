---
layout: post
title:  "Partitions on your hard drive and their details"
date:   2020-09-14 13:35:18 +0200
categories: linux hardware
---

Following is a short cheat sheet with a handful of commands helpful for getting yourself oriented in the partition layout of your hard drive.

All the commands below I have performed on machines equipped with a single hard disk reporting itself as `/dev/sda`. Therefore this is what all the command examples that follow contain.


#### lsblk

Listing block devices:

```bash
lsblk
lsblk /dev/sda
```

An example output for `/dev/sda`:

{:.jwoutput}
```
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0   477G  0 disk 
├─sda1   8:1    0    75G  0 part 
├─sda2   8:2    0     1K  0 part 
├─sda3   8:3    0    45G  0 part 
├─sda5   8:5    0   5,5G  0 part [SWAP]
├─sda6   8:6    0   196G  0 part 
├─sda7   8:7    0  18,3G  0 part /
└─sda8   8:8    0 137,2G  0 part /home
```

#### fdisk

Peeking into the device partition table:

```bash
sudo fdisk -l /dev/sda
```

An example output:

{:.jwoutput}
```
Disk /dev/sda: 477 GiB, 512110190592 bytes, 1000215216 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xc3ffc3ff

Device     Boot     Start        End   Sectors   Size Id Type
/dev/sda1  *           63  157276159 157276097    75G  7 HPFS/NTFS/exFAT
/dev/sda2       157278208  905842687 748564480   357G  f W95 Ext'd (LBA)
/dev/sda3       905842688 1000215215  94372528    45G  7 HPFS/NTFS/exFAT
/dev/sda5       157282304  168810495  11528192   5,5G 82 Linux swap / Solaris
/dev/sda6       168812544  579854335 411041792   196G  7 HPFS/NTFS/exFAT
/dev/sda7       579856384  618151935  38295552  18,3G 83 Linux
/dev/sda8       618153984  905840639 287686656 137,2G 83 Linux
```

#### lshw

This can be used to view partitions (a.k.a volumes here) in the following way:

```bash
sudo lshw -short -class volume
```

{:.jwoutput}
```
H/W path             Device     Class          Description
==========================================================
/0/100/1f.2/0.0.0/1  /dev/sda1  volume         1GiB EXT4 volume
/0/100/1f.2/0.0.0/2  /dev/sda2  volume         29GiB EFI partition
/0/100/1f.2/0.0.0/3  /dev/sda3  volume         19GiB EFI partition
/0/100/1f.2/0.0.0/4  /dev/sda4  volume         870GiB EFI partition
```

And with more verbosity:

```bash
sudo lshw -class volume
```

{:.jwoutput}
```
  *-volume:0                
       description: EXT4 volume
       vendor: Linux
       physical id: 1
       bus info: scsi@1:0.0.0,1
       logical name: /dev/sda1
       logical name: /boot
       version: 1.0
       size: 1GiB
       capabilities: journaled extended_attributes large_files huge_files dir_nlink recover 64bit extents ext4 ext2 initialized
       configuration: created=2020-12-05 02:59:11 filesystem=ext4 label=boot lastmountpoint=/boot modified=2021-10-16 01:09:09 mount.fstype=ext4 mount.options=rw,noatime mounted=2021-10-16 01:09:09 name=bootpart state=mounted
  *-volume:1
       description: EFI partition
       physical id: 2
       bus info: scsi@1:0.0.0,2
       logical name: /dev/sda2
       size: 29GiB
       capacity: 29GiB
       width: 1860298432 bits
       capabilities: encrypted luks initialized
       configuration: bits=1860298432 filesystem=luks hash=sha256 name=mx19 version=2
  (...)
```

#### hwinfo

This can be used to examine partitions in the following way:

```bash
hwinfo --short --partition
```

{:.jwoutput}
```
partition:                                                      
  /dev/sda1            Partition
  /dev/sda2            Partition
  /dev/sda3            Partition
  /dev/sda4            Partition
```

And with more verbosity:

```bash
hwinfo --partition
```

{:.jwoutput}
```
21: None 00.0: 11300 Partition                                  
  [Created at block.434]
  SysFS ID: /class/block/sda/sda1
  Hardware Class: partition
  Model: "Partition"
  Device File: /dev/sda1
  Device Files: /dev/sda1, /dev/disk/by-uuid/..., /dev/disk/by-partlabel/bootpart, /dev/disk/by-id/..., /dev/disk/by-path/..., /dev/disk/by-partuuid/..., /dev/disk/by-id/..., /dev/disk/by-label/boot
  Config Status: cfg=new, avail=yes, need=no, active=unknown
  Attached to: #20 (Disk)

22: None 00.0: 11300 Partition
  [Created at block.434]
  SysFS ID: /class/block/sda/sda2
  Hardware Class: partition
  Model: "Partition"
  Device File: /dev/sda2
  Device Files: /dev/sda2, /dev/disk/by-path/(...)
  Config Status: cfg=new, avail=yes, need=no, active=unknown
  Attached to: #20 (Disk)

23: None 00.0: 11300 Partition
  [Created at block.434]
  SysFS ID: /class/block/sda/sda3
  Hardware Class: partition
  Model: "Partition"
  Device File: /dev/sda3
  Device Files: /dev/sda3, /dev/disk/by-id/(...)
  Config Status: cfg=new, avail=yes, need=no, active=unknown
  Attached to: #20 (Disk)

24: None 00.0: 11300 Partition
  [Created at block.434]
  SysFS ID: /class/block/sda/sda4
  Hardware Class: partition
  Model: "Partition"
  Device File: /dev/sda4
  Device Files: /dev/sda4, /dev/disk/by-uuid/(...)
  Config Status: cfg=new, avail=yes, need=no, active=unknown
  Attached to: #20 (Disk)
```

#### /proc

Checking in the _proc_ pseudo-filesystem:

```bash
cat /proc/partitions
```

An example output:

{:.jwoutput}
```
major minor  #blocks  name

   7        0     100084 loop0
   7        1     100044 loop1
   7        2      18276 loop2
   7        3      69184 loop3
   7        4      69184 loop4
   8        0  500107608 sda
   8        1   78638048 sda1
   8        2          1 sda2
   8        3   47186264 sda3
   8        5    5764096 sda5
   8        6  205520896 sda6
   8        7   19147776 sda7
   8        8  143843328 sda8
```

#### (bonus) inxi

Apart from that, again, there is also _inxi_ with its vast and flexible system info reporting capabilities.

Let's learn some basic partition info:

```bash
inxi -P
```

{:.jwoutput}
```
Partition: ID-1: / size: 29.39 GiB used: 9.24 GiB (31.4%) fs: ext4 dev: /dev/dm-0 
           ID-2: /boot size: 975.9 MiB used: 430.6 MiB (44.1%) fs: ext4 dev: /dev/sda1 
           ID-3: /home size: 855.83 GiB used: 673.08 GiB (78.6%) fs: ext4 dev: /dev/dm-1 
           ID-4: swap-1 size: 19.98 GiB used: 207.7 MiB (1.0%) fs: swap dev: /dev/dm-2 
```

For full partition information (-P plus all other detected partitions):

```bash
inxi -p
```

{:.jwoutput}
```
Partition: ID-1: / size: 29.39 GiB used: 9.24 GiB (31.4%) fs: ext4 dev: /dev/dm-0 
           ID-2: /boot size: 975.9 MiB used: 430.6 MiB (44.1%) fs: ext4 dev: /dev/sda1 
           ID-3: /home size: 855.83 GiB used: 673.08 GiB (78.6%) fs: ext4 dev: /dev/dm-1 
           ID-4: swap-1 size: 19.98 GiB used: 207.7 MiB (1.0%) fs: swap dev: /dev/dm-2 
```

(well, here it added nothing, but it varies from system to system)

Let's add, if available, raw size of partition, percent available for user, block size of file system (root required). For swap, shows swapiness and vfs cache pressure, and if values are default or not:

```bash
inxi -pa
```

{:.jwoutput}
```
Partition: ID-1: / raw size: 29.98 GiB size: 29.39 GiB (98.01%) used: 9.24 GiB (31.4%) fs: ext4 dev: /dev/dm-0 
           ID-2: /boot raw size: 1024.0 MiB size: 975.9 MiB (95.30%) used: 430.6 MiB (44.1%) fs: ext4 dev: /dev/sda1 
           ID-3: /home raw size: 870.50 GiB size: 855.83 GiB (98.32%) used: 673.08 GiB (78.6%) fs: ext4 dev: /dev/dm-1 
           ID-4: swap-1 size: 19.98 GiB used: 207.7 MiB (1.0%) fs: swap swappiness: 15 (default 60) 
           cache pressure: 100 (default) dev: /dev/dm-2 
```

A variant for checking partition labels and UUIDs (triggers -P):

```bash
inxi -lu
```

{:.jwoutput}
```
Partition: ID-1: / size: 29.39 GiB used: 9.24 GiB (31.4%) fs: ext4 dev: /dev/dm-0 label: rootMX19 
           uuid: deb41ebe-24e2-4db0-96b0-2485778f7a1a 
           ID-2: /boot size: 975.9 MiB used: 430.6 MiB (44.1%) fs: ext4 dev: /dev/sda1 label: boot 
           uuid: d8bd8472-0cc5-4bf5-82db-1486b99a9b1d 
           ID-3: /home size: 855.83 GiB used: 673.08 GiB (78.6%) fs: ext4 dev: /dev/dm-1 label: homeMX 
           uuid: f34a45e3-d768-4fff-a6f1-3fbb209e0eee 
           ID-4: swap-1 size: 19.98 GiB used: 207.7 MiB (1.0%) fs: swap dev: /dev/dm-2 label: swapMX 
           uuid: b341c290-a431-443e-b310-8f0379bb752d 
```

Additionally, for unmounted partition info (includes UUID and Label if available):

```bash
inxi -o
```

{:.jwoutput}
```
Unmounted: ID-1: /dev/sda2 size: 30.00 GiB fs: crypto_luks label: N/A uuid: f928a180-f93c-44fc-af36-a3bcf5de5188 
           ID-2: /dev/sda3 size: 20.00 GiB fs: crypto_luks label: N/A uuid: eaa0084b-2948-49a7-a102-7c7f886d43bc 
           ID-3: /dev/sda4 size: 870.51 GiB fs: crypto_luks label: N/A uuid: ce7d8729-7716-4e58-89b9-2538635a31c2 
```
