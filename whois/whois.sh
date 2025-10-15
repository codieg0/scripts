#!/bin/bash

# sourcing token
if [ -f ~/.whoisenv]; then
    source ~/.whoisenv
elif [ -f ./whoisenv ]; then
    source ./whoisenv
fi

# Simple IP lookup script

if [ -z "$1" ]; then
    read -p "IP: " ip
else
    ip="$1"
fi

# Strip CIDR notation if present
ip=${ip%%/*}

curl -s "https://ipinfo.io/${ip}/json?token=$token"