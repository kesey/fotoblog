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
import blog.views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', authentication.views.SignupPageView.as_view(), name="signup"),
    path('', authentication.views.LoginPageView.as_view(), name="login"),
    path('logout/', authentication.views.logout_user, name="logout"),
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
    path('profile-photo/upload/', authentication.views.UploadProfilePhotoPageView.as_view(), name="upload_profile_photo"),
    path('home/', blog.views.home, name="home"),
    path('photo/upload/', blog.views.PhotoUploadPageView.as_view(), name="photo_upload"),
    path('blog/create/', blog.views.BlogAndPhotoUploadPageView.as_view(), name="blog_create"),
    path('blog/<int:blog_id>', blog.views.view_blog, name="view_blog")
]

if settings.DEBUG: # serve media in dev environnement (don't use this in production)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)