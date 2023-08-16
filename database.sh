#!/bin/bash
echo "HELLP"

if [ -z "$DB_CRED" ]; then
    echo "HELL2"
    exit 1
fi

# Extract username and password using string manipulation
username=$(echo "$DB_CRED" | sed -n 's/.*"username":"\([^"]*\)".*/\1/p')
password=$(echo "$DB_CRED" | sed -n 's/.*"password":"\([^"]*\)".*/\1/p')

export DB_USER="$username"
export DB_PASSWORD="$password"

# Run your application or script that uses USER and PASSWORD