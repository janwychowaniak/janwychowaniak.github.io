---
layout: post
title:  "Reclaiming disk space on Linux development system"
date:   2020-12-17 01:00:18 +0200
categories: linux docker
---

By _development system_ I mean one with no _X_ (GUI) or where we don't care about GUI-related stuff. Just the rest, plus _docker_. Possibly not the best term anyway, but it's already late in the evening.

Anyway, some tricks for getting back some disk space follow.

Let's check the general situation:

```bash
df -hT | grep ext4  # or whatever filesystem you use
```

{:.jwoutput}
```
/dev/mapper/rootfs ext4       30G  7.2G   21G  26% /
/dev/sda1          ext4      976M  159M  750M  18% /boot
/dev/mapper/homefs ext4      856G  380G  434G  47% /home
```

Cleaning `apt`:

```bash
sudo apt autoremove
sudo apt autoclean
sudo apt clean
```

Cleaning journals:

```bash
journalctl --disk-usage  # inspection
sudo journalctl --vacuum-time=15d  # action: remove older than 15 days
```

Cleaning snaps:

```bash
du -h /var/lib/snapd/snaps  # inspection
```

and then [this](https://itsfoss.com/free-up-space-ubuntu-linux/) resource sheds some light on actual further steps (par. "_5. Remove older versions of Snap applications_").

Cleaning user Python `pip` cache:

```bash
cd ~/.cache/pip && rm -r *
```

In terms of looking for deadweight across the filesystem, some tricks for displaying directory sizes:

```bash
du -m --max-depth=1 | sort -nr
ncdu
ncdu -x /  # -x = Do not cross filesystem boundaries
```

---
#

_Docker_ can also be greedy of we use it a lot.

Some inspection of the situation:

```bash
docker system df
```

{:.jwoutput}
```
TYPE                TOTAL               ACTIVE              SIZE                RECLAIMABLE
Images              129                 7                   27.67GB             26.1GB (94%)
Containers          20                  1                   52.32MB             51.24MB (97%)
Local Volumes       19                  0                   373.9MB             373.9MB (100%)
Build Cache         0                   0                   0B                  0B
```

Some more:

```bash
docker image ls -f dangling=true  # list dangling
docker volume ls -f dangling=true  # list dangling
```

Some of many [cleanup tips](https://medium.com/better-programming/docker-tips-clean-up-your-local-machine-35f370a01a78):

```bash
docker image prune  # dangling images
docker container prune  # stopped containers
docker volume prune  # local volumes not used by at least one container
docker builder prune  # dangling build cache
```

```bash
docker system prune  # all above plus networks (but minus volumes)
```

Switch `--all` to the below removes **all unused** images, not just dangling ones:

```bash
docker image prune --all
docker builder prune --all
docker system prune --all
```

[This](https://liejuntao001.medium.com/a-quick-note-to-clean-up-docker-overlay2-garbage-170225d38e69) resource (esp. its _Step 4_) is helpful, if more advanced purge is needed.
