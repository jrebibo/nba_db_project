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
    return render(request, 'teams.html', context)

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
def view_team_information(request):
    # Connect to DB & Get the requested team_abbreviation from index.html template
    cursor = connection.cursor()
    team_abbrev = request.POST.get('team_abbreviation')

    # Gets location and name of team
    sql_command = "SELECT Location, Name FROM Teams WHERE Abbreviation = "
    sql_command+= "'" + team_abbrev + "'"
    cursor.execute(sql_command)
    team_location_and_name = cursor.fetchall()
    print(team_location_and_name)
    team = team_location_and_name[0][0] + " " + team_location_and_name[0][1]

    # Gets team roster
    sql_command = "SELECT Player, Pos, Ht, Wt FROM Teams NATURAL JOIN Players NATURAL JOIN Plays_For WHERE Abbreviation = "
    sql_command+= "'" + team_abbrev + "'"
    cursor.execute(sql_command)
    team_roster = cursor.fetchall()

    # Gets team stats, this SQL command isn't completely correct. Double check this and change it. Don't know why it gets multiple
    sql_command = "SELECT Player, PPG, RPG, APG FROM Teams NATURAL JOIN Players NATURAL JOIN Plays_For NATURAL JOIN Stats WHERE Abbreviation = "
    sql_command+= "'" + team_abbrev + "'"
    cursor.execute(sql_command)
    team_stats = cursor.fetchall()

    # Gets team schedule
    sql_command = "SELECT Visitor, Visitor_PTS, Home, Home_PTS FROM Schedule WHERE Visitor = "
    sql_command+= "'" + team + "'" + " OR Home = " + "'" + team + "'"
    cursor.execute(sql_command)
    team_schedule = cursor.fetchall()

    # Gets head coach of team
    sql_command = "SELECT Coach_Name From Head_Coaches WHERE Abbreviation = "
    sql_command += "'" + team_abbrev + "'"
    cursor.execute(sql_command)
    # Index twice because it is given in a tuple
    team_coach = cursor.fetchall()[0][0]

    # Pass information into team_information html template
    context = {
        "team_roster": team_roster, 
        "team_stats": team_stats,
        "team_schedule": team_schedule,
        "team": team,
        "team_coach": team_coach,
    }
    return render(request, 'team_information.html', context) 

def add_information(request):
    pass

def add_player(request):
    pass