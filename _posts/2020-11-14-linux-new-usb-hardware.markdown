---
layout: post
title:  "Watching Linux greet new USB hardware"
date:   2020-11-14 13:35:18 +0200
categories: linux hardware
---

If one wishes to see a list of the USB hardware visible to the system, `lsusb` might be the way.

In its basic form:

```bash
lsusb
```

gives something like:

{:.jwoutput}
```
Bus 002 Device 003: ID 04f2:b105 Chicony Electronics Co., Ltd 
Bus 002 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 008 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 007 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 006 Device 002: ID 062a:4101 Creative Labs Wireless Keyboard/Mouse
Bus 006 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 005 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 004 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
Bus 003 Device 001: ID 1d6b:0001 Linux Foundation 1.1 root hub
```

Details of a particular device can be further inspected as follows, with the Wireless Keyboard/Mouse (_Bus 006 Device 002_) serving as an example:

```bash
lsusb -s 2 -v | less  # device(s) specified
lsusb -s 6: -v | less  # bus specified
lsusb -s 6:2 -v | less  # bus:device specified
```

The output is long and quite unpleasant, but in case of wanting to determine the kind and nature of a particular device, **bDevice*** items in the _Device Descriptor_ section and the entire **Interface Descriptor** subsection should be of tremendous help.

One can also dump the physical USB device hierarchy as a tree:

```bash
lsusb -t
```

which prints, let's say:

{:.jwoutput}
```
/:  Bus 08.Port 1: Dev 1, Class=root_hub, Driver=uhci_hcd/2p, 12M
/:  Bus 07.Port 1: Dev 1, Class=root_hub, Driver=uhci_hcd/2p, 12M
/:  Bus 06.Port 1: Dev 1, Class=root_hub, Driver=uhci_hcd/2p, 12M
    |__ Port 2: Dev 4, If 0, Class=Human Interface Device, Driver=usbhid, 12M
    |__ Port 2: Dev 4, If 1, Class=Human Interface Device, Driver=usbhid, 12M
/:  Bus 05.Port 1: Dev 1, Class=root_hub, Driver=uhci_hcd/2p, 12M
/:  Bus 04.Port 1: Dev 1, Class=root_hub, Driver=uhci_hcd/2p, 12M
/:  Bus 03.Port 1: Dev 1, Class=root_hub, Driver=uhci_hcd/2p, 12M
/:  Bus 02.Port 1: Dev 1, Class=root_hub, Driver=ehci-pci/6p, 480M
    |__ Port 5: Dev 3, If 0, Class=Video, Driver=uvcvideo, 480M
    |__ Port 5: Dev 3, If 1, Class=Video, Driver=uvcvideo, 480M
/:  Bus 01.Port 1: Dev 1, Class=root_hub, Driver=ehci-pci/6p, 480M
```

The **Class=** bits prompt on what a given piece might be.

