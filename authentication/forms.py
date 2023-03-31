from django import forms

class LogInForm(forms.Form):
    username = forms.CharField(max_length=63, label="Nom d'utlisateur")
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Mot de passe")