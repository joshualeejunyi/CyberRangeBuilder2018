# teachers forms.py will store all the forms that will be processed. 

# imports
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

# AddGroup form 
class AddGroup(ModelForm):
    groupname = forms.CharField(label = "Group Name", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    class Meta:
        model = Group
        fields = ('groupname',)

# AddGroupCommit form
class AddGroupCommit(AddGroup):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddGroupCommit, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AddGroupCommit, self).clean()
        # get the groupname
        groupname = cleaned_data.get("groupname")
        # use regex to check the groupname
        # criteria:
        # only letters, numbers, underscore and dashes
        if not re.match("^[A-Za-z0-9_-]*$", groupname):
            # set the message
            msg = u"Group Name should only contain letters, numbers, dashes or underscore!"
            self._errors["groupname"] = self.error_class([msg])
            
    def save(self, commit=True):
        group = super().save(commit=False)
        # set the datecreated to today
        group.datecreated = datetime.date.today()
        # set the time created to now
        group.timecreated = datetime.datetime.now().time()
        # set the grouppoints to 0
        group.grouppoints = 0
        # get the current user (teacher)
        admin = self.request.user
        # set the current user to createdby
        group.createdby = User.objects.get(username = admin)

        if commit:
            group.save()
        return group
    
    class Meta:
        model = Group
        fields = ('groupname',)

# RangeForm
# Create the range
class RangeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(RangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RangeForm, self).clean()
        # get all the relevant values
        startdate = cleaned_data.get("datestart")
        enddate = cleaned_data.get("dateend")
        timestart = cleaned_data.get("timestart")
        timeend = cleaned_data.get("timeend")

        self.startdate = startdate
        self.enddate = enddate
        self.timestart = timestart
        self.timeend = timeend

        # check if the start and end date is not None
        if startdate is not None and enddate is not None:
            # check if the endate is before the start date
            if enddate < startdate:
                # set the error message
                msg = u"End Date should be after Start Date!"
                self._errors["dateend"] = self.error_class([msg])

            # check if the range is a one day range
            if startdate == enddate:
                # check if the start and end time is not none
                if timeend is not None or timestart is not None:
                    # check if the time end if before the time start
                    if timeend < timestart:
                        # set the error message
                        msg = u"End Time should be after Start Time for a one day range!"
                        self._errors["timeend"] = self.error_class([msg])
        
        # check if the start date is left blank
        if startdate is None and enddate is not None:
            # set the error message
            msg = u"Please enter a Start Date!"
            self._errors["datestart"] = self.error_class([msg])

        # check if the end date is left blank
        if startdate is not None and enddate is None:
            # set the error message
            msg = u"Please enter a End Date!"
            self._errors["dateend"] = self.error_class([msg])

        # check if the start time is left blank
        if timestart is None and timeend is not None:
            # set the error message
            msg = u"Please enter a Start Time!"
            self._errors["timestart"] = self.error_class([msg])
        
        # check if the end time is left blank
        if timeend is None and timestart is not None:
            # set the error message
            msg = u"Please enter a End Time!"
            self._errors["timeend"] = self.error_class([msg])

        # get the rangeurl input
        rangeurl = cleaned_data.get("rangeurl")
        # use regex to check the rangeurl
        # criteria:
        # only letters, numbers, underscore and dashes
        if not re.match("^[A-Za-z0-9_-]*$", rangeurl):
            # set the error message
            msg = u"Range URL should only contain letters, numbers, dashes or underscore!"
            self._errors["rangeurl"] = self.error_class([msg])

    def save(self, commit=True):
        createdrange = super().save(commit=False)
        # get today's date and set the datecreated to today
        createdrange.datecreated = datetime.date.today()
        # generate a 6 number random code and set the rangecode as it
        createdrange.rangecode = randint(10 ** (6 - 1), (10 ** (6) - 1))
        # get the current user (teacher)
        admin = self.request.user
        # get the current user's email
        email = User.objects.get(username = admin)
        # set the created by to the user's email
        createdrange.createdby = email

        # check if the start date and end date is not None
        if self.startdate is not None and self.enddate is not None:
            # check if the timestart and timeend is None
            if self.timestart is None and self.timeend is None:
                # set the default values
                # timestart at 0830
                createdrange.timestart = '08:30:AM'
                # time end at 2359
                createdrange.timeend = '11:59:PM'

        if commit:
            createdrange.save()
        return createdrange

    class Meta:
        model = Range
        fields = ('rangename', 'maxscore', 'rangeurl', 'datestart', 'timestart', 'dateend', 'timeend', 'attempts', 'rangeinfo')

