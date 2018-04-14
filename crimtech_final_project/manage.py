#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crimsononline.settings')
    from django.core.management import execute_from_command_line

    # Communicate true project path to settings.py
    os.environ['X_DJANGO_PROJECT_PATH'] = os.path.dirname(
        os.path.abspath(__file__))

    execute_from_command_line(sys.argv)
