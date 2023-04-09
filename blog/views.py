from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from blog import forms, models
from django.conf import settings
from django.contrib.auth.decorators import login_required # restrict access to authenticate users use it only with def view
from django.contrib.auth.mixins import LoginRequiredMixin # restrict access to authenticate users use it only with class view

@login_required # restrict access to authenticate users in def view
def home(request):
    photos = models.Photo.objects.all()
    blogs = models.Blog.objects.all()
    return render(
        request,
        "blog/home.html",
        context={"photos": photos, "blogs": blogs}
    )

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

class BlogAndPhotoUploadPageView(View, LoginRequiredMixin):
    template_name = "blog/create_blog_post.html"
    blog_form_class = forms.BlogForm
    photo_form_class = forms.PhotoForm

    def get(self, request):
        blog_form = self.blog_form_class()
        photo_form = self.photo_form_class()
        return render(
            request,
            self.template_name,
            context={"blog_form": blog_form, "photo_form": photo_form} 
        )
    
    def post(self, request):
        blog_form = self.blog_form_class(request.POST)
        photo_form = self.photo_form_class(request.POST, request.FILES)
        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            blog.save()
            return redirect('home')
        return render(
            request,
            self.template_name,
            context={"blog_form": blog_form, "photo_form": photo_form}
        )

@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(
        request,
        "blog/view_blog.html",
        context={"blog": blog}
    )