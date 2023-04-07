from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # restrict access to authenticate users
# from django.contrib.auth.mixins import LoginRequiredMixin # restrict access to authenticate users
from django.views.generic import View
from authentication import forms
from django.conf import settings

class LoginPageView(View): # class LoginPageView(View, LoginRequiredMixin): restrict access to authenticate users 
    template_name = "authentication/login.html"
    form_class = forms.LogInForm

    def get(self, request):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            context={"form": form}
        )

    def post(self, request):
        message = ""
        formu = self.form_class(request.POST)
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
            self.template_name,
            context={"form": formu, "message": message}
        )


@login_required # restrict access to authenticate users
def home(request):
    return render(request, "blog/home.html")

def logout_user(request):
    logout(request)
    return redirect("login")

class SignupPageView(View):
    template_name = "authentication/signup.html"
    form_class = forms.SignupForm

    def get(self, request):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            context={"form": form}
        )
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(
            request,
            self.template_name,
            context={"form": form}
        )


