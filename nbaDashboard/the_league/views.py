from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db import connections, connection
from django.views.decorators.csrf import csrf_exempt
from .forms import *
# Create your views here.

from passlib.hash import sha256_crypt

def index(request):
    try:
        user_type = request.session['user_type']
    except:
        return redirect('login')
    cursor = connections['nba'].cursor()
    cursor.execute('SELECT Name, Location, Abbreviation FROM Teams')
    teams = cursor.fetchall()
    teams_list = []
    for value in teams:
        teams_list.append(value[0])
    
    context = {
        "team_info": teams,
        "user_type": request.session['user_type']
    }
    return render(request, 'index2.html', context)

def get_team_info(request):
    cursor = connections['nba'].cursor()
    cursor.execute('SELECT Name, Location, Abbreviation FROM Teams')
    teams = cursor.fetchall()
    context = {
        "team_info": teams,
    }
    return render(request, 'teams.html', context)

def get_team_names(request):
    cursor = connections['nba'].cursor()
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
    cursor = connections['nba'].cursor()
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
    cursor = connections['nba'].cursor()
    cursor.execute('SELECT Location FROM Teams')
    teams = cursor.fetchall()
    location_list = []
    for value in teams:
        location_list.append(value[0])

    context = {
        "location_list": location_list
    }
    return render(request, 'team_locations.html', context)

@csrf_exempt
def view_team_information(request):
    # Connect to DB & Get the requested team_abbreviation from index.html template
    cursor = connections['nba'].cursor()
    team_abbrev = request.POST.get('team_abbreviation')

    # Gets location and name of team
    sql_command = "SELECT Location, Name FROM Teams WHERE Abbreviation = "
    sql_command+= "'" + team_abbrev + "'"
    cursor.execute(sql_command)
    team_location_and_name = cursor.fetchall()
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
    form = AddPlayerForm()
    context = {
        "add_player_form": form
    }
    return render(request, 'add_information.html', context)


def base_template(request):
    try:
        user_type = request.session['user_type']
    except:
        return redirect('login')
    return render(request, 'base_template.html')

@csrf_exempt
def add_player(request):
    if request.method == 'POST':
        # Gets form object to render in template view
        form = AddPlayerForm(request.POST)
        if form.is_valid():
            # Gets field from form
            number = form.cleaned_data['number']
            player = form.cleaned_data['player']
            position = form.cleaned_data['position']
            height = form.cleaned_data['height']
            weight = form.cleaned_data['weight']
            team = form.cleaned_data['team']

            # Run command to insert into database
            sql_command = "INSERT INTO Players (No, Player, Pos, Ht, Wt) VALUES ('"
            sql_command += str(number) + "', '" + player + "', '" + position + "', '" + height + "', '" + str(weight) + "')"
            
            cursor = connections['nba'].cursor()
            cursor.execute(sql_command)

            sql_command = "SELECT Player_ID FROM Players WHERE Player = "
            sql_command+= "'" + str(player) + "' AND No = "
            sql_command+= "'" + str(number) + "'"
            cursor.execute(sql_command)
            response = cursor.fetchall()
            player_id = response[0][0]

            sql_command = "INSERT INTO Plays_For (Player_ID, Abbreviation) VALUES ('"
            sql_command+= str(player_id) + "', '" + str(team) + "')"
            cursor.execute(sql_command)

            return redirect("index")
    return HttpResponse(request)

def team(request, team_abbr):

    try:
        user_type = request.session['user_type']
    except:
        return redirect('login')

    cursor = connections['nba'].cursor()
    
    sql_command = "SELECT * FROM Plays_For NATURAL JOIN Players WHERE Abbreviation="
    sql_command += "'" + team_abbr + "'"
    cursor.execute(sql_command)
    response = cursor.fetchall()

    roster = []

    for r in response:
        roster.append(r)


  

    sql_command = "SELECT Location FROM Teams WHERE Abbreviation="
    sql_command += "'" + team_abbr + "'"
    cursor.execute(sql_command)
    location = cursor.fetchall()[0][0]



    sql_command = "SELECT Name FROM Teams WHERE Abbreviation="
    sql_command += "'" + team_abbr + "'"
    cursor.execute(sql_command)
    name = cursor.fetchall()[0][0]

    sql_command = "SELECT Coach_Name FROM Head_Coaches WHERE Abbreviation="
    sql_command += "'" + team_abbr + "'"
    cursor.execute(sql_command)
    head_coach = cursor.fetchall()[0][0]

    sql_command = "SELECT COUNT(Player) FROM Plays_For NATURAL JOIN Players WHERE Abbreviation="
    sql_command += "'" + team_abbr + "'"
    cursor.execute(sql_command)
    roster_size = cursor.fetchall()[0][0]


    team_formatted = location + " " + name
    sql_command = "SELECT * FROM Schedule WHERE Visitor="
    sql_command += "'" + team_formatted + "'"
    sql_command += " OR Home="
    sql_command += "'" + team_formatted + "' ORDER BY Date DESC LIMIT 5"
    cursor.execute(sql_command)
    past_five_games = cursor.fetchall()




    # r[1] + " " + r[0] + " (" + r[2] + ")"
    full_team_name = location + " " + name + " (" + team_abbr + ")"

    context = {
        "roster": roster,
        "location": location,
        "name": name,
        "full_team_name": full_team_name,
        "abbreviation": team_abbr,
        "head_coach": head_coach,
        "roster_size": roster_size,
        "past_games" : past_five_games
    }


    return render(request,'team.html', context = context)

