#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root or use sudo"
  exit
fi

cp -r ./ /usr/bin/theVirtualThings

cat >> /etc/profile.d/thevirtualthings.sh << \EOF
  PATH=$PATH:/usr/bin/theVirtualThings/tvtcommands
  PATH=$PATH:/usr/bin/theVirtualThings/UI
  export PATH
EOF

sudo mv ~/.local/share/applications/<application-name.desktop> /usr/share/applications/