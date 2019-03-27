from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
# Create your views here.

def index(request):
    cursor = connection.cursor()
    cursor.execute('SELECT Name FROM Teams')
    teams = cursor.fetchall()
    teams_list = []
    for value in teams:
        print(value[0])
        teams_list.append(value[0])
    print(teams_list)
    return HttpResponse(teams_list)