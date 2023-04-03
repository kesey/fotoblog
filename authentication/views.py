from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from authentication import forms

@login_required
def home(request):
    return render(request, "blog/home.html")

def logout_user(request):
    logout(request)
    return redirect("login")

def login_page(request):
    formu = forms.LogInForm()
    message = ""
    if request.method == "POST":
        formu = forms.LogInForm(request.POST)
        if formu.is_valid():
            user = authenticate(
                username=formu.cleaned_data["username"], 
                password=formu.cleaned_data["password"]
            )
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                message = "Identifiants invalides."
    return render(
        request,
        "authentication/login.html",
        context={"formu": formu, "message": message}
    )