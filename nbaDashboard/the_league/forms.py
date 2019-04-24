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
    number = forms.IntegerField(max_value=100, widget=forms.TextInput(attrs={'placeholder': 'Player Number', 'class': 'identifier'}))
    player = forms.CharField(max_length=40, widget=forms.TextInput(attrs={'placeholder': 'Player Name', 'class': 'identifier'}))
    position = forms.CharField(max_length=2, widget=forms.TextInput(attrs={'placeholder': 'Position', 'class': 'identifier'}))
    height = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'placeholder': 'Height', 'class': 'identifier'}))
    weight = forms.IntegerField(max_value=450, widget=forms.TextInput(attrs={'placeholder': 'Weight', 'class': 'identifier'}))
    team = forms.ChoiceField(choices=choices, widget = forms.Select(attrs={'class': 'identifier'}))
    ppg = forms.DecimalField(max_value=100, widget=forms.TextInput(attrs={'placeholder': 'Points Per Game', 'class': 'identifier'}))
    rpg = forms.DecimalField(max_value=100, widget=forms.TextInput(attrs={'placeholder': 'Rebounds Per Game', 'class': 'identifier'}))
    apg = forms.DecimalField(max_value=100, widget=forms.TextInput(attrs={'placeholder': 'Assists Per Game', 'class': 'identifier'}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)  
    password = forms.CharField(max_length=100, widget = forms.PasswordInput())

class SQLCommandForm(forms.Form):
    sql_command = forms.CharField(widget = forms.Textarea(attrs={'rows': 4, 'columns': 20}))
