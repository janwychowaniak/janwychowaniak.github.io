---
layout: post
title:  "Checking TRIM status on Windows and Linux"
date:   2020-09-15 13:35:18 +0200
categories: windows linux hardware
---

[This resource](https://blog.100tb.com/how-to-keep-your-ssds-fast-with-trim-on-linux) introduces nicely the concept of `TRIM` in the context of SSD disks.

> TRIM is a command built into the ATA command set for SSDs that is part of how the disk interfaces with the computer. The operating system is able to send TRIM commands to the disk to let it know which blocks are part of deleted files, and allow the SSD to erase the blocks in advance of needing to write to them. While the operating system is capable of signaling the drive to erase these sections every time they delete a file on the file system, this can also have an impact on performance and slow things down. So the recommendation is to run TRIM on a schedule to clear the blocks intermittently.

It is considered the most important optimization of an SSD operation. It should be automatically handled by most modern versions of _Windows_ and _Linux_.

But let's verify it really is.

### In Windows

Command prompt (as admin):

```
fsutil behavior query disabledeletenotify
```

Possible outputs:

```bash
NTFS DisableDeleteNotify = 0  # meaning: TRIM is enabled :)
NTFS DisableDeleteNotify = 1  # meaning: TRIM is disabled :(
```
There also exists a GUI tool for interacting with SSD disks, called `SSD-Z`.
It allows to check various disk parameters, including TRIM:

![image ssd-z](/assets/img/checking-trim-status-on-windows-and-linux/ssd-z.png)

### In Linux

In modern Linux systems a TRIM job should be run every week.

Verifying this on platforms employing the _systemd_ system and service manager can be accomplished with `systemctl`.

Let's see the timers:

```bash
systemctl list-timers
```

```
NEXT                          LEFT          LAST                          PASSED     UNIT                         ACTIVATES
Sat 2020-10-10 19:00:09 CEST  24s left      Sat 2020-10-10 18:04:50 CEST  54min ago    anacron.timer                anacron.service
Sat 2020-10-10 23:10:26 CEST  4h 10min left Sat 2020-10-10 07:14:47 CEST  11h ago      apt-daily.timer              apt-daily.service
Sun 2020-10-11 05:32:45 CEST  10h left      Sat 2020-10-10 16:17:09 CEST  2h 42min ago motd-news.timer              motd-news.service
Sun 2020-10-11 06:03:35 CEST  11h left      Sat 2020-10-10 06:37:45 CEST  12h ago      apt-daily-upgrade.timer      apt-daily-upgrade.service
Sun 2020-10-11 16:14:39 CEST  21h left      Sat 2020-10-10 16:14:39 CEST  2h 45min ago systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service
Mon 2020-10-12 00:00:00 CEST  1 day 5h left Mon 2020-10-05 00:19:34 CEST  5 days ago   fstrim.timer                 fstrim.service
n/a                           n/a           Sat 2020-10-10 16:00:31 CEST  2h 59min ago ureadahead-stop.timer        ureadahead-stop.service
7 timers listed.
```

We see `fstrim.timer`. Let's have a closer look:

```bash
systemctl status fstrim.timer
```

```
● fstrim.timer - Discard unused blocks once a week
   Loaded: loaded (/lib/systemd/system/fstrim.timer; enabled; vendor preset: enabled)
   Active: active (waiting) since Fri 2020-10-09 22:01:16 CEST; 16h ago
  Trigger: Mon 2020-10-12 00:00:00 CEST; 1 day 8h left
     Docs: man:fstrim
```

So, we see it is indeed active and it fires every week. Good.

[More](https://dannyda.com/2019/12/16/ubuntu-linux-check-ssd-trim-status/).
