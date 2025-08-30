#!/usr/bin/env bash

export $(dbus-launch)
export DISPLAY=:0.0
Xvnc :0 -SecurityTypes=none &
startxfce4 &

