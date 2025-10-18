#!/bin/bash
# Check for jq and curl dependency
for cmd in jq curl; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ Error: '$cmd' is not installed. Please install it using your package manager:"
        if [ "$cmd" = "jq" ]; then
            echo "Ubuntu: sudo apt install -y jq"
        elif [ "$cmd" = "curl" ]; then
            echo "Ubuntu: sudo apt install -y curl"
        fi
        exit 1
    fi
done

# Load environment variables
ENVFILE="/home/dcastroosorio/downloads/info/ess_scripts/who/.whoisenv"
source "$ENVFILE"

# This is the API token
token="${ipinfoToken}"

# Check if IP argument is provided
if [ -z "$1" ]; then
    echo "❌ Error: No IP address provided"
    echo "Usage: $0 <IP_ADDRESS>"
    echo "Example: $0 8.8.8.8"
    exit 1
fi

# Get IP from command-line argument
ip="$1"
echo

# Run the request and capture output
result=$(curl -s -H "Accept: application/json" "ipinfo.io/$ip?token=$token")

# Result
if echo "$result" | jq empty 2>/dev/null; then
    echo "✅ IP Information:"
    echo "$result" | jq .
else
    echo "⚠️ API did not return valid JSON or an error occurred."
    echo "Raw response:"
    echo "$result"
fi