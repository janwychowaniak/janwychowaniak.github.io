---
layout: post
title:  "Linux system memory details"
date:   2021-11-12 13:35:19 +0200
categories: linux hardware
---

Another hardware specs cheat sheet for Linux. This time for memory.

#### lshw

`lshw` must be run as super user or it will only report partial information.

```bash
sudo lshw -short -class memory
```

{:.jwoutput}
```
H/W path             Device     Class          Description
==========================================================
/0/0                            memory         64KiB BIOS
/0/3d/3e                        memory         1MiB L2 cache
/0/3d/3f                        memory         256KiB L1 cache
/0/3d/40                        memory         8MiB L3 cache
/0/41                           memory         16GiB System Memory
/0/41/0                         memory         DIMM [empty]
/0/41/1                         memory         8GiB DIMM DDR3 Synchronous 1600 MHz (0.6 ns)
/0/41/2                         memory         DIMM [empty]
/0/41/3                         memory         8GiB DIMM DDR3 Synchronous 1600 MHz (0.6 ns)
```

The info includes cache for some reason. Good, why not.
More verbosely:

```bash
sudo lshw -class memory
```

{:.jwoutput}
```
  *-firmware                
       description: BIOS
       vendor: LENOVO
       physical id: 0
       date: 05/19/2016
       size: 64KiB
       capacity: 6656KiB
       capabilities: pci upgrade shadowing cdboot bootselect socketedrom edd int13floppy1200
                     int13floppy720 int13floppy2880 int5printscreen int9keyboard int14serial
                     int17printer acpi usb biosbootspecification uefi
  *-cache:0
       description: L2 cache
       physical id: 3e
       slot: CPU Internal L2
       size: 1MiB
       capacity: 1MiB
       capabilities: internal write-back unified
       configuration: level=2
  *-cache:1
       description: L1 cache
       physical id: 3f
       slot: CPU Internal L1
       size: 256KiB
       capacity: 256KiB
       capabilities: internal write-back
       configuration: level=1
  *-cache:2
       description: L3 cache
       physical id: 40
       slot: CPU Internal L3
       size: 8MiB
       capacity: 8MiB
       capabilities: internal write-back unified
       configuration: level=3
  *-memory
       description: System Memory
       physical id: 41
       slot: System board or motherboard
       size: 16GiB
     *-bank:0
          description: DIMM [empty]
          vendor: [Empty]
          physical id: 0
          slot: ChannelA-DIMM0
     *-bank:1
          description: DIMM DDR3 Synchronous 1600 MHz (0.6 ns)
          vendor: AMD
          physical id: 1
          slot: ChannelA-DIMM1
          size: 8GiB
          width: 64 bits
          clock: 1600MHz (0.6ns)
     *-bank:2
          description: DIMM [empty]
          vendor: [Empty]
          physical id: 2
          slot: ChannelB-DIMM0
     *-bank:3
          description: DIMM DDR3 Synchronous 1600 MHz (0.6 ns)
          vendor: AMD
          physical id: 3
          slot: ChannelB-DIMM1
          size: 8GiB
          width: 64 bits
          clock: 1600MHz (0.6ns)
```

#### hwinfo

This one is not the world verbosity champion for memory, but for the sake of completeness:

```bash
hwinfo --memory
```

{:.jwoutput}
```
01: None 00.0: 10102 Main Memory                                
  [Created at memory.74]
  Hardware Class: memory
  Model: "Main Memory"
  Memory Range: 0x00000000-0x3e3bebfff (rw)
  Memory Size: 16 GB
  Config Status: cfg=new, avail=yes, need=no, active=unknown
```

#### inxi

`inxi` offers some basic memory info. Requires root for this.

```bash
sudo inxi -m
```

{:.jwoutput}
```
Memory:    RAM: total: 15.56 GiB used: 10.01 GiB (64.3%) 
           Array-1: capacity: 32 GiB slots: 4 EC: None 
           Device-1: ChannelA-DIMM0 size: No Module Installed 
           Device-2: ChannelA-DIMM1 size: 8 GiB speed: 1600 MT/s 
           Device-3: ChannelB-DIMM0 size: No Module Installed 
           Device-4: ChannelB-DIMM1 size: 8 GiB speed: 1600 MT/s 
```

The same, but excluding empty module slots:

```bash
sudo inxi --memory-modules
```

