# Dockerfile
FROM docker.io/library/fedora:latest

COPY script.sh /home/script.sh

RUN dnf upgrade -y && dnf install -y iproute nano iputils tigervnc-server sudo xorg-x11-server-Xorg xorg-x11-xinit xorg-x11-drv-libinput mesa-dri-drivers xfce4-panel xfce4-session  xfce4-settings  xfconf  xfdesktop xfwm4 xfce4-terminal

EXPOSE 5900

RUN chmod 755 /home/script.sh

RUN useradd -m -G wheel user
RUN echo 'user ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/user && chmod 0440 /etc/sudoers.d/user
USER user
WORKDIR /home/user

ENTRYPOINT "/home/script.sh" && /bin/bash


# Commande pour build (le point va avec) : podman build -t fedora_xfce .

