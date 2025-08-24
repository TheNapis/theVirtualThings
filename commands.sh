
# Containers commands --------------------------------------------------------------------------------------
# VM PART (vm = virtual machine)

vm-create(){
    local name="$1"
    local xfce=false
    local vnc_port=5900
    local isolated=false
    local connect=false
    local network_name=""
    local run_now=false

    while [[ $# -gt 0 ]]; do
        case "$1" in
        --xfce|-x)
            xfce=true
            ;;
        --run-now|-r)
            run_now=true
            ;;
        --isolated|-i)
            if $connect; then
                echo "Error: --isolated and --connect cannot be used together."
                return 1
            fi
            isolated=true
            ;;
        --connect|-c)
            if $isolated; then
                echo "Error: --isolated and --connect cannot be used together."
                return 1
            fi
            connect=true
            network_name="$2"
            ;;
        
        --help|-h)
            echo "Usage: vm-create [OPTIONS] NAME"
            echo "Create a new Debian container with podman."
            echo ""
            echo "Options:"
            echo "--xfce, -x              Create a Debian container with XFCE desktop environment and VNC access."
            echo "--insolated, -i         Create an isolated container with no network access."
            echo "--connect, -c NET       Connect the container to an existing network NET."
            echo "--help, -h              Show this help message and exit."
            echo ""
            return 0
            ;;
        *)
            name="$1"
            ;;
        esac
        shift 1
    done

    if [[ -z "$name" ]]; then
        echo "Error: A name is required."
        echo "Try 'vm-create --help' for usage."
        return 1
    fi

    local args=()
    if $xfce; then
        vnc_port=$(find_free_port)
        args+=(-p "$vnc_port:5900" localhost/debian_xfce:latest)
    else
        args+=(localhost/deb_mod:latest)
    fi
    

    if podman create -it -h="$name" --name="$name" --network bridge --cap-add=NET_ADMIN --restart always --systemd always "${args[@]}" ; then
        if $xfce; then
            echo "Machine $name created with XFCE on port $vnc_port."
        else
            echo "Machine $name created."
        fi
        if $isolated; then
            podman network disconnect podman "$name"
            podman network create --internal isolated-$name
            podman network connect isolated-$name "$name"
            echo "Container $name is isolated into the isolated-$name network."
        elif $connect; then
            if podman network inspect $network_name &> /dev/null; then
                podman network connect "$network_name" "$name"
                echo "Container $name connected to network $network_name."
            else
                echo "Error: Network $network_name does not exist."
                podman rm "$name"
                echo "Container $name removed due to network configuration error."
                return 1
            fi
        fi
        $run_now && podman start "$name" && podman attach "$name"
        return 0
    else
        echo "Machine creation failed."
        return 1
    fi
}

vm-start(){
    local name="$1"
    if [[ -z "$name" ]]; then
        echo "Error: A name is required."
        echo "Try 'vm-start --help' for usage."
        return 1
    elif [[ $name == "-h" || $name == "--help" ]]; then
        echo "Usage: vm-start NAME"
        echo "Start an existing Podman container."
        echo ""
        echo "Options:"
        echo "--help, -h          Show this help message and exit."
        echo ""
        return 0
    fi
    podman start "$name"
}

vm-run(){
    local name="$1"
    if [[ -z "$name" ]]; then
        echo "Error: A name is required."
        echo "Try 'vm-run --help' for usage."
        return 1
    elif [[ $name == "-h" || $name == "--help" ]]; then
        echo "Usage: vm-run NAME"
        echo "Start and attach to an existing Podman container."
        echo ""
        echo "Options:"
        echo "--help, -h          Show this help message and exit."
        echo ""
        return 0
    fi
    podman start "$name" && podman attach "$name"
}

vm-attach(){
	local name="$1"
    if [[ -z "$name" ]]; then
        echo "Error: A name is required."
        echo "Try 'vm-attach --help' for usage."
        return 1
    elif [[ $name == "-h" || $name == "--help" ]]; then
        echo "Usage: vm-attach NAME"
        echo "Attach to a running Podman container."
        echo ""
        echo "Options:"
        echo "--help, -h          Show this help message and exit."
        echo ""
        return 0
    fi
    podman attach "$name"
}

vm-stop() {
    local name="$1"
    if [[ -z "$name" ]]; then
        echo "Error: A name is required."
        echo "Try 'vm-stop --help' for usage."
        return 1
    elif [[ $name == "-h" || $name == "--help" ]]; then
        echo "Usage: vm-stop NAME"
        echo "Stop a running Podman container."
        echo ""
        echo "Options:"
        echo "--help, -h          Show this help message and exit."
        echo ""
        return 0
    fi
    podman stop -t 3 "$name"
}

