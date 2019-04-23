from django import forms

class AddPlayerForm(forms.Form):
    choices = (
        ('ATL', 'Atlanta Hawks'),
        ('BKN', 'Brooklyn Nets'),
        ('BOS', 'Boston Celtics'),
        ('CHA', 'Charlotte Hornets'),
        ('CHI', 'Chicago Bulls'),
        ('CLE', 'Cleveland Cavaliers'),
        ('DAL', 'Dallas Mavericks'),
        ('DEN', 'Denver Nuggets'),
        ('DET', 'Detroit Pistons'),
        ('GSW', 'Golden State Warriors'),
        ('HOU', 'Houston Rockets'),
        ('IND', 'Indiana Pacers'),
        ('LAC', 'Los Angeles Clippers'),
        ('LAL', 'Los Angeles Lakers'),
        ('MEM', 'Memphis Grizzlies'),
        ('MIA', 'Miami Heat'),
        ('MIL', 'Milwaukee Bucks'),
        ('MIN', 'Minnesota Timberwolves'),
        ('NOP', 'New Orleans Pelicans'),
        ('NYK', 'New York Knicks'),
        ('OKC', 'Oklahoma City Thunder'),
        ('ORL', 'Orlando Magic'),
        ('PHI', 'Philadelphia 76ers'),
        ('PHX', 'Phoenix Suns'),
        ('POR', 'Portland Trailblazers'),
        ('SAC', 'Sacramento Kings'),
        ('SAS', 'San Antonio Spurs'),
        ('TOR', 'Toronto Raptors'),
        ('UTA', 'Utah Jazz'),
        ('WAS', 'Washington Wizards'),

    )
    number = forms.IntegerField(max_value=100)
    player = forms.CharField(max_length=40)
    position = forms.CharField(max_length=2)
    height = forms.CharField(max_length=5)
    weight = forms.IntegerField(max_value=450)
    team = forms.ChoiceField(choices=choices)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget = forms.PasswordInput())

class SQLCommandForm(forms.Form):
    sql_command = forms.CharField(widget = forms.Textarea(attrs={'rows': 4, 'columns': 20}))
