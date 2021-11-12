---
layout: post
title:  "Discovering hard disk's specs and details"
date:   2020-09-13 13:35:19 +0200
categories: linux hardware
---

Here is a cheat sheet, kind of, of commands related to discovering physical specs and details of hard disks installed on a machine.
Manufacturers, models, partitions layout and sizes, etc.

All the commands below I have performed on machines equipped with a single hard disk reporting itself as `/dev/sda`. Therefore this is what all the command examples that follow contain.


#### hdparm

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
	Firmware Revision:  FVVER
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
 Model=SSDPR-CX400-512, FwRev=FVVER, SerialNo=SERIALNO
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

#### lshw

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

#### hwinfo

Displaying all disks and storage controllers in the system (another way):

```bash
hwinfo --disk --storage
```

{:.jwoutput}
```
08: PCI 1f.2: 0106 SATA controller (AHCI 1.0)                   
  [Created at pci.386]
  SysFS ID: /devices/pci0000:00/0000:00:1f.2
  SysFS BusID: 0000:00:1f.2
  Hardware Class: storage
  Model: "Intel 8 Series/C220 Series Chipset Family 6-port SATA Controller 1 [AHCI mode]"
  Vendor: pci 0x8086 "Intel Corporation"
  Device: pci 0x8c02 "8 Series/C220 Series Chipset Family 6-port SATA Controller 1 [AHCI mode]"
  SubVendor: pci 0x17aa "Lenovo"
  SubDevice: pci 0x3097 
  Revision: 0x04
  Driver: "ahci"
  Driver Modules: "ahci"
  I/O Ports: 0xf0d0-0xf0d7 (rw)
  I/O Ports: 0xf0c0-0xf0c3 (rw)
  I/O Ports: 0xf0b0-0xf0b7 (rw)
  I/O Ports: 0xf0a0-0xf0a3 (rw)
  I/O Ports: 0xf060-0xf07f (rw)
  Memory Range: 0xf7d3a000-0xf7d3a7ff (rw,non-prefetchable)
  IRQ: 27 (9935737 events)
  Module Alias: "pci:v00008086d00008C02sv000017AAsd00003097bc01sc06i01"
  Driver Info #0:
    Driver Status: ahci is active
    Driver Activation Cmd: "modprobe ahci"
  Config Status: cfg=new, avail=yes, need=no, active=unknown

26: IDE 100.0: 10600 Disk
  [Created at block.245]
  SysFS ID: /class/block/sda
  SysFS BusID: 1:0:0:0
  SysFS Device Link: /devices/pci0000:00/0000:00:1f.2/ata2/host1/target1:0:0/1:0:0:0
  Hardware Class: disk
  Model: "CT1000MX500SSD1"
  Device: "CT1000MX500SSD1"
  Revision: "023"
  Driver: "ahci", "sd"
  Driver Modules: "ahci", "sd_mod"
  Device File: /dev/sda
  Device Files: /dev/sda, /dev/disk/by-path/pci-0000:00:1f.2-ata-2, /dev/disk/by-id/ata-CT1000MX500SSD1_1940E222815B, /dev/disk/by-id/wwn-0x500a0751e222815b
  Device Number: block 8:0-8:15
  BIOS id: 0x80
  Drive status: no medium
  Config Status: cfg=new, avail=yes, need=no, active=unknown
  Attached to: #8 (SATA controller)
```

Or just shortly:

```bash
hwinfo --short --disk --storage
```

{:.jwoutput}
```
storage:                                                        
                       Intel 8 Series/C220 Series Chipset Family 6-port SATA Controller 1 [AHCI mode]
disk:
  /dev/sda             CT1000MX500SSD1
```

#### smartctl

Using _Smartmontools_ to get disk info:

```bash
sudo smartctl -d ata -i /dev/sda
```

{:.jwoutput}
```
=== START OF INFORMATION SECTION ===
Device Model:     SSDPR-CX400-512
Serial Number:    SERIALNO
Firmware Version: FVVER
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

#### sdparm

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

#### lsscsi

Another one similar to the above:

```bash
lsscsi
```

{:.jwoutput}
```
[0:0:0:0]    disk    ATA      SSDPR-CX400-512  61  /dev/sda 
[4:0:0:0]    disk    TOSHIBA  MK5061GSYN       03  /dev/sdb 
```

#### /proc

Finally, from the _proc_ pseudo-filesystem on SCSI/SATA devices:

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

#### (bonus) inxi

Apart from that, there is also _inxi_ with its vast and flexible system info reporting capabilities.

The following prints nice Hard Disk info, including total storage and details for each disk. Disk total used percentage includes swap partition size(s). Additionally, if available, with logical and physical block sizes.

```bash
inxi -Dxxxa
```

{:.jwoutput}
```
Drives:    Local Storage: total: 931.51 GiB used: 682.96 GiB (73.3%) 
           ID-1: /dev/sda vendor: Crucial model: CT1000MX500SSD1 size: 931.51 GiB block size: physical: 4096 B logical: 512 B 
           speed: 6.0 Gb/s serial: SERIALNO rev: 023 temp: 23 C scheme: GPT 
```

Another switch prints drive data with floppy disks, if present.

```bash
inxi -d
```

{:.jwoutput}
```
Drives:    Local Storage: total: 931.51 GiB used: 682.96 GiB (73.3%) 
           ID-1: /dev/sda vendor: Crucial model: CT1000MX500SSD1 size: 931.51 GiB 
           Message: No Optical or Floppy data was found. 
```

I really like this one. More on its usage [here](https://www.tecmint.com/inxi-command-to-find-linux-system-information/).

Now you know almost all there is about your disk :)
