import os
import site
import sys

# KIOSK_ROOT should be defined via SetEnv in your Apache configuration.
# to the directory esmond is installed in.
# SetEnv doesn't work? WTF?!?!
os.environ['KIOSK_ROOT'] = "/a/scinet-kiosk"
if not os.environ.has_key('KIOSK_ROOT'):
    print >>sys.stderr, "Please define KIOSK_ROOT in your Apache configuration"
    exit()
rootpath=os.environ['KIOSK_ROOT']
# This will make Django run in a virtual env
# Remember original sys.path.
prev_sys_path = list(sys.path)

# Add each new site-packages directory.
site.addsitedir(rootpath+'/lib/python2.6/site-packages')

# Reorder sys.path so new directories at the front.
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

os.environ['DJANGO_SETTINGS_MODULE'] = 'kiosk_example.settings'

print >>sys.stderr, "path=", sys.path
try:
    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()
except Exception, e:
    print >>sys.stderr,"exception:",e

"""
Example apache httpd.conf directives:
Make sure that WSGIPassAuthorization is on when using the tastypie/django
level auth or mod_wsgi will munch the auth headers.

WSGIScriptAlias / /services/kiosk_example/kiosk_example/wsgi.py
WSGIPythonPath /services/kiosk_example/kiosk_example:/services/kiosk_example/venv/lib/python2.7/site-packages
WSGIPythonHome /services/kiosk_example/venv
WSGIPassAuthorization On

WSGIDaemonProcess www python-path=/services/kiosk_example/kiosk_example:/services/kiosk_example/venv/lib/python2.7/site-packages home=/services/kiosk_example processes=3 threads=15
WSGIProcessGroup www

<Directory /services/kiosk_example/kiosk_example>
<Files wsgi.py>
SetEnv ESMOND_ROOT /services/kiosk_example
AuthType None
Order deny,allow
Allow from all
</Files>
</Directory>
"""
