---
layout: post
title:  "dmesg - how to read it efficiently"
date:   2020-10-15 13:35:18 +0200
categories: linux hardware
---

`dmesg` prints or controls the Linux kernel ring buffer, allowing e.g. reviewing and monitoring hardware device and driver messages and more.

The default output format that the tool offers I consider to be of limited friendliness.
Let's quickly summarise on the most useful or common options for output format control.

---

* Human Timestamps

```bash
dmesg -H
```

Drops to `less`.

* Watching Live Events

```bash
dmesg -w
dmesg --follow
```

New output is systematically added to the printout as it arrives.

---

The two options above I consider the **most useful** personally.
Some of the other helpful bits:

* Human Readable Timestamps

```bash
dmesg -T
```

(These are two slightly different things here: _Human_ vs _Human Readable_)

* Searching For Specific Terms

```bash
dmesg | grep -i usb
```

Simple `grep`, essentially.

* Using Log Levels

```bash
dmesg -l info
dmesg --level info
dmesg -l debug,info
```

Available loglevels:
_emerg, alert, crit, err, warn, notice, info, debug_

* The Facility Categories

```bash
dmesg -f daemon
dmesg --facility daemon
dmesg -f syslog,daemon
```

Available facilities: 
_kern, user, mail, daemon, auth, syslog, lpr, news_

* Showing _facility_ and _level_ as human-readable prefixes to each line

```bash
dmesg -x
```

Additional reading: [here](https://www.howtogeek.com/449335/how-to-use-the-dmesg-command-on-linux/) and [here](https://fossbytes.com/dmesg-command-reading-kernel-ring-buffer-log/).
