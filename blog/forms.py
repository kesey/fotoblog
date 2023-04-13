from django import forms
from blog import models
from django.contrib.auth import get_user_model

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ('image', 'caption')

class BlogForm(forms.ModelForm):
    edit_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True) # add input type hidden to identify form

    class Meta:
        model = models.Blog
        fields = ('title', 'content')

class DeleteBlogForm(forms.Form):
    delete_blog = forms.BooleanField(widget=forms.HiddenInput, initial=True) # add input type hidden to identify form

class FollowUsersForm(forms.ModelForm):
    class Meta:
        model = get_user_model() # get User class define in models.py
        fields = ('follows', )