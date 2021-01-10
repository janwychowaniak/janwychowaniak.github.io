---
layout: post
title:  "showkey in Linux"
date:   2021-01-10 01:00:18 +0200
categories: linux hardware
---

`showkey` helps with keyboard examination/debugging. It prints to standard output the scan codes/keycode/ASCII code of each key pressed.

Summary of the valid options:

```
-s --scancodes  raw scan-codes
-k --keycodes   interpreted keycodes (default)
-a --ascii      decimal/octal/hex values of the keys
```

More detailed program description [here](https://linux.die.net/man/1/showkey).

Some notes on the options:

**-s**
- The program runs until 10 seconds have elapsed since the last key event.
- Issues _X warning_.

**-k**
- The program runs until 10 seconds have elapsed since the last key event.
- Issues _X warning_.

**-a**
- The program terminates when the user types `^D`. 

A note on the _X warning_ thing. For the **-s** and **-k** modes the following warning is issued by the program:

>if you are trying this under X, it might not work since the X server is also reading /dev/console

Starting the operating system in text mode might be a solution.
The system ___runlevel 3___ is suitable for this purpose. [More](https://www.geeksforgeeks.org/run-levels-linux/) on runlevels.

For **one-time** text-based start with modern Ubuntu-based OS, the following line in the _GRUB menu_ is of interest:

![image grubboot1](/assets/img/showkey-in-linux/grub-boot-1.jpg)

An information needs to be passed, that we want runlevel `3`.

![image grubboot2](/assets/img/showkey-in-linux/grub-boot-2.jpg)

If we want to spectate the system startup, we can also get rid of `quiet` and `splash`.