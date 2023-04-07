from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class LogInForm(forms.Form):
    username = forms.CharField(max_length=63, label="Nom d'utlisateur")
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label="Mot de passe")

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model() # get User class define in models.py
        fields = ('username', 'email', 'first_name', 'last_name', 'role')