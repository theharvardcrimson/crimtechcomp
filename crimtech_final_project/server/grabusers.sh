#!/bin/bash

rpass() {
    strings /dev/urandom | grep -o '[[:alnum:]!@#$%^&*()<>,.,{}]' | head -n $1 | tr -d '\n'; echo
}

new_user() {
    USR=$1
    KEYS_FILE=$2

    data=`grep "$USR" "$KEYS_FILE"`
    pubkey=`echo "$data" | awk '{print $1" "$2" "$3}'`
    email=`echo "$data" | awk '{print $4}'`
    name=`echo "$data" | cut -d ' ' -f5-`

    pass=`rpass 12`

    useradd -d /home/$USR -m -c "$name,,," -s "/bin/bash" $USR
    echo -e "$pass\n$pass\n" | passwd $USR > /dev/null 2>&1
    usermod -a -G sudo "$USR"
    echo "$pass" > /home/"$USR"/.pass
    chmod 700 /home/"$USR"/.pass
    mkdir /home/"$USR"/.ssh/
    echo "$pubkey" >> /home/"$USR"/.ssh/authorized_keys
    chown -R "$USR:$USR" /home/"$USR"/.ssh
    chmod 700 /home/"$USR"/.ssh
    chmod 644 /home/"$USR"/.ssh/authorized_keys
}

usage() {
    echo "Usage:"
    echo "`basename $0` [keyfile URI]"
    echo
    exit 1
}

KEY_URI=$1

if [ -z "$KEY_URI" ]; then
    KEY_URI='http://static.thecrimson.com/userkeys'
fi
wget -O /tmp/keys "$KEY_URI"

KEY_FILE='/tmp/keys'

if [ -z "$KEY_FILE" ]; then
    usage
fi

for USR in `cat "$KEY_FILE"  | awk '{print $3}'`; do
    if `id $USR > /dev/null 2>&1`; then
        echo "$USR already exists!"
    else
        echo Creating $USR
        new_user "$USR" "$KEY_FILE"
    fi
done
