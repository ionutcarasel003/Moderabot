"""
URL configuration for moderabot_dj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from Moderabot import views


urlpatterns = [
    path('', views.home, name='home'),
    path('violations/', views.violation_list, name='violation_list'),
    path('rules/', views.rule_list, name='rule_list'),
    path('users/', views.user_list, name='user_list'),
]