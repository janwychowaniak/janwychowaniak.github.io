---
layout: post
title:  "Disk health and S.M.A.R.T. info lookup"
date:   2020-12-01 13:35:18 +0200
categories: linux windows hardware
---

### Lookup: Linux commandline

Getting general disk info and checking whether _S.M.A.R.T._ is enabled:

```bash
sudo smartctl -i /dev/sda
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

_S.M.A.R.T._ support available, but disabled?

```bash
sudo smartctl -s on /dev/sda
```

Overall health:

```bash
sudo smartctl -H /dev/sda
```

{:.jwoutput}
```
=== START OF READ SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED
```

For the complete list of _S.M.A.R.T._ attributes:

```bash
sudo smartctl -a /dev/sda
```

The output is pretty lengthy, informative though.

Some particular attributes to pay attention to:

- `Reallocated Sectors Count`
- `Spin Retry Count`
- `Reallocation Event Count`
- `Current Pending Sector Count`
- `Offline_Uncorrectable`

_Sidenote_: Depending on a particular disk type, output from the above commands may be misleading or incomplete. In case of such suspicion, it may be worth playing with different type parameters. Try adding one of the following switches:

- `-d auto` 
- `-d ata`
- `-d sat`
- `-d scsi`

End _Sidenote_.

There is also the `gnome-disks` app giving visual insight:

![image gnomedisks](/assets/img/disk-health-and-smart-info-lookup/gnomeDisks.png)

### Lookup: Windows

There is a couple of programs out there allowing to quickly assess disk health and to see the parameters of interest. My favourites follow.

[CrystalDiskInfo](https://portableapps.com/apps/utilities/crystaldiskinfo_portable)

![image crystaldiskinfo](/assets/img/disk-health-and-smart-info-lookup/CrystalDisk.png)

[HWiNFO](https://portableapps.com/apps/utilities/hwinfo-portable)

![image hwinfo](/assets/img/disk-health-and-smart-info-lookup/HwInfo.png)

[SSD-Z](https://portableapps.com/apps/utilities/ssd-z-portable)

![image ssd-z](/assets/img/disk-health-and-smart-info-lookup/ssdz-smart.png)

---
#

### Tests: Linux commandline

Info on estimated duration of tests:

```bash
sudo smartctl -c /dev/sda
```

{:.jwoutput}
```
(...)
Short self-test routine 
recommended polling time: 	 (   2) minutes.
Extended self-test routine
recommended polling time: 	 (  30) minutes.
Conveyance self-test routine
recommended polling time: 	 (   6) minutes.
(...)
```

Available test types (_Background Mode_ by default):

- **Short** (for **ATA**/**SCSI**)
- **Long** (for **ATA**/**SCSI**)
- **Conveyance** (**ATA** only)
- **Select** (**ATA** only)

Starting tests:

```bash
sudo smartctl -t short /dev/sda
sudo smartctl -t long /dev/sda
sudo smartctl -t conveyance /dev/sda
```

Checking the results:

```bash
sudo smartctl -l selftest /dev/sda
```

One thing to remember when testing external drives that are otherwise idle: they tend to go to sleep after some idleness period and that aborts the test execution.
Something needs to keep them awake. An example command for that to run during the test:

```bash
while true ; do touch dontsleep ; echo -n '.' ; sleep 60 ; done
```

Some reading: [here](https://www.thomas-krenn.com/en/wiki/Smartctl_Tool) and [here](https://www.thomas-krenn.com/en/wiki/SMART_tests_with_smartctl).
