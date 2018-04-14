#!/bin/bash

vagrant ssh -c "if ! [ -e /srv/crimson/log/error.log ];
                then sudo touch /srv/crimson/log/error.log;
                else sudo echo | sudo tee /srv/crimson/log/error.log > /dev/null; fi;
                tail -f /srv/crimson/log/error.log"
