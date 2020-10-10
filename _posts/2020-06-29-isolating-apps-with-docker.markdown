---
layout: post
title:  "Isolating apps with docker"
date:   2020-06-29 13:35:18 +0200
categories: security docker
---

Another way to obtain an isolated environment for testing and ringfencing apps is a `docker` container hosting an operating system.
Inside there can be done whatever, that one wants, without the fear of breaking the system, as the container will eventually be trashed anyway.

Below follows a simple recipe for creating such guy (_Ubuntu_-based in this case).

{% highlight bash %}
# ------------------------------
IMAGE="ubuntu:18.04"
CONTAINER="bionic-disposable0"
# ------------------------------

docker pull $IMAGE
# regular "run"...
docker run -d --name $CONTAINER $IMAGE tail -f /dev/null
# ...OR if the container is intended to host an app visible from the
# outside and thus needs to publish a port, "run" has a variant:
PUBLISH_PORT=9000
docker run -d --publish $PUBLISH_PORT:$PUBLISH_PORT --name $CONTAINER $IMAGE tail -f /dev/null
{% endhighlight %}

{% highlight bash %}
# (optionally)
# if the parent system is behind http proxy and it also happens to be
# ubuntu-based, the proxy settings can be copied into the container:
docker cp /etc/apt/apt.conf.d/95proxies $CONTAINER:/etc/apt/apt.conf.d/95proxies
docker cp /etc/environment $CONTAINER:/etc/environment
{% endhighlight %}

{% highlight bash %}
# let's pad it out a bit
docker exec -it $CONTAINER apt update
docker exec -it $CONTAINER apt install -y apt-utils dialog
docker exec -it $CONTAINER apt -y dist-upgrade
## optionally, possibly handy for some tasks:
docker exec -it $CONTAINER apt install -y ca-certificates  # [https://askubuntu.com/a/1145374], might be useful for adding external keys for whatever may need them
docker exec -it $CONTAINER apt install -y vim curl python3
{% endhighlight %}

{% highlight bash %}
# enter and have fun
docker exec -it $CONTAINER bash
{% endhighlight %}

---

#

Like with chroot, launching `X` apps within a docker container is also possible. A strong influence is drawn from [here](http://fabiorehm.com/blog/2014/09/11/running-gui-apps-with-docker/).

There will be a custom docker image needed, which can be created with the following `Dockerfile`:

```bash
FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y apt-utils dialog
RUN apt-get -y dist-upgrade
RUN apt-get install -y sudo

ARG user_uid
ARG user_gid

# Creating regular user "developer", with the sudoers entry
# also replacing his uid/gid with the host system user uid/gid
RUN export uid=${user_uid} gid=${user_gid} && \
    mkdir -p /home/developer && \
    mkdir -p /etc/sudoers.d && \
    echo "developer:x:${uid}:${gid}:Developer,,,:/home/developer:/bin/bash" >> /etc/passwd && \
    echo "developer:x:${uid}:" >> /etc/group && \
    echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer && \
    chmod 0440 /etc/sudoers.d/developer && \
    chown ${uid}:${gid} -R /home/developer

USER developer
ENV HOME /home/developer

CMD ["tail", "-f", "/dev/null"]
```

Let's build it and run a container:

```bash
docker build \
    --build-arg user_uid=`id -u` \
    --build-arg user_gid=`id -g` \
    -t regular_sudoer .

docker run -d \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    --name regular_sudoer_container \
    regular_sudoer
```

Enter...

```bash
docker exec -it regular_sudoer_container bash
```

...and have fun.