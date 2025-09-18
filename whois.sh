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
source .env

# This is the API key
API_key="${whoisKey}"

# Asking the user for the IP
read -p "IP: " ip
echo

# Run the request and capture output
result=$(curl -s "https://api.whatismyip.com/whois.php?key=$API_key&input=$ip&output=json")

# Result
if echo "$result" | jq empty 2>/dev/null; then
    echo "✅ Parsed JSON:"
    echo "$result" | jq .
else
    echo "⚠️ API did not return JSON. Parsing WHOIS text..."
    raw=$(curl -s "https://api.whatismyip.com/whois.php?key=$API_key&input=$ip")

    # Extract useful fields (OrgName, Country, ASN, NetRange, CIDR, etc.)
    org=$(echo "$raw"     | grep -iE "OrgName|Organization" | head -n1 | cut -d: -f2- | xargs)
    country=$(echo "$raw" | grep -i "Country"               | head -n1 | cut -d: -f2- | xargs)
    cidr=$(echo "$raw"    | grep -i "CIDR"                  | head -n1 | cut -d: -f2- | xargs)
    netrange=$(echo "$raw"| grep -i "NetRange"              | head -n1 | cut -d: -f2- | xargs)

    echo
    echo "📡 WHOIS Summary for $ip"
    echo "----------------------------"
    echo "OrgName : $org"
    echo "Country : $country"
    echo "CIDR    : $cidr"
    echo
fi