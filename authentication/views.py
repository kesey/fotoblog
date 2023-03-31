from django.shortcuts import render
from django.contrib.auth import authenticate, login
from authentication import forms

def login_page(request):
    formu = forms.LogInForm()
    message = ""
    if request.method == "POST":
        formu = forms.LogInForm(request.POST)
        if formu.is_valid():
            user = authenticate(username=formu.cleaned_data["username"], password=formu.cleaned_data["password"])
            if user is not None:
                login(request, user)
                message = f"Bonjour {user.username}, Vous êtes connecté."
            else:
                message = "Identifiants invalides."
    return render(
            request,
            "authentication/login.html",
            context={"formu": formu, "message": message}
        )