"""
WSGI config for bmt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# urls.py
from django.urls import path
from bmtapp import views

urlpatterns = [
    path("api/login/", views.login_view, name="login"),
    path("api/sections/<str:section_id>/", views.section_data, name="section_data"),
]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmt.settings')

application = get_wsgi_application()
