#!/bin/bash

vagrant ssh -c "if ! [ -e /srv/crimson/log/django.log ];
                then touch /srv/crimson/log/django.log && sudo chown vagrant:www-data /srv/crimson/log/django.log;
                else echo > /srv/crimson/log/django.log; fi;
                tail -f /srv/crimson/log/django.log"
