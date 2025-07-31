#!/bin/bash

input_file="domains.txt"

while read -r domain; do
    domain=$(echo "$domain" | tr -d '[:space:]')  # Trim leading/trailing whitespace
    [ -z "$domain" ] && continue  # Skip empty lines

    echo "Domain: $domain"

    # Get SPF record
    spf_record=$(dig +short TXT "$domain" | grep -i "v=spf1")
    if [ -n "$spf_record" ]; then
        echo "  SPF: $spf_record"
    else
        echo "  SPF: Not found"
    fi

    # Get DMARC record
    dmarc_record=$(dig +short TXT "_dmarc.$domain" | grep -i "v=DMARC1")
    if [ -n "$dmarc_record" ]; then
        echo "  DMARC: $dmarc_record"
    else
        echo "  DMARC: Not found"
    fi

    echo
done < "$input_file"

