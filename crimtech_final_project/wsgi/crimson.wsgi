import os
import sys
import site

os.environ['DJANGO_SETTINGS_MODULE'] = 'crimsononline.settings'
site.addsitedir('/srv/crimson/venv/lib/python2.7/site-packages')
sys.path.append('/srv/crimson/releases/current')
sys.path.append('/srv/crimson/releases/current/crimsononline')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

#from werkzeug.debug import DebuggedApplication
#application = DebuggedApplication(application, evalex=True)

import newrelic.agent
newrelic.agent.initialize('/srv/crimson/newrelic.ini')
application = newrelic.agent.wsgi_application()(application)