[This](https://unix.stackexchange.com/a/207833) link offers some more insightful reading on `lsusb`.

Another useful means for reaching a similar goal is `hwinfo`.

```bash
hwinfo --short --usb
```

{:.jwoutput}
```
keyboard:                                                       
  /dev/input/event3    A4Tech USB Keyboard
mouse:
  /dev/input/mice      Logitech RX 250 Optical Mouse
disk:
  /dev/sdb             Kingston DataTraveler 3.0
hub:
                       Linux Foundation 2.0 root hub
                       Intel Hub
                       Linux Foundation 3.0 root hub
                       Linux Foundation 2.0 root hub
                       Intel Hub
                       Linux Foundation 2.0 root hub
unknown:
  /dev/input/event5    A4Tech USB Keyboard
```

Further, more detailed examination of a particular item from the output above may be accomplished e.g. with:

```bash
hwinfo --disk --only /dev/sdb
```

---
#

What I sometimes like to do is to see the system's live response exactly after plugging something in.

One happy method for that is to open up three terminals next to one another and to issue the following commands:

<table>
	<tr>
		<th> Terminal 1 </th>
		<th> Terminal 2 </th>
		<th> Terminal 3 </th>
	</tr>
	<tr>
		<td>
			<code>watch lsusb</code>
		</td>
		<td>
			<code>watch hwinfo --short --usb</code>
		</td>
		<td>
			<code>dmesg -wxH</code>
		</td>
	</tr>
</table>

and then to pay attention to what happens after plugging something in.

An example `dmesg` output produced after plugging the mentioned Wireless Keyboard/Mouse may resemble the following:

{:.jwoutput}
```
kern  :info  : [lis14 22:14] usb 6-2: new full-speed USB device number 4 using uhci_hcd
kern  :info  : [  +0,199069] usb 6-2: New USB device found, idVendor=062a, idProduct=4101, bcdDevice= 1.08
kern  :info  : [  +0,000008] usb 6-2: New USB device strings: Mfr=1, Product=2, SerialNumber=0
kern  :info  : [  +0,000005] usb 6-2: Product: 2.4G Keyboard Mouse
kern  :info  : [  +0,000005] usb 6-2: Manufacturer: MOSART Semi.
kern  :info  : [  +0,007709] input: MOSART Semi. 2.4G Keyboard Mouse as /devices/pci0000:00/0000:00:1d.0/usb6/6-2/6-2:1.0/0003:062A:4101.0005/input/input29
kern  :info  : [  +0,057811] hid-generic 0003:062A:4101.0005: input,hidraw0: USB HID v1.10 Keyboard [MOSART Semi. 2.4G Keyboard Mouse] on usb-0000:00:1d.0-2/input0
kern  :info  : [  +0,006028] input: MOSART Semi. 2.4G Keyboard Mouse as /devices/pci0000:00/0000:00:1d.0/usb6/6-2/6-2:1.1/0003:062A:4101.0006/input/input30
kern  :info  : [  +0,057761] input: MOSART Semi. 2.4G Keyboard Mouse Consumer Control as /devices/pci0000:00/0000:00:1d.0/usb6/6-2/6-2:1.1/0003:062A:4101.0006/input/input31
kern  :info  : [  +0,000218] input: MOSART Semi. 2.4G Keyboard Mouse System Control as /devices/pci0000:00/0000:00:1d.0/usb6/6-2/6-2:1.1/0003:062A:4101.0006/input/input32
kern  :info  : [  +0,000203] input: MOSART Semi. 2.4G Keyboard Mouse as /devices/pci0000:00/0000:00:1d.0/usb6/6-2/6-2:1.1/0003:062A:4101.0006/input/input33
kern  :info  : [  +0,000346] hid-generic 0003:062A:4101.0006: input,hiddev0,hidraw1: USB HID v1.10 Mouse [MOSART Semi. 2.4G Keyboard Mouse] on usb-0000:00:1d.0-2/input1
```

giving quite a bit of insight.

More on reading `dmesg` output in my [other post]({% post_url 2020-10-15-dmesg-how-to-read-it %}).

---
#

An additional way of examining the USB situation is, as with many other, with `inxi`.

A bird's eye look:

```bash
inxi --usb
```

{:.jwoutput}
```
USB:       Hub: 1-0:1 info: Full speed (or root) Hub ports: 3 rev: 2.0 
           Hub: 1-1:2 info: Intel ports: 6 rev: 2.0 
           Hub: 2-0:1 info: Full speed (or root) Hub ports: 15 rev: 2.0 
           Device-1: 2-3:15 info: A4Tech type: Keyboard,HID rev: 2.0 
           Device-2: 2-9:3 info: Logitech RX 250 Optical Mouse type: Mouse rev: 2.0 
           Hub: 3-0:1 info: Full speed (or root) Hub ports: 3 rev: 2.0 
           Hub: 3-1:2 info: Intel ports: 8 rev: 2.0 
           Hub: 4-0:1 info: Full speed (or root) Hub ports: 6 rev: 3.0 
           Device-3: 4-6:2 info: Kingston DataTraveler 100 G3/G4/SE9 G2 type: Mass Storage rev: 3.1 
```

A slightly more detailed one:

```bash
inxi --usb -xxx
```

{:.jwoutput}
```
USB:       Hub: 1-0:1 info: Full speed (or root) Hub ports: 3 rev: 2.0 speed: 480 Mb/s chip ID: 1d6b:0002 
           Hub: 1-1:2 info: Intel ports: 6 rev: 2.0 speed: 480 Mb/s chip ID: 8087:8008 
           Hub: 2-0:1 info: Full speed (or root) Hub ports: 15 rev: 2.0 speed: 480 Mb/s chip ID: 1d6b:0002 
           Device-1: 2-3:15 info: A4Tech type: Keyboard,HID driver: hid-generic,usbhid interfaces: 2 rev: 2.0 speed: 1.5 Mb/s 
           chip ID: 09da:2268 
           Device-2: 2-9:3 info: Logitech RX 250 Optical Mouse type: Mouse driver: hid-generic,usbhid interfaces: 1 rev: 2.0 
           speed: 1.5 Mb/s chip ID: 046d:c050 
           Hub: 3-0:1 info: Full speed (or root) Hub ports: 3 rev: 2.0 speed: 480 Mb/s chip ID: 1d6b:0002 
           Hub: 3-1:2 info: Intel ports: 8 rev: 2.0 speed: 480 Mb/s chip ID: 8087:8000 
           Hub: 4-0:1 info: Full speed (or root) Hub ports: 6 rev: 3.0 speed: 5 Gb/s chip ID: 1d6b:0003 
           Device-3: 4-6:2 info: Kingston DataTraveler 100 G3/G4/SE9 G2 type: Mass Storage driver: usb-storage interfaces: 1 
           rev: 3.1 speed: 5 Gb/s chip ID: 0951:1666 serial: <filter> 
```
