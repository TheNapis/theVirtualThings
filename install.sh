#!/bin/bash

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root or use sudo"
  exit 1
fi


rm -rf /usr/bin/theVirtualThings

chmod +x /usr/bin/theVirtualThings/tvtcommands/*
chmod +x /usr/bin/theVirtualThings/UI/*
sudo cp -r "$(pwd)" /usr/bin/theVirtualThings


cat > /etc/profile.d/thevirtualthings.sh << 'EOF'
PATH=$PATH:/usr/bin/theVirtualThings/tvtcommands
PATH=$PATH:/usr/bin/theVirtualThings/UI
export PATH
EOF


cp theVirtualThings.desktop /usr/share/applications/

echo "Installation terminée."