vm-rm() {
    local name="$1"
    if [[ -z "$name" ]]; then
        echo "Error: A name is required."
        echo "Try 'vm-rm --help' for usage."
        return 1
    elif [[ $name == "-h" || $name == "--help" ]]; then
        echo "Usage: vm-rm NAME"
        echo "Remove an existing Podman container."
        echo ""
        echo "Options:"
        echo "--help, -h          Show this help message and exit."
        echo ""
        return 0
    fi
    podman stop -t 3 "$name" && podman rm "$name"
}

vm-ls() {
    podman ps -a
}
vm-status() {
    local name="$1"
    if [[ -z "$name" ]]; then
        echo "Error: A name is required."
        echo "Try 'vm-status --help' for usage."
        return 1
    elif [[ $name == "-h" || $name == "--help" ]]; then
        echo "Usage: vm-status NAME"
        echo "Get the status of a Podman container."
        echo ""
        echo "Options:"
        echo "--help, -h          Show this help message and exit."
        echo ""
        return 0
    fi
    podman inspect --format '{{.State.Status}}' "$name"
}

# VN NETWORK PART (vn = virtual network)

vn-create() {
    local name=""
    local disable_dns=false
    local gateway=""
    local internal=false
    local subnet=""

    while [[ $# -gt 0 ]]; do
        case "$1" in
        --disable-dns|-d)
            disable_dns=true
            ;;
        --gateway|-g)
            gateway="$2"
            shift
            ;;
        --internal|-i)
            internal=true
            ;;
        --subnet|-s)
            subnet="$2"
            shift
            ;;
        --help|-h)
            echo "Usage: vn-create [OPTIONS] NAME"
            echo "Create a new Podman network."
            echo ""
            echo "Options:"
            echo "--disable-dns, -d   Disable DNS on the network."
            echo "--gateway, -g GW    Set gateway IP address."
            echo "--internal, -i      Make network internal (no external access)."
            echo "--subnet, -s SUBNET Set subnet (e.g. 10.88.0.0/16)."
            echo "--help, -h          Show this help message and exit."
            echo ""
            return 0
            ;;
        *)
            name="$1"
            ;;
        esac
        shift
    done

    if [[ -z "$name" ]]; then
        echo "Error: Network name is required."
        echo "Try 'vn-create --help' for usage."
        return 1
    fi

    local args=()
    $disable_dns && args+=(--disable-dns)
    [[ -n "$gateway" ]] && args+=(--gateway "$gateway")
    $internal && args+=(--internal)
    [[ -n "$subnet" ]] && args+=(--subnet "$subnet")

    if podman network create "${args[@]}" "$name"; then
        echo "Network $name created."
        return 0
    else
        echo "Network creation failed."
        return 1
    fi
}

vn-ls() {
    podman network ls
}

vn-rm() {
    local name="$1"
    if [[ -z "$name" ]]; then
        echo "Error: A name is required."
        echo "Try 'vn-rm --help' for usage."
        return 1
    elif [[ $name == "-h" || $name == "--help" ]]; then
        echo "Usage: vn-rm NAME"
        echo "Remove an existing Podman network."
        echo ""
        echo "Options:"
        echo "--help, -h          Show this help message and exit."
        echo ""
        return 0
    fi
    podman network rm "$name"
}

vn-info() {
    local name="$1"
    podman network inspect "$name"
}

vn-connect() {
    local network_name="$1"
    local container_name="$2"
    if [[ -z "$network_name" || -z "$container_name" ]]; then
        echo "Error: Network name and container name are required."
        echo "Try 'vn-connect --help' for usage."
        return 1
    elif [[ $network_name == "-h" || $network_name == "--help" || $container_name == "-h" || $container_name == "--help" ]]; then
        echo "Usage: vn-connect NETWORK CONTAINER"
        echo "Connect a Podman container to a network."
        echo ""
        echo "Options:"
        echo "--help, -h          Show this help message and exit."
        echo ""        
        return 0
    fi
    podman network connect "$network_name" "$container_name"
}

vn-disconnect() {
    local network_name="$1"
    local container_name="$2"
    if [[ -z "$network_name" || -z "$container_name" ]]; then
        echo "Error: Network name and container name are required."
        echo "Try 'vn-disconnect --help' for usage."
        return 1
    elif [[ $network_name == "-h" || $network_name == "--help" || $container_name == "-h" || $container_name == "--help" ]]; then
        echo "Usage: vn-disconnect NETWORK CONTAINER"
        echo "Disconnect a Podman container from a network."
        echo ""
        echo "Options:"
        echo "--help, -h          Show this help message and exit."
        echo ""        
        return 0
    fi
    podman network disconnect "$network_name" "$container_name"
}



# Le seul but de find_free_port est de trouver le premier port libre à partir de 5900
find_free_port() {
    local port=5900
    while podman container ps --format '{{.Ports}}' -a | grep -q "$port"; do
        ((port++))
    done
    echo "$port"
}
