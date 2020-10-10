---
layout: post
title:  "Expanding Live USB Linux persistent storage"
date:   2020-08-14 13:35:18 +0200
categories: linux
---

A recent exploration of the day was to see, if one can expand the persistent storage partition of a live USB without reinstalling the system onboard or basically touching anything in it.

I had a Ubuntu-based live USB key for some particular purposes, and I was starting to run out of space in its `casper-rw` partition. The problem was the partitions were already occupying the entire stick, so cloning the whole arrangement onto a larger one was necessary prior to expanding anything.

Hence, the plan was essentially to:
* create a bootable 1-to-1 copy on the new stick,
* expand `casper-rw` to cover all the space available,
all along the lines of [this](https://askubuntu.com/a/1179027) very nice instruction.

Below is the initial partition structure of the original stick: 

![image av1-1](/assets/img/expanding-live-usb-linux-persistent-storage/av1-1.png)

The selected partition, `msftdata`, created some problems with the expansion part of the plan, since it turned to be unmovable and I felt compelled to remove it.

Here is the remarks from _gparted_ on this guy:

![image av1-2](/assets/img/expanding-live-usb-linux-persistent-storage/av1-2.png)

**What does this partition do** and **is it safe to delete it?** - was the question of the day.

[Here](https://askubuntu.com/a/371605) comes some very nice and concise summary of what different types of partitions do. That gave some general idea, but I was still unsure about deletion, so I detailed the situation a bit at [askubuntu](https://askubuntu.com/q/1238266).

Turned out ___there were no worries___, so I deleted the thing and went on expanding the persistence.

Below is the result:

![image av2-1](/assets/img/expanding-live-usb-linux-persistent-storage/av2-1.png)

---
#

PS.

One of the reasons for expansion was my intention to run _dist-upgrade_ on the system. I was able to do it now, but the idea itself (upgrading on a live USB) is arguable. The up-to-date system is very slow now, and that might have to do with how `squashfs` works, as suggested [here](https://askubuntu.com/a/943631).

I might still need to consider reinstalling with a fresh system, I guess :)
