from django import forms
from accounts.models import *
import datetime
from ranges.models import *
from django.forms import ModelForm
from .choices import *
from django.db import models
from django.utils.translation import gettext_lazy as _
from random import randint

class AddGroup(ModelForm):
    groupname = forms.CharField(label = "Group Name", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    class Meta:
        model = Group
        fields = ('groupname',)

class AddGroupCommit(AddGroup):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddGroupCommit, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        group = super().save(commit=False)
        group.datecreated = datetime.date.today()
        group.timecreated = datetime.datetime.now().time()
        group.grouppoints = 0
        admin = self.request.user
        group.createdby = User.objects.get(username = admin)

        if commit:
            group.save()
        return group
    
    class Meta:
        model = Group
        fields = ('groupname',)

class RangeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(RangeForm, self).__init__(*args, **kwargs)

    # rangename = forms.CharField(label = "Range Name", required = True, widget=forms.TextInput(attrs={'required':'true'}))
    # rangeurl = forms.CharField(label = "Range URL", required = True)
    # datestart = forms.DateField(label = "Date Start", required=False, widget=forms.SelectDateWidget)
    # timestart = forms.TimeField(label = "Time Start", required=False)
    # dateend = forms.DateField(label = "Date End", required=False, widget=forms.SelectDateWidget)
    # timeend = forms.TimeField(label = "Time End", required=False)

    def save(self, commit=True):
        createdrange = super().save(commit=False)
        createdrange.datecreated = datetime.date.today()
        createdrange.rangecode = randint(10 ** (6 - 1), (10 ** (6) - 1))
        admin = self.request.user
        email = User.objects.get(username = admin)
        createdrange.createdbyusername = email

        if commit:
            createdrange.save()
        return createdrange

    class Meta:
        model = Range
        fields = ('rangename', 'maxscore', 'rangeurl', 'datestart', 'timestart', 'dateend', 'timeend')

class QuestionForm(ModelForm):
    questiontype = forms.ChoiceField(choices=QUESTION_TYPE_CHOICES, required=True, widget=forms.Select(choices=QUESTION_TYPE_CHOICES))
    topicname = forms.CharField(required = False)
    title = forms.CharField(required = True, widget=forms.TextInput(attrs={'required':'true'}))
    text = forms.CharField(required=True, widget=forms.TextInput(attrs={'required': 'true'}))
    answer = forms.CharField(required=True, widget=forms.TextInput(attrs={'required': 'true'}))
    hint = forms.CharField(required=True, widget=forms.TextInput(attrs={'required': 'true'}))
    marks = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'required': 'true'}))
    optionone = forms.CharField(required=False)
    optiontwo = forms.CharField(required=False)
    optionthree = forms.CharField(required=False)
    optionfour = forms.CharField(required=False)

    class Meta:
        model = Questions
        fields = ('questiontype', 'title', 'text', 'answer', 'hint', 'marks')