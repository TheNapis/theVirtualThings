# Dockerfile
FROM docker.io/library/archlinux:latest

COPY script.sh /home/script.sh

RUN pacman -Syu --noconfirm iproute2 nano iputils tigervnc xfce4 dbus sudo xfce4-terminal

EXPOSE 5900

RUN chmod 755 /home/script.sh

RUN useradd -m -G wheel user
RUN echo 'user ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/user && chmod 0440 /etc/sudoers.d/user
USER user
WORKDIR /home/user

ENTRYPOINT "/home/script.sh" && /bin/bash


# Commande pour build (le point va avec) : podman build -t arch_xfce .

