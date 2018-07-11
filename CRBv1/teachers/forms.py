from django import forms
from accounts.models import *
import datetime
from ranges.models import *
from django.forms import ModelForm
from .choices import *
from django.db import models
from django.utils.translation import gettext_lazy as _
from random import randint
import re

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

    def clean(self):
        cleaned_data = super(RangeForm, self).clean()
        startdate = cleaned_data.get("datestart")
        enddate = cleaned_data.get("dateend")
        timestart = cleaned_data.get("timestart")
        timeend = cleaned_data.get("timeend")

        if startdate is not None or enddate is not None:
            if startdate < datetime.date.today():
                msg = u"Please choose a Start Date starting from today!"
                self._errors["datestart"] = self.error_class([msg])

            if enddate < startdate:
                msg = u"End Date should be after Start Date!"
                self._errors["dateend"] = self.error_class([msg])

            if startdate == enddate:
                if timeend < timestart:
                    msg = u"End Time should be after Start Time for a one day range!"
                    self._errors["timeend"] = self.error_class([msg])
        

        rangeurl = cleaned_data.get("rangeurl")
        if not re.match("^[A-Za-z0-9_-]*$", rangeurl):
            msg = u"Range URL should only contain letters, numbers, dashes or underscore!"
            self._errors["rangeurl"] = self.error_class([msg])

        

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

class ModifyRangeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ModifyRangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ModifyRangeForm, self).clean()
        startdate = cleaned_data.get("datestart")
        enddate = cleaned_data.get("dateend")
        timestart = cleaned_data.get("timestart")
        timeend = cleaned_data.get("timeend")

        if startdate is not None or enddate is not None:
            if startdate < datetime.date.today():
                msg = u"Please choose a Start Date starting from today!"
                self._errors["datestart"] = self.error_class([msg])

            if enddate < startdate:
                msg = u"End Date should be after Start Date!"
                self._errors["dateend"] = self.error_class([msg])

            if startdate == enddate:
                if timeend < timestart:
                    msg = u"End Time should be after Start Time for a one day range!"
                    self._errors["timeend"] = self.error_class([msg])
        
    def save(self, commit=True):
        modifyrange = super().save(commit=False)
        if commit:
            modifyrange.lastmodifieddate = datetime.date.today()
            admin = self.request.user
            modifyrange.lastmodifiedby = User.objects.get(username = admin)
            modifyrange.lastmodifiedtime = datetime.datetime.now().time()
            modifyrange.save()
        return modifyrange

    class Meta:
        model = Range
        fields = ('rangename', 'datestart', 'timestart', 'dateend', 'timeend')

class QuestionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(QuestionForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        usedocker = cleaned_data.get("usedocker")
        registryid = self.request.POST.get('registryid','')
        print(usedocker)
        print(registryid)

        if usedocker == "Yes" and registryid == "":
            msg = u"Please enter the Registry ID!"
            self._errors["registryid"] = self.error_class([msg])

    def save(self, commit=True):
        question = super().save(commit=False)
        topicname = self.request.POST.get('topicname','')
        topicid = QuestionTopic.objects.get(topicname = topicname)
        question.topicid = topicid
        admin = self.request.user
        email = User.objects.get(username = admin)
        question.createdby = email
        question.datecreated = datetime.date.today()
        question.timecreated = datetime.datetime.now().time()

        if commit:
            question.save()
        return question, topicname

    class Meta:
        model = Questions
        fields = ('questiontype', 'title', 'text', 'hint', 'usedocker')

class ModifyQuestionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ModifyQuestionForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(ModifyQuestionForm, self).clean()
        usedocker = cleaned_data.get("usedocker")
        registryid = self.request.POST.get('registryid','')

        if usedocker == "Yes" and registryid == "":
            msg = u"Please enter the Registry ID!"
            self._errors["registryid"] = self.error_class([msg])

    def save(self, commit=True):
        question = super().save(commit=False)
        topicname = self.request.POST.get('topicname',' ')
        topicid = QuestionTopic.objects.get(topicname = topicname)
        question.topicid = topicid
        if commit:
            question.save()
        return question

    class Meta:
        model = Questions
        fields = ('title', 'text', 'hint',)