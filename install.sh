#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root or use sudo"
  exit
fi


if [ -f /etc/debian_version ]; then
    # Debian/Ubuntu
    apt update
    apt install -y python3 podman python3-pyqt5
elif [ -f /etc/fedora-release ]; then
    # Fedora
    dnf install -y python3 podman python3-qt5
elif [ -f /etc/arch-release ]; then
    # Arch
    pacman -Sy --noconfirm python podman python-pyqt5
else
    echo "Unknown distribution. Please install theVirtualThings manually."
    exit 1
fi


rm -rf /usr/bin/theVirtualThings
cp -r "$(pwd)" /usr/bin/theVirtualThings


cat > /etc/profile.d/thevirtualthings.sh << 'EOF'
PATH=$PATH:/usr/bin/theVirtualThings/tvtcommands
PATH=$PATH:/usr/bin/theVirtualThings/UI
export PATH
EOF


chmod  +x /usr/bin/theVirtualThings/theVirtualThings.desktop
cp /usr/bin/theVirtualThings/theVirtualThings.desktop /usr/share/applications/


cd /usr/bin/theVirtualThings/containerImages/archlinuxImages/archlinux
sudo -u $USER podman build -t arch_mod .

cd /usr/bin/theVirtualThings/containerImages/archlinuxImages/archlinuxxfce
sudo -u $USER podman build -t arch_xfce .

cd /usr/bin/theVirtualThings/containerImages/debianImages/debian
sudo -u $USER podman build -t deb_mod .

cd /usr/bin/theVirtualThings/containerImages/debianImages/debianxfce
sudo -u $USER podman build -t debian_xfce .

cd /usr/bin/theVirtualThings/containerImages/fedoraImages/fedora
sudo -u $USER podman build -t fedora_mod .

cd /usr/bin/theVirtualThings/containerImages/fedoraImages/fedoraxfce
sudo -u $USER podman build -t fedora_xfce .

echo "Installation terminée."