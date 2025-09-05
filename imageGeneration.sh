

echo "Building container images. This may take a while..."

LOGGEDUSER=$(logname)



echo "Building : arch_mod"
cd /usr/bin/theVirtualThings/containerImages/archlinuxImages/archlinux
su - $LOGGEDUSER -c 'cd /usr/bin/theVirtualThings/containerImages/archlinuxImages/archlinux && podman build -t arch_mod .'

echo "Building : arch_xfce"
cd /usr/bin/theVirtualThings/containerImages/archlinuxImages/archlinuxxfce
su - $LOGGEDUSER -c 'cd /usr/bin/theVirtualThings/containerImages/archlinuxImages/archlinuxxfce && podman build -t arch_xfce .'

echo "Building : deb_mod"
cd /usr/bin/theVirtualThings/containerImages/debianImages/debian
su - $LOGGEDUSER -c 'cd /usr/bin/theVirtualThings/containerImages/debianImages/debian && podman build -t deb_mod .'

echo "Building : debian_xfce"
cd /usr/bin/theVirtualThings/containerImages/debianImages/debianxfce
su - $LOGGEDUSER -c 'cd /usr/bin/theVirtualThings/containerImages/debianImages/debianxfce && podman build -t debian_xfce .'

echo "Building : fedora_mod"
cd /usr/bin/theVirtualThings/containerImages/fedoraImages/fedora
su -  $LOGGEDUSER -c 'cd /usr/bin/theVirtualThings/containerImages/fedoraImages/fedora && podman build -t fedora_mod .'

echo "Building : fedora_xfce"
cd /usr/bin/theVirtualThings/containerImages/fedoraImages/fedoraxfce
su - $LOGGEDUSER -c 'cd /usr/bin/theVirtualThings/containerImages/fedoraImages/fedoraxfce && podman build -t fedora_xfce .'

echo "Image building complete !"