#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root or use sudo"
  exit
fi


echo "Updating your depots and installing dependencies..."

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


echo "Removing old installation and copying new files..."
rm -rf /usr/bin/theVirtualThings
cp -r "$(pwd)" /usr/bin/theVirtualThings


echo "Setting up environment variables..."
cat > /etc/profile.d/thevirtualthings.sh << 'EOF'
PATH=$PATH:/usr/bin/theVirtualThings/tvtcommands
PATH=$PATH:/usr/bin/theVirtualThings/UI
export PATH
EOF

echo "Creating desktop entry..."
chmod  +x /usr/bin/theVirtualThings/theVirtualThings.desktop
cp /usr/bin/theVirtualThings/theVirtualThings.desktop /usr/share/applications/



echo "Building container images. This may take a while..."

LOGGEDUSER=$(logname)



echo "Building : arch_mod"
cd /usr/bin/theVirtualThings/containerImages/archlinuxImages/archlinux
su - $LOGGEDUSER -c 'podman build -t arch_mod .'

echo "Building : arch_xfce"
cd /usr/bin/theVirtualThings/containerImages/archlinuxImages/archlinuxxfce
su - $LOGGEDUSER -c 'podman build -t arch_xfce .'

echo "Building : deb_mod"
cd /usr/bin/theVirtualThings/containerImages/debianImages/debian
su - $LOGGEDUSER -c 'podman build -t deb_mod .'

echo "Building : debian_xfce"
cd /usr/bin/theVirtualThings/containerImages/debianImages/debianxfce
su - $LOGGEDUSER -c 'podman build -t debian_xfce .'

echo "Building : fedora_mod"
cd /usr/bin/theVirtualThings/containerImages/fedoraImages/fedora
su -  $LOGGEDUSER -c 'podman build -t fedora_mod .'

echo "Building : fedora_xfce"
cd /usr/bin/theVirtualThings/containerImages/fedoraImages/fedoraxfce
su - $LOGGEDUSER -c 'podman build -t fedora_xfce .'

echo "Installation terminée."