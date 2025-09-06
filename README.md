# theVirtualThings

Works with podman.

Installation command : 

```bash 
git clone https://github.com/TheNapis/theVirtualThings.git && cd theVirtualThings && chmod +x ./install.sh && sudo ./install.sh
```



## Containers commands 
### VM PART (vm = virtual machine)

vm-create : Create a new Debian container with podman.

vm-start : Start an existing Podman container.

vm-run : Start and attach to an existing Podman container.

vm-attach : Attach to a running Podman container.

vm-stop : Stop a running Podman container.

vm-rm : Remove an existing Podman container. (If the container has not been stopped, it stops it within 3 seconds and then deletes it.) 

vm-ls : It just list all the Podman containers created.

vm-status : Get the status of a Podman container.

---

### VN NETWORK PART (vn = virtual network)

vn-create : Create a new Podman network.

vn-ls : It just list all the Podman networks created. 

vn-rm : Remove an existing Podman network.

vn-info : Getting informations about a Podman network.

vn-connect : Connect a Podman container to a network.

vn-disconnect : Disconnect a Podman container from a network.

---

### ESSENTIALS FUNCTIONS

find_free_port : That is getting fre ports after 5900 (Used for vm-create with -x option for VNC)


## Help

**For how to use a command : COMMAND -h or --help**

Exemple : vm-create -h

_The help page is not implemented for find_free_port as it's not meant to use normaly_


How can i access a VM virtual screen : use TigerVNC or another VNC Client and the address is localhost:{your exposed port 5900,5901,...}

Your exposed VNC port : map[5900/tcp:[{0.0.0.0 **5901**}]] is 5901 in that situation


### For WSL : Fedora is strongly recomended 

You need to install a file manager like thunar or dolphin
and a terminal emulator like xfce4-terminal or konsole


