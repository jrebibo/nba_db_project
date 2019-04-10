from django.urls import path, re_path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('teams', views.get_team_info, name="team_information"),
    path('team_name', views.get_team_names, name="team_names"),
    path('team_abbreviations', views.get_team_abbreviations, name="team_abbreviations"),
    path('team_location', views.get_team_location, name="team_locations"),
    path('view_roster', views.view_roster, name="view_roster"),


]