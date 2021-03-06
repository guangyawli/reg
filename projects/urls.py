"""demox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from projects.views import *

urlpatterns = [
    path('', index, name='projects_home'),
    path('rated_projects', rated_projects, name='Rated_projects'),
    path('judge_list', judge_list, name='judge_list'),
    path('judge_member', judge_member, name='judge_member'),
    path('judge_detail/<int:judge_id>/', judge_detail, name='judge_detail'),
    path('super_list', super_list, name='super_list')
]