@csrf_exempt
def team_dashboard(request):
    try:
        user_type = request.session['user_type']
    except:
        return redirect('login')

    if request.method == "GET":
        cursor = connections['nba'].cursor()
        sql_command = "SELECT * From Teams"
        cursor.execute(sql_command)
        response = cursor.fetchall()

        teams = []
        for r in response:
            temp = r[1] + " " + r[0] + " (" + r[2] + ")"
            teams.append(temp)
    
        # print(teams)

        context = {
            "teams": teams
        }

        return render(request, 'team_dashboard.html', context = context)
    else:
        team = request.POST['team_selection']

        open_parenthesis = team.find('(')
        close_parenthesis = team.find(')')
        abbr = team[open_parenthesis+1:close_parenthesis]
        
        return redirect('team', abbr)

@csrf_exempt
def player_dashboard(request):

    try:
        user_type = request.session['user_type']
    except:
        return redirect('login')

    if request.method == "POST":
        name = request.POST.get('player_name')

        cursor = connections['nba'].cursor()
        sql_command = "SELECT * FROM Players NATURAL JOIN Plays_For WHERE Player LIKE "
        sql_command += "'%" + name + "%'"
        cursor.execute(sql_command)
        response = cursor.fetchall()

        col1 = []
        col2 = []
        col3 = []
        col = 1

        for r in response:
            if col == 1:
                col1.append(r)
                col = 2
            elif col == 2:
                col2.append(r)
                col = 3
            else:
                col3.append(r)
                col = 1

        context = {
            "col1": col1,
            "col2": col2,
            "col3": col3,
        }
        return render(request, 'player_search_results.html', context = context)
    else:
        form = AddPlayerForm()
        context = {"form": form}
        return render(request, 'player_dashboard.html', context= context)

def player(request, player_id):

    try:
        user_type = request.session['user_type']
    except:
        return redirect('login')

    cursor = connections['nba'].cursor()
    sql_command = "SELECT * FROM Players NATURAL JOIN Plays_For WHERE Player_ID="
    sql_command += str(player_id)
    cursor.execute(sql_command)
    player_info = cursor.fetchall()[0]

    print("player_info \n", player_info)

    sql_command = "SELECT * FROM Awards NATURAL JOIN Awarded WHERE Player_ID="
    sql_command += str(player_id)
    cursor.execute(sql_command)
    awards = cursor.fetchall()

    print("awards \n", awards)

    if len(awards) == 0:
        awards = (("No Awards Won", player_id)),
    

    sql_command = "SELECT * FROM Stats WHERE Player_ID="
    sql_command += str(player_id)
    cursor.execute(sql_command)
    stats = cursor.fetchall()[0]

    print("stats \n", stats)

    sql_command = "SELECT * FROM Plays_For NATURAL JOIN Teams NATURAL JOIN Head_Coaches WHERE Player_ID="
    sql_command += str(player_id)
    cursor.execute(sql_command)
    team_info = cursor.fetchall()

    print("team_info \n", team_info)


    sql_command = "SELECT * FROM Players NATURAL JOIN Plays_For WHERE Abbreviation = ("
    sql_command += "SELECT Abbreviation FROM Players NATURAL JOIN Plays_For WHERE Player_ID = "
    sql_command += str(player_id)
    sql_command += ")"
    cursor.execute(sql_command)
    team_roster = cursor.fetchall()

    print("team_roster \n", team_roster)




    context = {
        "player_info": player_info[0],
        "awards": awards,
        "stats": stats,
        "team_info": team_info,
        "team_roster": team_roster

    }
    return render(request, 'player.html', context = context)

