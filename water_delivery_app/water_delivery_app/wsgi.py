"""
WSGI config for water_delivery_app project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

print("📂 Current Working Directory:", os.getcwd())
print("📦 Python Path:", sys.path)
print("📁 Files in Current Directory:", os.listdir(os.getcwd()))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'water_delivery_app.settings')

application = get_wsgi_application()
