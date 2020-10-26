"""
WSGI config for reg project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys
from os.path import join, dirname, abspath

PROJECT_DIR = dirname(dirname(abspath(__file__)))

sys.path.insert(0, PROJECT_DIR)
sys.path.append('/home/xyaw/reg/xvenv/lib/python3.6/site-packages/')

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'reg.settings'

application = get_wsgi_application()
