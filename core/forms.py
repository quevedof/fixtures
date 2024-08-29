from django import forms

# to collect the input of the club name
class clubForm(forms.Form):
    club_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Barcelona', 'id':'clubName'}), max_length=50, required=True)


# to collect the input of the player name
class playerForm(forms.Form):
    player_name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Alcaraz', 'id':'playerName'}), max_length=50, required=True)
