# Dockerfile
FROM docker.io/library/debian:stable

COPY script.sh /home/script.sh

RUN apt update && apt install -y iproute2 nano iputils-ping tigervnc-standalone-server tigervnc-xorg-extension xfce4 dbus-x11 sudo xfce4-terminal

EXPOSE 5900

RUN chmod 755 /home/script.sh

RUN adduser --disabled-password --gecos '' user && adduser user sudo
RUN echo 'user ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/user && chmod 0440 /etc/sudoers.d/user
USER user
WORKDIR /home/user

ENTRYPOINT "/home/script.sh" && /bin/bash


# Commande pour build (le point va avec) : podman build -t debian_xfce .

