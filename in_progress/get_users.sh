#!/bin/bash

username="api@pfptmail.com"
password="Hola@ThisIs%AP1"

# To do:
# Need to figure how to fiter by type of user

creds_domain() {
  # read -rep "Username: " username
  # read -rep "Password: " password
  # echo
  read -rep "Enter domain: " domain
  read -rep "Enter stack: " stack 
}

menu(){
  cat <<'USERS'

[1] End Users
[2] Silent Users
[3] Organizational Admins
[4] Channel Admins
[5] Functional Accounts
[6] All Users Except Functional Accounts
[7] All Users

USERS
}

response() {
  echo
  creds_domain
  echo

  curl -s -X GET \
  -H "X-User: $username" \
  -H "X-Password: $password" \
  https://"$stack".proofpointessentials.com/api/v1/orgs/"$domain"/users \
  | jq .
}

while true;do
  menu
  read -rep "➤ Select an option [1 – 7 | q = quit]: " option

  case $option in
    1) 
      response
      ;;  
      
    q|Q)
      echo
      echo "Bye 👋"
      exit 0
      ;;
    *)
      echo
      echo "Invalid option. Please try again."
  esac
  
done