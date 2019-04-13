from django.urls import path, re_path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('teams', views.get_team_info, name="team_information"),
    path('team_name', views.get_team_names, name="team_names"),
    path('team_abbreviations', views.get_team_abbreviations, name="team_abbreviations"),
    path('team_location', views.get_team_location, name="team_locations"),
    path('view_team', views.view_team_information, name="view_team"),
    path('add', views.add_information, name="add"),
    path('add_player', views.add_player, name="add_player"),
    path('base_template', views.base_template, name = 'base_template'),
    path('team_dashboard', views.team_dashboard, name = 'team_dashboard'),
    path('player_dashboard', views.player_dashboard, name = 'player_dashboard'),
    path('team/<str:team_abbr>', views.team, name = 'team'),
    path('player/<int:player_id>', views.player, name ='player')

]