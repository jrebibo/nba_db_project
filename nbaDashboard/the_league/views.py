from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    cursor = connection.cursor()
    cursor.execute('SELECT Name, Location, Abbreviation FROM Teams')
    teams = cursor.fetchall()
    teams_list = []
    for value in teams:
        teams_list.append(value[0])
    
    context = {
        "team_info": teams
    }
    return render(request, 'index.html', context)

def get_team_info(request):
    cursor = connection.cursor()
    cursor.execute('SELECT Name, Location, Abbreviation FROM Teams')
    teams = cursor.fetchall()
    context = {
        "team_info": teams,
    }
    return render(request, 'team_information.html', context)

def get_team_names(request):
    cursor = connection.cursor()
    cursor.execute('SELECT Name FROM Teams')
    teams = cursor.fetchall()
    teams_list = []
    for value in teams:
        teams_list.append(value[0])
    
    context = {
        "teams_list": teams_list
    }
    return render(request, 'team_names.html', context)

def get_team_abbreviations(request):
    cursor = connection.cursor()
    cursor.execute('SELECT Abbreviation FROM Teams')
    teams = cursor.fetchall()
    abbr_list = []
    for value in teams:
        abbr_list.append(value[0])

    context = {
        "abbr_list": abbr_list
    }
    return render(request, 'team_abbreviations.html', context)

def get_team_location(request):
    cursor = connection.cursor()
    cursor.execute('SELECT Location FROM Teams')
    teams = cursor.fetchall()
    location_list = []
    for value in teams:
        print(value[0])
        location_list.append(value[0])

    context = {
        "location_list": location_list
    }
    return render(request, 'team_locations.html', context)

@csrf_exempt
def view_roster(request):
    print(request.POST.get('roster'))
    team_abbrev = request.POST.get('roster')
    cursor = connection.cursor()
    sql_command = "SELECT Player, Pos, Ht, Wt FROM Teams NATURAL JOIN Players NATURAL JOIN Plays_For WHERE Abbreviation = "
    sql_command+= "'" + team_abbrev + "'"
    print(sql_command)
    cursor.execute(sql_command)
    context = {
        "team_roster": cursor.fetchall()
    }
    return render(request, 'team_roster.html', context) 