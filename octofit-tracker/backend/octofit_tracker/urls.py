"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.contrib import admin
from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

CODESPACE_NAME = os.getenv('CODESPACE_NAME', '')
CODESPACE_HOST = f"{CODESPACE_NAME}-8000.app.github.dev" if CODESPACE_NAME else None
CODESPACE_BASE = f"https://{CODESPACE_HOST}" if CODESPACE_HOST else None


def get_url_base(request):
    if CODESPACE_BASE:
        return CODESPACE_BASE
    # use request host for local runs
    proto = 'https' if request.is_secure() else 'http'
    return f"{proto}://{request.get_host()}"


@api_view(['GET'])
def api_root(request, format=None):
    base = get_url_base(request)
    return Response({
        'users': f"{base}/api/users/",
        'teams': f"{base}/api/teams/",
        'activities': f"{base}/api/activities/",
        'workouts': f"{base}/api/workouts/",
        'leaderboard': f"{base}/api/leaderboard/",
    })


@api_view(['GET'])
def api_component(request, component, format=None):
    base = get_url_base(request)
    return Response({
        'component': component,
        'api_url': f"{base}/api/{component}/",
        'message': 'API endpoint active',
    })


def root_status(request):
    base = get_url_base(request)
    return JsonResponse({
        'status': 'ok',
        'message': 'Octofit API is running',
        'api_root': f"{base}/api/",
    })


urlpatterns = [
    path('', root_status),
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/<str:component>/', api_component),
]