# ModifyRangeForm
# modifies the range
class ModifyRangeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ModifyRangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ModifyRangeForm, self).clean()
        # get all the relevant values
        startdate = cleaned_data.get("datestart")
        enddate = cleaned_data.get("dateend")
        timestart = cleaned_data.get("timestart")
        timeend = cleaned_data.get("timeend")

        self.startdate = startdate
        self.enddate = enddate
        self.timestart = timestart
        self.timeend = timeend

        # check if the start and end date is not None
        if startdate is not None and enddate is not None:
            # check if the endate is before the start date
            if enddate < startdate:
                # set the error message
                msg = u"End Date should be after Start Date!"
                self._errors["dateend"] = self.error_class([msg])

            # check if the range is a one day range
            if startdate == enddate:
                # check if the start and end time is not none
                if timeend is not None or timestart is not None:
                    # check if the time end if before the time start
                    if timeend < timestart:
                        # set the error message
                        msg = u"End Time should be after Start Time for a one day range!"
                        self._errors["timeend"] = self.error_class([msg])
        
        # check if the start date is left blank
        if startdate is None and enddate is not None:
            # set the error message
            msg = u"Please enter a Start Date!"
            self._errors["datestart"] = self.error_class([msg])

        # check if the end date is left blank
        if startdate is not None and enddate is None:
            # set the error message
            msg = u"Please enter a End Date!"
            self._errors["dateend"] = self.error_class([msg])

        # check if the start time is left blank
        if timestart is None and timeend is not None:
            # set the error message
            msg = u"Please enter a Start Time!"
            self._errors["timestart"] = self.error_class([msg])
        
        # check if the end time is left blank
        if timeend is None and timestart is not None:
            # set the error message
            msg = u"Please enter a End Time!"
            self._errors["timeend"] = self.error_class([msg])

        
    def save(self, commit=True):
        modifyrange = super().save(commit=False)
        
        if commit:
            # set the lastmodified date to today
            modifyrange.lastmodifieddate = datetime.date.today()
            # get the current user
            admin = self.request.user
            # set the lastmodified by to the user
            modifyrange.lastmodifiedby = User.objects.get(username = admin)
            # set the last modified time to now
            modifyrange.lastmodifiedtime = datetime.datetime.now().time()
            
            # check if the start date and end date is not None
        if self.startdate is not None and self.enddate is not None:
            # check if the timestart and timeend is None
            if self.timestart is None and self.timeend is None:
                # set the default values
                # timestart at 0830
                modifyrange.timestart = '08:30:AM'
                # time end at 2359
                modifyrange.timeend = '11:59:PM'
            # save the object
            modifyrange.save()
        return modifyrange

    class Meta:
        model = Range
        fields = ('rangename', 'datestart', 'timestart', 'dateend', 'timeend', 'attempts', 'rangeinfo')

