from django import forms
from accounts.models import *
import datetime
from SDL.models import *
from django.forms import ModelForm

from django.db import models
from random import randint

from django.utils.translation import gettext_lazy as _
from tinymce import TinyMCE

class SDLAddPostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SDLAddPostForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SDLAddPostForm, self).clean()

    def save(self, commit=True):
        post = super().save(commit=False)
        admin = self.request.user
        email = User.objects.get(username=admin)

        post.createdby = email
        post.datecreated = datetime.date.today()
        post.timecreated = datetime.datetime.now().time()

        if commit:
            post.save()
        return post

    class Meta:
        model = SDLPost
        fields = ('title', 'text', 'postactive', 'postid')

class PostModifyModelForm(forms.ModelForm):

    class Meta:
        model = SDLPost
        fields = ('title', 'text', 'postactive', 'postid')

class PostModifyForm(PostModifyModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(PostModifyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.lastmodifieddate = datetime.date.today()
            post.lastmodifiedtime = datetime.datetime.now().time()
            post.save()
        return post

    class Meta:
        model = SDLPost
        fields = ('title', 'text', 'postactive',)

class SDLPostComment(ModelForm):
    comment = forms.CharField(label='comment', max_length=256,
                                  widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(SDLPostComment, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(SDLPostComment, self).clean()

    def save(self, postinstance, user, commit=True):
        comment = super().save(commit=False)
        comment.postid = postinstance
        comment.commenter = user
        comment.dateposted = datetime.date.today()
        comment.timeposted = datetime.datetime.now().time()

        if commit:
            comment.save()
        return comment

    class Meta:
        model = SDLComment
        fields = ('comment', )