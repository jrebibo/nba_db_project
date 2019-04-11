from django import forms
class AddPlayerForm(forms.Form):
    number = forms.IntegerField(max_value=100)
    player = forms.CharField(max_length=40)
    position = forms.CharField(max_length=2)
    height = forms.CharField(max_length=5)
    weight = forms.IntegerField(max_value=450)
