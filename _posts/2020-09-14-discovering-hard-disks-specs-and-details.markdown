---
layout: post
title:  "Discovering hard disks specs and details"
date:   2020-09-14 13:35:18 +0200
categories: linux hardware
---

Here is a cheat sheet, kind of, of commands related to discovering specs and details of hard disks installed on a machine.
Manufacturers, models, partitions layout and sizes, etc.

All the commands below I have performed on machines equipped with a single hard disk reporting itself as `/dev/sda`. Therefore this is what all the command examples that follow contain.

### Partition layout 

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

### Hardware information 

Drive identification info:

```bash
sudo hdparm -I /dev/sda
```

An example output:

{:.jwoutput}
```
/dev/sda:

ATA device, with non-removable media
	Model Number:       SSDPR-CX400-512                         
	Serial Number:      SERIALNO           
	Firmware Revision:  SBFM61
	Transport:          Serial, ATA8-AST, SATA 1.0a, SATA II Extensions, SATA Rev 2.5, SATA Rev 2.6, SATA Rev 3.0
Standards:
	Supported: 11 10 9 8 7 6 5 
	Likely used: 11
Configuration:
	Logical		max	current
	cylinders	16383	16383
	heads		16	16
	sectors/track	63	63
	--
	CHS current addressable sectors:    16514064
	LBA    user addressable sectors:   268435455
	LBA48  user addressable sectors:  1000215216
	Logical  Sector size:                   512 bytes
	Physical Sector size:                   512 bytes
	Logical Sector-0 offset:                  0 bytes
	device size with M = 1024*1024:      488386 MBytes
	device size with M = 1000*1000:      512110 MBytes (512 GB)
	cache/buffer size  = unknown
	Form Factor: 2.5 inch
	Nominal Media Rotation Rate: Solid State Device

	(... - much more)
```

The `-I` switch above requests identification info directly from the drive, as opposed to `-i`, which displays the identification info which the kernel drivers (IDE, libata) have stored from boot/configuration time:

```bash
sudo hdparm -i /dev/sda
```

{:.jwoutput}
```
 Model=SSDPR-CX400-512, FwRev=SBFM61, SerialNo=SERIALNO
 Config={ Fixed }
 RawCHS=16383/16/63, TrkSize=0, SectSize=0, ECCbytes=0
 BuffType=unknown, BuffSize=unknown, MaxMultSect=16, MultSect=16
 CurCHS=16383/16/63, CurSects=16514064, LBA=yes, LBAsects=1000215216
 IORDY=on/off, tPIO={min:120,w/IORDY:120}, tDMA={min:120,rec:120}
 PIO modes:  pio0 pio3 pio4 
 DMA modes:  mdma0 mdma1 mdma2 
 UDMA modes: udma0 udma1 udma2 udma3 udma4 udma5 *udma6 
 AdvancedPM=no WriteCache=enabled
 Drive conforms to: Unspecified:  ATA/ATAPI-3,4,5,6,7
```

Displaying all disks and storage controllers in the system:

```bash
sudo lshw -class disk
sudo lshw -class storage
```

Example outputs:

{:.jwoutput}
```
  *-disk                    
       description: ATA Disk
       product: SSDPR-CX400-512
       physical id: 0.0.0
       bus info: scsi@0:0.0.0
       logical name: /dev/sda
       version: 61
       serial: SERIALNO
       size: 476GiB (512GB)
       capabilities: partitioned partitioned:dos
       configuration: ansiversion=5 logicalsectorsize=512 sectorsize=512 signature=c3ffc3ff
```

{:.jwoutput}
```
  *-storage                 
       description: SATA controller
       product: 82801IBM/IEM (ICH9M/ICH9M-E) 4 port SATA Controller [AHCI mode]
       vendor: Intel Corporation
       physical id: 1f.2
       bus info: pci@0000:00:1f.2
       version: 03
       width: 32 bits
       clock: 66MHz
       capabilities: storage msi pm ahci_1.0 bus_master cap_list
       configuration: driver=ahci latency=0
       resources: irq:28 ioport:d110(size=8) ioport:d100(size=4) (...) memory:d3d04000-d3d047ff
  *-scsi
       physical id: 1
       logical name: scsi0
       capabilities: emulated
```

Or identifying the disks just shortly:

```bash
sudo lshw -short -C disk
```

{:.jwoutput}
```
H/W path         Device     Class       Description
===================================================
/0/1/0.0.0       /dev/sda   disk        512GB SSDPR-CX400-512
```

Using _Smartmontools_ to get disk info:

```bash
sudo smartctl -d ata -i /dev/sda
```

{:.jwoutput}
```
=== START OF INFORMATION SECTION ===
Device Model:     SSDPR-CX400-512
Serial Number:    SERIALNO
Firmware Version: SBFM61
User Capacity:    512 110 190 592 bytes [512 GB]
Sector Size:      512 bytes logical/physical
Rotation Rate:    Solid State Device
Form Factor:      2.5 inches
Device is:        Not in smartctl database [for details use: -P showall]
ATA Version is:   Unknown(0x0ff8) (minor revision not indicated)
SATA Version is:  SATA 3.2, 6.0 Gb/s (current: 3.0 Gb/s)
SMART support is: Available - device has SMART capability.
SMART support is: Enabled
```

