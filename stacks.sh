#!/bin/bash
# Created by Diego Castro.
# Purpose: SMTP Authentication testing tool fo PPE support.

# Added a menu - no need but just wanted to practice from previous project.
menu() {
    cat <<'OPTIONS'
[1] Check domain.
[q] To quit. 👋

OPTIONS
}

#Declaring stacks array
stacks=("eu1" "us1" "us2" "us3" "us4" "us5" "usg1" "usg2")

user_info() {
    read -rep "Username: " username
    read -rep "Password: " password
    read -rep "Domain: " domain
    echo
}

domain_info() {
    user_info

    for location in "${stacks[@]}"; do
        response=$(curl -s \
            -X GET \
            -H "X-User: ${username}" \
            -H "X-Password: ${password}" \
            "https://${location}.proofpointessentials.com/api/v1/orgs/${domain}")

        eid=$(echo "$response" | grep -o '"eid":[0-9]*' | cut -d':' -f2)

        url="https://${location}.proofpointessentials.com/i/${eid}/dashboard"

        if [[ -n "$eid" ]]; then
            printf "Location: %s\nEID: %s\nURL: %s\n\n" \
            "${location^^}" "$eid" "$url"
        fi
    done
}

while true;do
    menu

    read -rep "➤ Select an option: " option
    echo

    case $option in
    1) 
        domain_info
        ;;
    q|Q) 
        echo "Bye 👋."
        exit 0
        ;;
    *)
        echo "Invalid option. Try again."
        ;;
    esac
done