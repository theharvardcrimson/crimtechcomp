#!/bin/bash

for USR in $(getent passwd | tr ":" " " | awk "\$3 > $(grep UID_MIN /etc/login.defs | cut -d " " -f 2) { print \$1 }" | sort); do
    if [ $USR != "nobody" ] && [ $USR != "crimson" ]; then
        userdel "$USR" && rm -r /home/"$USR" && echo "$USR removed"
    fi
done
exit
