from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
# Create your views here.

def index(request):
    return render(request, 'index.html')

def team_names(request):
    cursor = connection.cursor()
    cursor.execute('SELECT Name FROM Teams')
    teams = cursor.fetchall()
    teams_list = []
    for value in teams:
        teams_list.append(value[0])
    return HttpResponse(teams_list)

def team_abbreviations(request):
    cursor = connection.cursor()
    cursor.execute('SELECT Abbreviation FROM Teams')
    teams = cursor.fetchall()
    abbr_list = []
    for value in teams:
        print(value[0])
        abbr_list.append(value[0])
    return HttpResponse(abbr_list)