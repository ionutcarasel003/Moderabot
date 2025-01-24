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
    path('admin/', admin.site.urls),
    path('', views.welcome, name='welcome'),
    path('rules/', views.rules_list, name='rules_list'),
    path('rule/edit/<int:rule_id>/', views.edit_rule, name='edit_rule'),
    path('users/', views.user_list, name='user_list'),
    path('violations/', views.violation_list, name='violation_list'),
    path('rule/delete/<int:rule_id>/', views.delete_rule, name='delete_rule'),
    path('rule/add/', views.add_rule, name='add_rule'),
    path('user/reset-severity/<int:user_id>/', views.reset_severity, name='reset_severity'),
    path('user/mute/<int:user_id>/', views.mute_user, name='mute_user'),
]