# QuestionForm
# creates the question
class QuestionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        # get the rangeinstance from kwargs
        self.rangeinstance = kwargs.pop("rangeinstance")
        super(QuestionForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(QuestionForm, self).clean()
        # get the relevant values
        usedocker = cleaned_data.get('usedocker')
        imagename = cleaned_data.get('registryid')
        registryid = self.request.POST.get('registryid','')
        points = cleaned_data.get('points')
        hintpenalty = cleaned_data.get('hintpenalty')
        
        # check if the user left the registry id blank
        if usedocker is True and registryid == "":
            # set the error message
            msg = u"Please enter the Registry Image Name!"
            self._errors["usedocker"] = self.error_class([msg])
        
        if hintpenalty is None:
            hintpenalty = 0
        
        if points is None:
            points = 0
        # check if the hintpenalty or points is not None
        if hintpenalty is not None or points is not None:
            # check if the hint penalty is more than points (cause it shouldn't be)
            if int(hintpenalty) > int(points):
                # set the error message
                msg = u"Hint Penalty should not be more than Points awarded!"
                self._errors["hintpenalty"] = self.error_class([msg])

    def save(self, commit=True):
        question = super().save(commit=False)
        # get the relevant values
        registryid = self.request.POST.get('registryid','')
        topicname = self.request.POST.get('topicname','')
        # get the topicid
        topicid = QuestionTopic.objects.get(topicname = topicname)
        # set the topicid 
        question.topicid = topicid
        # get the current user (teacher)
        admin = self.request.user
        # get the email using the username
        email = User.objects.get(username = admin)
        # set the created by the email
        question.createdby = email
        # set the date created to today
        question.datecreated = datetime.date.today()
        # set the time created to now
        question.timecreated = datetime.datetime.now().time()
        # set the registryid to registryid
        question.registryid = registryid
        # get the rangeid 
        rangeid = self.rangeinstance.rangeid
        # set the rangeid in the question
        question.rangeid = self.rangeinstance

        if commit:
            question.save()
        return question, topicname

    class Meta:
        model = Questions
        fields = ('questiontype', 'title', 'text', 'hint', 'hintpenalty', 'answer', 'usedocker', 'points',)

# ModifyRangeQuestionForm
# Edits the question in the range view only
class ModifyRangeQuestionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.rangeurl = kwargs.pop("rangeurl")
        super(ModifyRangeQuestionForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(ModifyRangeQuestionForm, self).clean()
        # get the relevant values
        usedocker = cleaned_data.get('usedocker')
        imagename = cleaned_data.get('registryid')
        registryid = self.request.POST.get('registryid','')
        points = cleaned_data.get('points')
        hintpenalty = cleaned_data.get('hintpenalty')
        # set the self.usedocker for save function
        self.usedocker = usedocker

        # check if the question uses docker and registry is left blank 
        if usedocker is True and registryid == "":
            # set the error message
            msg = u"Please enter the Registry Image Name!"
            self._errors["usedocker"] = self.error_class([msg])
        
         # check if the hintpenalty or points is not None
        if hintpenalty is not None or points is not None:
            # check if the hint penalty is more than points (cause it shouldn't be)
            if int(hintpenalty) > int(points):
                # set the error message
                msg = u"Hint Penalty should not be more than Points awarded!"
                self._errors["hintpenalty"] = self.error_class([msg])


    def save(self, commit=True):
        question = super().save(commit=False)
        # get the relevant values
        topicname = self.request.POST.get('topicname',' ')
        registryid = self.request.POST.get('registryid','')
        # get the topic id
        topicid = QuestionTopic.objects.get(topicname = topicname)
        # set the topicid
        question.topicid = topicid
        # get the remarks
        remarks = self.request.POST.get('remarks','')
        # set the remarks
        question.remarks = remarks

        # check if the question uses docker
        if self.usedocker is True:
            # set the registryid
            question.registryid = registryid
            imageid = registryid
            # call the CreateImage() View to create the image
            error = teachersview.CreateImage.get(self, self.request, self.rangeurl, self.questionid, imageid)
            # check if no error
            if error is not 0:
                # if got error, response
                return HttpResponse('ERROR')

        if commit:
            question.save()
        return question

    class Meta:
        model = Questions
        fields = ('title', 'text', 'hint', 'hintpenalty', 'answer', 'usedocker', 'points',)

# ModifyQuestionForm
# edits the question from the question management only
class ModifyQuestionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        self.questionid = kwargs.pop("questionid")
        super(ModifyQuestionForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(ModifyQuestionForm, self).clean()
        # get the relevant values
        usedocker = cleaned_data.get('usedocker')
        imagename = cleaned_data.get('registryid')
        registryid = self.request.POST.get('registryid','')
        points = cleaned_data.get('points')
        hintpenalty = cleaned_data.get('hintpenalty')
        # set the self.usedocker for save function
        self.usedocker = usedocker

        # check if the question uses docker and registry is left blank 
        if usedocker is True and registryid == "":
            # set the error message
            msg = u"Please enter the Registry Image Name!"
            self._errors["usedocker"] = self.error_class([msg])
        
        # check if the hintpenalty or points is not None
        if hintpenalty is not None or points is not None:
            # check if the hint penalty is more than points (cause it shouldn't be)
            if int(hintpenalty) > int(points):
                # set the error message
                msg = u"Hint Penalty should not be more than Points awarded!"
                self._errors["hintpenalty"] = self.error_class([msg])


    def save(self, commit=True):
        question = super().save(commit=False)
        # get the relevant values
        topicname = self.request.POST.get('topicname',' ')
        registryid = self.request.POST.get('registryid','')
        # get the topic id
        topicid = QuestionTopic.objects.get(topicname = topicname)
        # set the topicid
        question.topicid = topicid
        # get the remarks
        remarks = self.request.POST.get('remarks','')
        # set the remarks
        question.remarks = remarks

        # check if the question uses docker
        if self.usedocker is True:
            # set the registryid
            question.registryid = registryid
            imageid = registryid
            # call the CreateImage() View to create the image
            error = teachersview.CreateImage.get(self, self.request, self.rangeurl, self.questionid, imageid)
            # check if no error
            if error is not 0:
                # if got error, response
                return HttpResponse('ERROR')

        if commit:
            question.save()
        return question

    class Meta:
        model = Questions
        fields = ('title', 'text', 'hint', 'hintpenalty', 'answer', 'usedocker', 'points',)

# ClassForm
# Creates the class
class ClassForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ClassForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        newclass = super().save(commit=False)
        # set the datecreated to today
        newclass.datecreated = datetime.date.today()
        # set the timecreated to today
        newclass.timecreated = datetime.datetime.now().time()
        # get the current user
        admin = self.request.user
        # set the created by
        newclass.createdby = User.objects.get(username = admin)

        if commit:
            newclass.save()
        return newclass

    class Meta:
        model = UserClass
        fields = ('userclass',)