def game_schedule(request):

    try:
        user_type = request.session['user_type']
    except:
        return redirect('login')

    team = request.GET.get('team_selection')
    cursor = connections['nba'].cursor()

    sql_command = "SELECT * From Teams"
    cursor.execute(sql_command)
    response = cursor.fetchall()

    teams = []
    for r in response:
        temp = r[1] + " " + r[0] + " (" + r[2] + ")"
        teams.append(temp)

    if team == None or team == "all":
        sql_command = "SELECT * FROM Schedule"
        cursor.execute(sql_command)
        schedule = cursor.fetchall()
    else:
        open_parenthesis = team.find('(')
        team_formatted = team[:open_parenthesis-1]

        sql_command = "SELECT * FROM Schedule WHERE Visitor="
        sql_command += "'" + team_formatted + "'"
        sql_command += " OR Home="
        sql_command += "'" + team_formatted + "'"

        cursor.execute(sql_command)
        schedule = cursor.fetchall()

    context = {
        "schedule": schedule,
        "teams": teams,
    }
    return render(request, 'game_schedule.html', context = context)

def login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form} )
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            cursor = connections['nba'].cursor()
            sql_command = "SELECT Password,User_Type FROM Users WHERE Username="
            sql_command += "'" + form.cleaned_data['username'] + "'"
            cursor.execute(sql_command)
            response = cursor.fetchall()
            
            if len(response) <= 0:
                return redirect('login')
            
            password = response[0][0]
            user_type = response[0][1]

            if sha256_crypt.verify(form.cleaned_data['password'], password):
                request.session['username'] = form.cleaned_data['username']
                request.session['user_type'] = user_type
                return redirect('index')
            else:
                return redirect('login')

def logout(request):
    try:
        del request.session['username']
        del request.session['user_type']
    except:
        return redirect('login')
    return redirect('login')

def admin_dashboard(request):
    try:
        user_type = request.session['user_type']
    except:
        return redirect('login')

    if request.session['user_type'] != 'admin':
        return redirect('login')
    cursor = connections['nba'].cursor()
    sql_command = "SELECT table_name FROM information_schema.tables WHERE table_schema ='rk2ea_nba'"
    cursor.execute(sql_command)
    response = cursor.fetchall()

    tables = []
    for r in response:
        tables.append(r[0])
    
    context = {
        "tables": tables,
    }
    return render(request, 'admin_dashboard.html', context = context)

def tables(request, table_name):
    try:
        user_type = request.session['user_type']
    except:
        return redirect('login')

    if request.method == 'GET':
        if request.session['user_type'] != 'admin':
            redirect('login')
    
        cursor = connections['nba'].cursor()
        sql_command = "SELECT * FROM " + table_name
        cursor.execute(sql_command)
        response = cursor.fetchall()

        sql_command = "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='rk2ea_nba' AND `TABLE_NAME`='" + table_name + "'";
        cursor.execute(sql_command)
        columns = cursor.fetchall()
        print(columns)


        form = SQLCommandForm()

        context = {
            "table_name": table_name,
            "table_contents": response,
            "form": form,
            "columns": columns,
            "status": "None"
        }
        return render(request, 'admin_table_view.html', context = context)
    else:
        sql_command = request.POST.get('sql_command')
        print(sql_command)

        cursor = connections['nba'].cursor()
        restricted_commands = ["DROP", "DELETE"]
        for rc in restricted_commands:
            if rc in sql_command:
                form = SQLCommandForm()
                context = {
                    "status": "Failure",
                    "comment": "Cannot Execute Command - Restricted Command",
                    "sql_command": sql_command,
                    "form": form
                }
                return render(request, 'admin_table_view.html', context = context)

        try:
            cursor.execute(sql_command)
            response = cursor.fetchall()
        except:
            form = SQLCommandForm()
            context = {
                    "status": "Failure",
                    "comment": "Could Not Execute Command Successfully",
                    "sql_command": sql_command,
                    "form": form
                }
            return render(request, 'admin_table_view.html', context = context)
        else:
            form = SQLCommandForm()
            context = {
                    "status": "Success",
                    "comment": "Command Executed Successfully",
                    "sql_command": sql_command,
                    "table_contents": response,
                    "form": form
                }
            return render(request, 'admin_table_view.html', context = context)
