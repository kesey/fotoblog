"""fotoblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView # generic view, allows you to do without the view
import authentication.views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', LoginView.as_view(
    #     template_name="authentication/login.html",
    #     redirect_authenticated_user=True
    # ), name="login"), # generic view, allows you to do without the view
    # path('logout/', LogoutView.as_view(), name="logout"), # generic view, allows you to do without the view
    path('change-password/', PasswordChangeView.as_view(
        template_name="authentication/change_password.html",
    ), name="password_change"), # generic view, allows you to do without the view
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name="authentication/change_password_done.html",
    ), name="password_change_done"), # generic view, allows you to do without the view
    path('', authentication.views.LoginPageView.as_view(), name="login"),
    path('logout/', authentication.views.logout_user, name="logout"),
    path('home/', authentication.views.home, name="home")
]
