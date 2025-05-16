"""
WSGI config for AirTrafficProject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
print("PYTHONPATH:", sys.path)
sys.path.append('/opt/render/project/src/AirTrafficProject')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AirTrafficProject.settings')

application = get_wsgi_application()
