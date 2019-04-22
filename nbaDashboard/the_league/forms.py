from django import forms
class AddPlayerForm(forms.Form):
    number = forms.IntegerField(max_value=100)
    player = forms.CharField(max_length=40)
    position = forms.CharField(max_length=2)
    height = forms.CharField(max_length=5)
    weight = forms.IntegerField(max_value=450)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget = forms.PasswordInput())

class SQLCommandForm(forms.Form):
    sql_command = forms.CharField(widget = forms.Textarea(attrs={'rows': 4, 'columns': 20}))
