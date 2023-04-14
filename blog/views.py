from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from blog import forms, models
from django.conf import settings
from django.contrib.auth.decorators import login_required # restrict access to authenticate users use it only with def view
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin # LoginRequiredMixin restrict access to authenticate users, use it only with class view # PermissionRequiredMixin restrict access to users with permissions
from django.forms import formset_factory
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator

@login_required # restrict access to authenticate users in def view
def home(request):
    blogs = models.Blog.objects.filter(
        Q(contributors__in=request.user.follows.all()) | # get blogs whose contributors are followed by the user or starred
        Q(starred=True) # with Q you can add logic operand or: | and: & not: ~ to combine conditions
    )
    photos = models.Photo.objects.filter(
        uploader__in=request.user.follows.all() # get photos whose author are followed by the user
    ).exclude(
        blog__in=blogs # but not already display in blog list
    )

    photos_and_blogs = sorted(chain(blogs, photos), key= lambda instance: instance.date_created, reverse=True) # combine the two QuerySet and sort them by date of creation (begin with the most recent)

    paginator = Paginator(photos_and_blogs, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "blog/home.html",
        context={"page": page}
    )

@login_required
def photo_feed(request):
    photos = models.Photo.objects.filter(uploader__in=request.user.follows.all()).order_by("-date_created")

    paginator = Paginator(photos, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(
        request,
        "blog/photo_feed.html",
        context={"page": page}
    )

class PhotoUploadPageView(LoginRequiredMixin, PermissionRequiredMixin, View): # LoginRequiredMixin restrict access to authenticate users in class view, have to be in first position
    permission_required = ("blog.add_photo", ) # you can set multiple permissions with a tuple
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

class BlogAndPhotoUploadPageView(LoginRequiredMixin, PermissionRequiredMixin, View): # mixin first (important)
    permission_required = ("blog.add_photo", "blog.add_blog")
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
            blog.photo = photo
            blog.save() # You can save relations in the ManyToManyField ONCE the model has been saved in database.
            blog.contributors.add(request.user, through_defaults={"contributions": "Auteur principal"})
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

class EditBlogPageView(LoginRequiredMixin, PermissionRequiredMixin, View): # mixin first (important)
    permission_required = ("blog.change_blog", )
    template_name = "blog/edit_blog.html"
    blog_form_class = forms.BlogForm
    delete_blog_form_class = forms.DeleteBlogForm

    def get(self, request, **kwargs): # use **kwargs to get url parameters
        blog = get_object_or_404(models.Blog, id=kwargs["blog_id"])
        edit_form = self.blog_form_class(instance=blog)
        delete_form = self.delete_blog_form_class()
        return render(
            request,
            self.template_name,
            context={"edit_form": edit_form, "delete_form": delete_form}
        )
    
    def post(self, request, **kwargs): # use **kwargs to get url parameters
        blog = get_object_or_404(models.Blog, id=kwargs["blog_id"])
        edit_form = self.blog_form_class(instance=blog)
        delete_form = self.delete_blog_form_class()
        if "edit_blog" in request.POST:
            edit_form = self.blog_form_class(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("home")
        if "delete_blog" in request.POST:
            delete_form = self.delete_blog_form_class(request.POST)
            if delete_form.is_valid():
                blog.delete()
                return redirect("home")

        return render(
            request,
            self.template_name,
            context={"edit_form": edit_form, "delete_form": delete_form}
        )

class CreateMultiplePhotoPageView(LoginRequiredMixin, PermissionRequiredMixin, View): # mixin first (important)
    permission_required = ("blog.add_photo")
    template_name = "blog/create_multiple_photos.html"
    photo_form_class = formset_factory(forms.PhotoForm, extra=5)
    
    def get(self, request):
        formset = self.photo_form_class()
        return render(
            request,
            self.template_name,
            context={"formset": formset}
        )
    
    def post(self, request):
        formset = self.photo_form_class(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect("home")
        
        return render(
            request,
            self.template_name,
            context={"formset": formset}
        )

class FollowUserPageView(LoginRequiredMixin, View):
    template_name = "blog/follow_user.html"
    follow_user_form_class = forms.FollowUsersForm

    def get(self, request):
        form = self.follow_user_form_class(instance=request.user)
        return render(
            request,
            self.template_name,
            context={"form": form}
        )
    
    def post(self, request):
        form = self.follow_user_form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
        
        return render(
            request,
            self.template_name,
            context={"form": form}
        )