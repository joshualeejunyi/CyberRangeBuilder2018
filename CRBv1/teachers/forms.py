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
from tinymce import TinyMCE
from teachers import views as teachersview

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

        self.startdate = startdate
        self.enddate = enddate
        self.timestart = timestart
        self.timeend = timeend


        if startdate is not None and enddate is not None:
            if enddate < startdate:
                msg = u"End Date should be after Start Date!"
                self._errors["dateend"] = self.error_class([msg])

            if startdate == enddate:
                if timeend < timestart:
                    msg = u"End Time should be after Start Time for a one day range!"
                    self._errors["timeend"] = self.error_class([msg])
        
        if startdate is None and enddate is not None:
            msg = u"Please enter a Start Date!"
            self._errors["datestart"] = self.error_class([msg])

        if startdate is not None and enddate is None:
            msg = u"Please enter a End Date!"
            self._errors["dateend"] = self.error_class([msg])

        if timestart is None and timeend is not None:
            msg = u"Please enter a Start Time!"
            self._errors["timestart"] = self.error_class([msg])
        
        if timeend is None and timestart is not None:
            msg = u"Please enter a End Time!"
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

        if self.startdate is not None and self.enddate is not None:
            if self.timestart is None and self.timeend is None:
                createdrange.timestart = '08:30:AM'
                createdrange.timeend = '11:59:PM'

        if commit:
            createdrange.save()
        return createdrange

    class Meta:
        model = Range
        fields = ('rangename', 'maxscore', 'rangeurl', 'datestart', 'timestart', 'dateend', 'timeend', 'attempts', 'rangeinfo')

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

        self.startdate = startdate
        self.enddate = enddate
        self.timestart = timestart
        self.timeend = timeend

        if startdate is not None or enddate is not None:
            if enddate < startdate:
                msg = u"End Date should be after Start Date!"
                self._errors["dateend"] = self.error_class([msg])

            if startdate == enddate:
                if timeend < timestart:
                    msg = u"End Time should be after Start Time for a one day range!"
                    self._errors["timeend"] = self.error_class([msg])
                    

        if timestart is None and timeend is not None:
            msg = u"Please enter a Start Time!"
            self._errors["timestart"] = self.error_class([msg])
        
        if timeend is None and timestart is not None:
            msg = u"Please enter a End Time!"
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
        fields = ('rangename', 'datestart', 'timestart', 'dateend', 'timeend', 'attempts', 'rangeinfo')
        
class QuestionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.rangeinstance = kwargs.pop("rangeinstance")
        super(QuestionForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        usedocker = cleaned_data.get('usedocker')
        imagename = cleaned_data.get('registryid')
        registryid = self.request.POST.get('registryid','')
        points = cleaned_data.get('points')
        hintpenalty = cleaned_data.get('hintpenalty')
        

        if usedocker is True and registryid == "":
            msg = u"Please enter the Registry Image Name!"
            self._errors["usedocker"] = self.error_class([msg])
        
        if hintpenalty is not None or points is not None:
            if int(hintpenalty) > int(points):
                msg = u"Hint Penalty should not be more than Points awarded!"
                self._errors["hintpenalty"] = self.error_class([msg])

        

    def save(self, commit=True):
        question = super().save(commit=False)
        registryid = self.request.POST.get('registryid','')
        topicname = self.request.POST.get('topicname','')
        topicid = QuestionTopic.objects.get(topicname = topicname)
        question.topicid = topicid
        admin = self.request.user
        email = User.objects.get(username = admin)
        question.createdby = email
        question.datecreated = datetime.date.today()
        question.timecreated = datetime.datetime.now().time()
        question.registryid = registryid
        rangeid = self.rangeinstance.rangeid
        question.rangeid = self.rangeinstance

        if commit:
            question.save()
        return question, topicname

    class Meta:
        model = Questions
        fields = ('questiontype', 'title', 'text', 'hint', 'hintpenalty', 'answer', 'usedocker', 'points',)

class ModifyQuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.rangeurl = kwargs.pop("rangeurl")
        self.questionid = kwargs.pop("questionid")
        super(ModifyQuestionForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(ModifyQuestionForm, self).clean()
        usedocker = cleaned_data.get('usedocker')
        imagename = cleaned_data.get('registryid')
        registryid = self.request.POST.get('registryid','')
        points = cleaned_data.get('points')
        hintpenalty = cleaned_data.get('hintpenalty')
        
        self.usedocker = usedocker

        if usedocker is True and registryid == "":
            msg = u"Please enter the Registry Image Name!"
            self._errors["usedocker"] = self.error_class([msg])
        
        if hintpenalty is not None or points is not None:
            if int(hintpenalty) > int(points):
                msg = u"Hint Penalty should not be more than Points awarded!"
                self._errors["hintpenalty"] = self.error_class([msg])


    def save(self, commit=True):
        question = super().save(commit=False)
        topicname = self.request.POST.get('topicname',' ')
        registryid = self.request.POST.get('registryid','')
        topicid = QuestionTopic.objects.get(topicname = topicname)
        question.topicid = topicid
        print('------------')
        print(self.usedocker)

        if self.usedocker is True:
            question.registryid = registryid
            imageid = registryid
            print(imageid)
            error = teachersview.CreateImage.get(self, self.request, self.rangeurl, self.questionid, imageid)
            if error is not 0:
                return HttpResponse('ERROR')

        if commit:
            question.save()
        return question

    class Meta:
        model = Questions
        fields = ('title', 'text', 'hint', 'hintpenalty', 'answer', 'usedocker', 'points',)



class ClassForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ClassForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        newclass = super().save(commit=False)
        course = self.request.POST.get('course')
        time = self.request.POST.get('time')
        yearsem = self.request.POST.get('yearsem')
        classnumber = self.request.POST.get('classnumber')
        fullclass = course+'/'+time+'/'+yearsem+'/'+classnumber
        newclass.userclass = fullclass
        if commit:
            newclass.save()
        return newclass

    class Meta:
        model = UserClass
        fields = ()