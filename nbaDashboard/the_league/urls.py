from django.urls import path, re_path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('team_name', views.team_names, name="team_names"),
    path('team_abbreviations', views.team_abbreviations, name="team_abbreviations"),

]