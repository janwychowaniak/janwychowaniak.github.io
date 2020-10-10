---
layout: post
title:  "debootstrap and schroot"
date:   2020-06-24 13:35:18 +0200
categories: linux security
---

After [this](https://logan.tw/posts/2018/02/24/manage-chroot-environments-with-schroot/), here is how to quickly set up a chroot environment with `schroot`.

Assumptions:

- _Ubuntu 16.04 Xenial Xerus_ would serve as an example inside chroot,
- parent (host system) architecture is amd64 and so will be our xenial.

{% highlight bash %}
$ sudo apt install debootstrap schroot
$ sudo debootstrap xenial /var/chroot/xenial http://archive.ubuntu.com/ubuntu
{% endhighlight %}

Contents of `/etc/schroot/chroot.d/xenial.conf`:

```
[xenial]
description=Ubuntu 16.04 Xenial Xerus
directory=/var/chroot/xenial
root-users=USERNAME
users=USERNAME
type=directory
```

How to use (should work without root):

{% highlight bash %}
$ schroot -l                  # list the chroot environments
$ schroot -c xenial           # enter a chroot environment
$ schroot -c xenial -u root   # enter a chroot environment as root
{% endhighlight %}

In case the parent is behind proxy, the "guest" would need to have the parent's proxy settings replicated. The relevant files:

- `/etc/environment`
- `/etc/apt/apt.conf.d/95proxies`

Also, the guest's **apt** has only the _main_ repository enabled by default. Adding more (e.g. _universe_) might be desired.

Once a chroot environment has been entered, certain filesystem resources get mounted, so that life is easier by e.g. having the parent system user home folder shared. To quickly list the mounted resources:

{% highlight bash %}
$ mount | grep chroot
$ mount | grep chroot | awk '{print $1 " " $2 " " $3}'
$ mount | grep chroot | grep "^\/dev" | awk '{print $1 " " $2 " " $3}'
{% endhighlight %}

That's the, kind of, basics.

---

#

**BONUS:**

To be able for the chroot environment to launch `X` apps, two things are needed:

- access to the `~/.Xauthority` file from host (after [this](https://forums.gentoo.org/viewtopic-t-814521.html) suggestion)
- the `DISPLAY` environment variable (after [this](https://www.binarytides.com/setup-chroot-ubuntu-debootstrap/) suggestion)

The `~/.Xauthority` file:

- if entered chroot as the regular user, the file is already there, since home is mounted
- if entered chroot as root, the file needs to be copied to chroot's root's home

Now, with setting the `DISPLAY` env var, an X app can be launched with the likes of:

{% highlight bash %}
$ export DISPLAY=":0.0" && firefox
# or
$ DISPLAY=":0.0" firefox
{% endhighlight %}

Have fun.
