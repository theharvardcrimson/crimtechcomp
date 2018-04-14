import os
import sys
import site

# _project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'releases', 'current')
_project_path = '/srv/crimson/releases/current'
os.environ['DJANGO_SETTINGS_MODULE'] = 'crimsononline.settings'

os.environ['X_DJANGO_PROJECT_PATH'] = _project_path

site.addsitedir('/srv/crimson/venv/lib/python2.7/site-packages')
sys.path.append('/srv/crimson/releases/current')
sys.path.append('/srv/crimson/releases/current/crimsononline')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


import wsgi.monitor
wsgi.monitor.start(interval=1.0)
