#!/bin/bash

VAGRANT_COMMAND="/srv/crimson/venv/bin/python /srv/crimson/releases/current/manage.py $@"
vagrant ssh -c "cd /srv/crimson/releases/current/ && $VAGRANT_COMMAND"
unset VAGRANT_COMMAND
