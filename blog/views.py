from django.shortcuts import render, redirect
from django.views.generic import View
from blog import forms, models
from django.conf import settings
from django.contrib.auth.decorators import login_required # restrict access to authenticate users use it only with def view
from django.contrib.auth.mixins import LoginRequiredMixin # restrict access to authenticate users use it only with class view

class PhotoUploadPageView(View, LoginRequiredMixin): # LoginRequiredMixin restrict access to authenticate users in class view
    template_name = "blog/photo_upload.html"
    form_class = forms.PhotoForm

    def get(self, request):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            context={"form": form}
        )

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False) # commit=False doesn't save but return a photo object
            photo.uploader = request.user # set the uploader to the user before saving the model
            photo.save() # now you can save
            return redirect('home')
        return render(
            request,
            self.template_name,
            context={"form": form}
        )
    
@login_required # restrict access to authenticate users in def view
def home(request):
    photos = models.Photo.objects.all()
    return render(
        request,
        "blog/home.html",
        context={"photos": photos}
    )