{:.jwoutput}
```
Memory:    RAM: total: 15.56 GiB used: 10.00 GiB (64.3%) 
           Array-1: capacity: 32 GiB slots: 4 EC: None 
           Device-1: ChannelA-DIMM1 size: 8 GiB speed: 1600 MT/s 
           Device-2: ChannelB-DIMM1 size: 8 GiB speed: 1600 MT/s 
```

More verbosely, with additional info, if available:

```bash
sudo inxi --memory-modules -xxx
```

{:.jwoutput}
```
Memory:    RAM: total: 15.56 GiB used: 9.85 GiB (63.3%) 
           Array-1: capacity: 32 GiB slots: 4 EC: None max module size: 8 GiB note: est. 
           Device-1: ChannelA-DIMM1 size: 8 GiB speed: 1600 MT/s type: DDR3 detail: synchronous bus width: 64 bits 
           total: 64 bits manufacturer: 0112 part-no: <filter> serial: <filter> 
           Device-2: ChannelB-DIMM1 size: 8 GiB speed: 1600 MT/s type: DDR3 detail: synchronous bus width: 64 bits 
           total: 64 bits manufacturer: 0112 part-no: <filter> serial: <filter> 
```

#### dmidecode

Now, this one is quite verbose.

Note (from _man_):

> dmidecode is a tool for dumping a computer's DMI (some say SMBIOS) table contents in a human-readable format. This table contains a description of the system's hardware components, as well as other useful pieces of information such as serial numbers and BIOS revision. Thanks to this table, you can retrieve this information without having to probe for the actual hardware.

but

> While this is a good point in terms of report speed and safeness, this also makes the presented information possibly unreliable.

Anyway:

```bash
sudo dmidecode -t memory
```

{:.jwoutput}
```
# dmidecode 3.2
Getting SMBIOS data from sysfs.
SMBIOS 2.8 present.

Handle 0x0041, DMI type 16, 23 bytes
Physical Memory Array
	Location: System Board Or Motherboard
	Use: System Memory
	Error Correction Type: None
	Maximum Capacity: 32 GB
	Error Information Handle: Not Provided
	Number Of Devices: 4

Handle 0x0042, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0041
	Error Information Handle: Not Provided
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: DIMM
	Set: None
	Locator: ChannelA-DIMM0
	Bank Locator: BANK 0
	Type: Unknown
	Type Detail: None
	Speed: Unknown
	Manufacturer: [Empty]
	Rank: Unknown
	Configured Memory Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0044, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0041
	Error Information Handle: Not Provided
	Total Width: 64 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: ChannelA-DIMM1
	Bank Locator: BANK 1
	Type: DDR3
	Type Detail: Synchronous
	Speed: 1600 MT/s
	Manufacturer: 0112
	Rank: 2
	Configured Memory Speed: 1600 MT/s
	Minimum Voltage: 1.5 V
	Maximum Voltage: 1.5 V
	Configured Voltage: 1.5 V

Handle 0x0046, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0041
	Error Information Handle: Not Provided
	Total Width: Unknown
	Data Width: Unknown
	Size: No Module Installed
	Form Factor: DIMM
	Set: None
	Locator: ChannelB-DIMM0
	Bank Locator: BANK 2
	Type: Unknown
	Type Detail: None
	Speed: Unknown
	Manufacturer: [Empty]
	Rank: Unknown
	Configured Memory Speed: Unknown
	Minimum Voltage: Unknown
	Maximum Voltage: Unknown
	Configured Voltage: Unknown

Handle 0x0047, DMI type 17, 40 bytes
Memory Device
	Array Handle: 0x0041
	Error Information Handle: Not Provided
	Total Width: 64 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: ChannelB-DIMM1
	Bank Locator: BANK 3
	Type: DDR3
	Type Detail: Synchronous
	Speed: 1600 MT/s
	Manufacturer: 0112
	Rank: 2
	Configured Memory Speed: 1600 MT/s
	Minimum Voltage: 1.5 V
	Maximum Voltage: 1.5 V
	Configured Voltage: 1.5 V
```

---
#

More memory needed? How to find a module that would match correctly?

Apart from some obvious characteristics, like the desired capacity or correct form factor, some more details should be taken into consideration, with at least the following matching also:

* `type` - whether _DDR2_, _DDR3_, _DDR4_ etc; with detail, like _synchronous_
* `clock` - or `rate` or `frequency` (in MHz); might also be possibly indicated as `speed` [MT/s]
* `latency` - or `CAS Latency` or `CL`
* `voltage` - minimum, maximum, configured if known

Some of these details are immediately known from the output of the tools above, some need to be searched for with the part number.
