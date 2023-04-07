from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # restrict access to authenticate users use it only with def view
from django.contrib.auth.mixins import LoginRequiredMixin # restrict access to authenticate users use it only with class view
from django.views.generic import View
from authentication import forms
from django.conf import settings

class LoginPageView(View): # class LoginPageView(View, LoginRequiredMixin): restrict access to authenticate users in class view
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

@login_required # works only with def view
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
    
class UploadProfilePhotoPageView(View, LoginRequiredMixin):
    template_name = "authentication/upload_profile_photo.html"
    form_class = forms.UploadProfilePhotoForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(
            request,
            self.template_name,
            context={"form": form}
        )

    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(
            request,
            self.template_name,
            context={"form": form}
        )