The above prints after specifying **-d** `ata` or `sat` or `auto`.
The below comes for **-d** `scsi` for curiosity/reference:

{:.jwoutput}
```
User Capacity:        512 110 190 592 bytes [512 GB]
Logical block size:   512 bytes
LU is fully provisioned
Rotation Rate:        Solid State Device
Form Factor:          2.5 inches
Serial number:        SERIALNO
Device type:          disk
SMART support is:     Unavailable - device lacks SMART capability.
```

There is also a means of fetching specifically _SCSI/SATA_ device information:

```bash
sudo sdparm /dev/sda
```

{:.jwoutput}
```
    /dev/sda: ATA       SSDPR-CX400-512   61
Read write error recovery mode page:
  AWRE        1  [cha: n, def:  1]
  ARRE        0  [cha: n, def:  0]
  PER         0  [cha: n, def:  0]
Caching (SBC) mode page:
  WCE         1  [cha: y, def:  1]
  RCD         0  [cha: n, def:  0]
Control mode page:
  SWP         0  [cha: n, def:  0]
```

or

```bash
sudo sdparm --inquiry /dev/sda
```

{:.jwoutput}
```
    /dev/sda: ATA       SSDPR-CX400-512   61
Device identification VPD page:
  Addressed logical unit:
    designator type: vendor specific [0x0],  code set: ASCII
      vendor specific: SERIALNO           
    designator type: T10 vendor identification,  code set: ASCII
      vendor id: ATA     
      vendor specific: SSDPR-CX400-512                         SERIALNO           
```

Another one similar to the above:

```bash
lsscsi
```

{:.jwoutput}
```
[0:0:0:0]    disk    ATA      SSDPR-CX400-512  61  /dev/sda 
[4:0:0:0]    disk    TOSHIBA  MK5061GSYN       03  /dev/sdb 
```

Finally, from the _proc_ pseudo-filesystem on SCSI/Sata devices:

```bash
cat /proc/scsi/scsi
```

{:.jwoutput}
```
Attached devices:
Host: scsi0 Channel: 00 Id: 00 Lun: 00
  Vendor: ATA      Model: SSDPR-CX400-512  Rev: 61
  Type:   Direct-Access                    ANSI  SCSI revision: 05
Host: scsi4 Channel: 00 Id: 00 Lun: 00
  Vendor: TOSHIBA  Model: MK5061GSYN       Rev: 03
  Type:   Direct-Access                    ANSI  SCSI revision: 06
```

More reference on all the above [here](https://www.cyberciti.biz/faq/find-hard-disk-hardware-specs-on-linux/) and [here](https://www.cyberciti.biz/tips/sdparm-linux-scsi-device-attribute.html).

---
#

Apart from that, there is also _inxi_ with its vast and flexible system info reporting capabilities.

For disks:

```bash
inxi -D
```

{:.jwoutput}
```
Drives:    HDD Total Size: 512.1GB (18.8% used)
           ID-1: /dev/sda model: SSDPR size: 512.1GB
```

or, more verbosely:

```bash
inxi -v 7
```

{:.jwoutput}
```
(...)
Drives:    HDD Total Size: 512.1GB (18.8% used)
           ID-1: /dev/sda model: SSDPR size: 512.1GB serial: SERIALNO temp: 33C
           Optical: No optical drives detected.
Partition: ID-1: / size: 18G used: 12G (67%) fs: ext4 dev: /dev/sda7
           label: N/A uuid: 319c9ac4-98fe-48d5-97b0-d51bacfa75f0
           ID-2: /home size: 135G used: 74G (58%) fs: ext4 dev: /dev/sda8
           label: N/A uuid: cd2c7389-dfee-40f1-840d-abb9d8dd20e4
           ID-3: swap-1 size: 5.90GB used: 0.40GB (7%) fs: swap dev: /dev/sda5
           label: N/A uuid: b8aa231c-bf9c-42e4-aa58-45bff4c3996d
RAID:      System: supported: N/A
           No RAID devices: /proc/mdstat, md_mod kernel module present
           Unused Devices: none
Unmounted: ID-1: /dev/sda1 size: 80.53G fs: NTFS label: N/A uuid: 5A5C09D95C09B135
           ID-2: /dev/sda3 size: 48.32G fs: NTFS label: N/A uuid: 77E2AB297C2BD23F
           ID-3: /dev/sda6 size: 210.45G fs: NTFS label: N/A uuid: 0C572A625B81C0D6
(...)
```

I really like this one. More on its usage [here](https://www.tecmint.com/inxi-command-to-find-linux-system-information/).

Now you know almost all there is about your disk :)