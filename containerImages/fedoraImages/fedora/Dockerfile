# Dockerfile
FROM docker.io/library/fedora:latest

RUN dnf upgrade -y && dnf install -y iproute nano iputils

# Commande pour build (le point va avec) : podman build -t fedora_mod .