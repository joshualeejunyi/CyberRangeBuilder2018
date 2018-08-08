# Teachers app views.py
# This view will mainly controll all of the functionalities available on the teachers application

# imports
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, ModelFormMixin, UpdateView, DeleteView, CreateView
from django.views.generic.base import TemplateView
from django.views import generic 
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms import *
from ranges.models import *
from accounts.models import *
from django.core.paginator import Paginator
from .forms import *
from django_filters.views import FilterView
from .filters import *
from django.views import View
from django.contrib import messages
from django.views.generic import RedirectView
from functools import reduce
from django.db.models.functions import Lower
from django.contrib.auth.mixins import PermissionRequiredMixin
import requests
from .choices import *
from django.contrib import messages
import datetime
from tablib import *
import logging
import csv
from .decorators import *
from django.utils.decorators import method_decorator
from SDL.forms import *
from SDL.filters import *
from SDL.models import *

# Error TemplateView
# Currently working on designing a customized error page 
# Not deployed yet as it is not 100%
class Error(TemplateView):
    # use the template at teachers/error.html
    template_name = "teachers/error.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # set the errorcode as context
        # not fully functional
        context['errorcode'] = kwargs
        return context
        return render(request, 'teachers/error.html')

# CreateImage View
# This view will receive the rangeurl, questionid and imageid 
# This is so that we can create the docker image for that specific question
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class CreateImage(View):
    # create image class to pull from registry and create the image in the local server
    def get(self, request, rangeurl, questionid, imageid):
        data = {}
        # declare a list of server ip addresses for the for loop later
        serverip = ['192.168.100.42:8051', '192.168.100.43:8051']
        # conver the imageid to be lowercase
        imageid = imageid.lower()
        
        # start a forloop for each ip address in the list
        for ip in serverip:
            # set the enpoints and header to communicate with the server
            endpoint1 = 'http://' + ip + '/images/create?fromImage=dmit2.bulletplus.com:8053/{conid}'
            header1 = {"X-Registry-Auth": "eyAidXNlcm5hbWUiOiAiYWRtaW4iLCAicGFzc3dvcmQiOiAicGFzc3dvcmQiLCAic2VydmVyYWRkcmVzcyI6ICJkbWl0Mi5idWxsZXRwbHVzLmNvbTo4MDUzIiB9Cg=="}
            # format the url to be sent
            url1 = endpoint1.format(conid=imageid)
            # request for response 
            response = requests.post(url1, headers=header1)
            # check the status code
            if response.status_code == 200:
                # if 200 (okay), it will pass, not returning errors
                pass
            elif response.status_code == 404:
                # if 404 (no container found), it will return -1 as indication
                return -1 
            elif response.status_code == 500:
                # if 500 (server error), it will return 02
                return -2
            else:
                # if any other error, return the status_code
                return response.status_code

            # next, we have to rename the image
            reference = {}
            # concatenate the rangeurl and questionid with a period between to form the imagename syntax
            imagename = str(rangeurl) + '.' + str(questionid)
            # set the endpoint
            endpoint2 = 'http://' + ip + '/images/dmit2.bulletplus.com:8053/' + imageid + '/tag?repo=' + imagename
            # request for response
            response = requests.post(endpoint2)
            # check the status code
            if response.status_code == 201:
                # if 201 (okay), will pass
                pass
            elif response.status_code == 400:
                # if 400 (bad parameter), will return -3
                return -3
            elif response.status_code == 404:
                # if 404 (no image found), will return a -4
                return -4
            elif response.status_code == 409:
                # if 409 (conflict), will return -5
                return -5
            elif response.status_code == 500:
                # if 500 (server error), will return -2 (same as above)
                return -2
            else:
                # otherwise, return the code
                return response.status_code

        # if all okay, return 0 
        return 0

#################################################################
# The following code will support Teacher Dashboard
# The dashboard as of end of phase 1 only displays users that have registered through the website but not accepted
# This view will retrieve all the unaccpeted users and display in a table
# The teacher can then choose the accept or reject the user (see views AcceptUser and RejectUser)

# Teacher Dashboard View
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class TeacherDashboard(ListView, PermissionRequiredMixin):
    # use the template at teachers/teacherdashboard.html
    template_name = 'teachers/teacherdashboard.html'
    # set the context_object_name (from get_queryset() function) as usersobject to be used in the template
    context_object_name = 'usersobject'
    # paginate by 10, so that the page won't load too many at once
    paginate_by = 10
    # use the StudentFilter class in filters.py
    filterset_class = StudentFilter

    # get_queryset function will return the queryset for the listview
    def get_queryset(self):
        # unacceptedstudents criteria:
        # not superuser
        # not staff
        # is disabled
        # not accepted
        unacceptedstudents = User.objects.filter(is_superuser = False, is_staff = False, isdisabled=True, isaccepted=False).order_by('-lastmodifieddate', '-lastmodifiedtime')
        # return the queryset
        return unacceptedstudents
    
    # get_context_data function will get additional context to be displayed on the template
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set the UserClass as a context to be used in the template
        context['classesobject'] = UserClass.objects.all()
        # return the context
        return context

# AcceptUser View
# This view will process the function to accept the user
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AcceptUser(View):
    # use a simple get function because its not a big functionality
    # get will receive the username of the user to be accepted
    def get(self, request, username):
        # get the object of the user selected
        selecteduser = User.objects.get(username = username)
        # set the parameters:
        # is accepted
        selecteduser.isaccepted = True
        # is not disabled
        selecteduser.isdisabled = False
        # set the last modified date and time
        selecteduser.lastmodifieddate = datetime.date.today()
        selecteduser.lastmodifiedtime = datetime.datetime.now().time()
        # get the currentuser accepting the request (teacher's account)
        admin = self.request.user
        # set the last modified by to the current user
        selecteduser.lastmodifiedby = User.objects.get(username = admin)
        # set the accepted by to the current user
        selecteduser.acceptedby = User.objects.get(username = admin)
        # get the class that the user belongs to
        userclass = selecteduser.userclass.userclass
        # get the userclass obj of the user's class
        userclassobj = UserClass.objects.get(userclass = userclass)
        # add the student count of the class by 1
        userclassobj.studentcount = userclassobj.studentcount + 1
        # save the userclass object
        userclassobj.save()
        # delete the user object
        # save the object
        selecteduser.save()

        # return to the dashboard
        return redirect('/teachers/')

# RejectUserView
# This view will process the function to reject the user
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class RejectUser(View):
    # get will receive the user name of the user to be rejected
    def get(self, request, username):
        # get the object of the selected user
        selecteduser = User.objects.get(username = username)
        selecteduser.delete()
        
        # return to the dashboard
        return redirect('/teachers/')

#################################################################
# The following code will support User Management 

# UserManagement View
# This view will give the teacher access to all functionalities related to handling and managing users (that are not disabled and are accepted)
# The users displayed in this page are not disabled and are accepted
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class UserManagement(FilterView, ListView):
    # use the template teachers/usermanagement.html
    template_name = 'teachers/usermanagement.html'
    # set the context_object_name to usersobject for the templaet
    context_object_name = 'usersobject'
    # paginate by 10 entries
    paginate_by = 10
    # call the StudentFilter class in filters.py
    filterset_class = StudentFilter

    # get_queryset function will get all the users
    def get_queryset(self):
        # requirements for user:
        # not superuser
        # not staff
        # not disabled
        # is accepted
        allstudents = User.objects.filter(is_superuser = False, is_staff = False, isdisabled=False, isaccepted=True).order_by('-lastmodifieddate', '-lastmodifiedtime')
        return allstudents
    
    # get_context_data function to get the relevant context
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set all the userclass queryset as context
        context['classesobject'] = UserClass.objects.all()
        # return context
        return context

# DisabledUserManagement
# This view will give the teacher access to all functionalities related to handling and managing disabled users
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DisabledUserManagement(FilterView, ListView):
    # use the template teachers/disabledusermanagement.html
    template_name = 'teachers/disabledusermanagement.html'
    # set the context_object_name as usersobject for template
    context_object_name = 'usersobject'
    # paginate by 10
    paginate_by = 10
    # call the StudentFilter in filters.py
    filterset_class = StudentFilter

    # get_queryset function
    def get_queryset(self):
        # requirements for disabled users:
        # not superuser
        # not staff
        # is disabled
        # is accepted
        allstudents = User.objects.filter(is_superuser = False, is_staff = False, isdisabled=True, isaccepted=True).order_by('-lastmodifieddate')
        # return the queryset
        return allstudents
    
    # get_context_data function
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set all the userclass queryset as context
        context['classesobject'] = UserClass.objects.all()
        # return context
        return context

# AddUser View
# This view will allow the teacher to manually add additional users
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddUser(ListView, ModelFormMixin):
    # use the template teachers/adduserform.html
    template_name = 'teachers/adduserform.html'
    # set the context_object_name as classesobject
    context_object_name = 'classesobject'
    # use the model User in accounts.models
    model = User
    # set the form class as AdminRegisterForm in forms.py
    form_class = AdminRegisterForm

    # def get will display the initial form
    def get(self, request, *args, **kwargs):
        # set the object as None
        self.object = None
        # call the form
        self.form = self.get_form(self.form_class)
        # return the listview with the form to be displayed
        return ListView.get(self, request, *args, **kwargs)

    # def post will process the form
    def post(self, request, *args, **kwargs):
        # set the object as None
        self.object = None
        # call the form
        self.form = self.get_form(self.form_class)

        # check if the form is valid
        if self.form.is_valid():
            # save the form if valid
            self.form.save()
            # redirect the teacher to the usermanagement page
            return redirect('/teachers/usermanagement/')
        else:
            # if not valid, return to the form with the errors
            return ListView.get(self, request, *args, **kwargs)
    
    # get_queryset function will get the userclasses to be displayed in the dropdown menu
    def get_queryset(self):
        classes = UserClass.objects.all()
        return classes

    # get_form_kwargs will get the relevant kwarg to be passed into the form
    def get_form_kwargs(self):
        # call super
        kwargs = super(AddUser, self).get_form_kwargs()
        # set the request as a kwarg
        kwargs.update({'request': self.request})
        # return kwargs
        return kwargs

# ModifyUser View
# This view will allow the teacher to modify user accounts
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ModifyUser(UpdateView):
    # set the form class as AdminModifyForm in forms.py
    form_class = AdminModifyForm
    # use the model User in accounts.models
    model = User
    # use the template teachers/modifyuserform.html
    template_name = 'teachers/modifyuserform.html'
    # when update successful, redirect to usermanagement
    success_url = '/teachers/usermanagement'

    # get the object to be updated
    def get_object(self, queryset = None):
        # use the kwargs in the URL to get the user object
        selecteduser = User.objects.get(username = self.kwargs['username'])
        # return the object to the update view
        return selecteduser
    
    # get_context _data
    def get_context_data(self, **kwargs):
        # call supser
        context = super().get_context_data(**kwargs)
        # call the userclass object to be displayed in the dropdown template
        context['classesobject'] = UserClass.objects.all()
        # return context
        return context

    # get_form_kwargs will get the relevant kwargs for the form
    def get_form_kwargs(self):
        # call super
        kwargs = super(ModifyUser, self).get_form_kwargs()
        # set the request as a kwargs
        kwargs.update({'request': self.request})
        # return kwargs
        return kwargs

# ResetPasswordView
# This view will allow the teacher to reset the password of a user who has forgotten their password
@method_decorator(user_is_staff, name='dispatch')
class ResetPasswordView(UpdateView):
    # use the form class AdminResetCommit in forms.py
    form_class = AdminResetCommit
    # use the User model in accounts.models
    model = User
    # use the template teachers/resetpassword.html
    template_name = 'teachers/resetpassword.html'
    # if successful, redirect to the suermanagement
    success_url = '/teachers/usermanagement'

    # get_object will get the object to be updated
    def get_object(self, queryset = None):
        # use the kwargs in the URL to get the user object
        selecteduser = User.objects.get(username = self.kwargs['username'])
        # return the user object
        return selecteduser
    
    # get_form_kwargs will get the relevant kwargs for the form
    def get_form_kwargs(self):
        # call super
        kwargs = super(ResetPasswordView, self).get_form_kwargs()
        # set the request as a kwargs
        kwargs.update({'request': self.request})
        # return kwargs
        return kwargs

# DisableUser View
# This view will process the function to disable the user selected in user management
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DisableUser(View):
    # def get to process view
    # receives the username of the selected user
    def get(self, request, username):
        # get the user object using the username
        selecteduser = User.objects.get(username = username)
        # set the isdisabled parameter as True
        selecteduser.isdisabled = True
        # save the object
        selecteduser.save()

        # redirect to the usermanagement
        return redirect('/teachers/usermanagement/')

# EnableUser View
# This will reverse the disable user function
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class EnableUser(View):
    # def get to process
    # receives the username of the selected user
    def get(self, request, username):
        # get the user object using the username
        selecteduser = User.objects.get(username = username)
        # set the isdisabledparameter to False
        selecteduser.isdisabled = False
        # save the object
        selecteduser.save()

        # redirect to disabled usermanagement
        return redirect('/teachers/usermanagement/disabled')

# DeleteUser View
# This will delete the user selected by the teacher
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DeleteUser(View):
    # receives the username of the selected user
    def get(self, request, username):
        # get the userobject of the username
        selecteduser = User.objects.get(username = self.kwargs['username'])
        # get the student's class
        userclass = selecteduser.userclass
        # get the userclass obj of the user's class
        userclassobj = UserClass.objects.get(userclass = userclass)
        # reduce the student count of the class by 1
        userclassobj.studentcount = userclassobj.studentcount - 1
        # save the userclass object
        userclassobj.save()
        # get the fakeuser object from the fakeuser model to delete
        # fake objects are to delete the object without foreign key constraints 
        fakeuser = FakeUser.objects.get(username = self.kwargs['username'])
        # delete the fake objects
        fakeuser.delete()
        # delete the selected user object
        selecteduser.delete()
        # set the url to redirect to
        url = '/teachers/usermanagement/disabled'
        # redirect to the disabled user management
        return redirect(url)

#################################################################
# The following code will support Group Management 
# GroupManagement View
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class GroupManagement(FilterView, ListView):
    # use the template teachers/groupmanagement.html
    template_name = 'teachers/groupmanagement.html'
    # set context_object_name as groupobjects
    context_object_name = 'groupobjects'
    # set the filterset class to GroupFilter in filters.py
    filterset_class = GroupFilter
    # paginate by 10
    paginate_by = 10

    # get_queryset
    def get_queryset(self):
        # retrieve all groups from the database
        allgroups = Group.objects.all().order_by('-lastmodifieddate', '-lastmodifiedtime', '-datecreated', '-timecreated')
        # return the queryset
        return allgroups

# AddGroup View
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddGroup(ListView, ModelFormMixin):
    # use template teachers/addgroupform.html
    template_name = 'teachers/addgroupform.html'
    # use the Group model in accounts.models
    model = Group
    # set the form class to AddGroupCommit in forms.py
    form_class = AddGroupCommit

    # standard get and post functions
    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # if the form is vali, save the form
            self.form.save()
            # redirect to group management
            return redirect('/teachers/groupmanagement/')
        else:
            return ListView.get(self, request, *args, **kwargs)
    
    # get_queryset function
    def get_queryset(self):
        # gets all the classes
        classes =  UserClass.objects.all()
        # return the classes queryset
        return classes
    
    # get_form_kwargs to get request for form
    def get_form_kwargs(self):
        # call super
        kwargs = super(AddGroup, self).get_form_kwargs()
        # set request as kwarg
        kwargs.update({'request': self.request})
        # return kwargs
        return kwargs

# GroupView
# Details of the group along with users within it 
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class GroupView(ListView):
    # use template teachers/groupiew.html
    template_name = 'teachers/groupview.html'
    # set context object name as usersobject
    context_object_name = 'usersobject'

    # get_queryset
    def get_queryset(self):
        # get the groupid
        groupid = Group.objects.filter(groupname = self.kwargs['groupname']).values_list('groupid')[0][0]
        # get the students in the groupd
        studentsingroup = StudentGroup.objects.filter(groupid = groupid).values_list('studentid')

        # check if got anyone in the group
        if len(studentsingroup) != 0:
            # if there is, get the queryset
            students = User.objects.filter(email = studentsingroup[0][0])
            for x in range(1, len(studentsingroup)):
                # use a forloop
                # concatenate the user objects 
                result = User.objects.filter(email = studentsingroup[x][0])
                students = students | result
        else:
            # if no students, set as None
            students = None

        # return students queryset
        return students

    # get_context_data function
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set groupname as context
        context['groupname'] = self.kwargs['groupname']
        # set groupobject as context
        context['groupobjects'] = Group.objects.filter(groupname = self.kwargs['groupname']).order_by('-lastmodifieddate')
        # return context
        return context

# AddUserInGroup View
# Displays all the users that can be added into the group and gives teachers the option to add users
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddUserInGroup(FilterView, ListView):
    # use template teachers/adduseringroup.html
    template_name = 'teachers/adduseringroup.html'
    # set contextobjectname as usersobject
    context_object_name = 'usersobject'
    # paginate by 10
    paginate_by = 10
    # set filtersetclass as StudentFilter
    filterset_class = StudentFilter

    def get_queryset(self):
        # get the group id from the groupname
        groupid = Group.objects.filter(groupname = self.kwargs['groupname']).values_list('groupid')[0][0]
        # get the students that are already in the group
        studentsingroup = StudentGroup.objects.filter(groupid = groupid).values_list('studentid')
        # get students excluding those already in the group
        allstudents = User.objects.filter(is_superuser = False, is_staff = False).exclude(email__in=studentsingroup).order_by('-lastmodifieddate')
        return allstudents
    
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set the userclass queryset as context
        context['classesobject'] = UserClass.objects.all()
        # set groupname as context
        context['groupname'] = self.kwargs['groupname']

        # check if there is a usercart session
        if "usercart" in self.request.session:
            # if there is, get the session 
            cart = self.request.session.get('usercart', {})
            # set the cart as context
            context['cart'] = cart

        # return context
        return context

# AddUserToCart View
# Processes the adding of user to cart
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddUserToCart(View):
    # gets the groupname and username
    def get(self, request, groupname, username):
        # check if the username is valid
        get_object_or_404(User, username = username)
        # get the email using the username
        useremail = User.objects.filter(username = username).values_list('email')[0][0]
        # create empty list
        userslist = []
        # check if there is a usercart session
        if 'usercart' in request.session:
            # if there is, add the users in the session into the list
            userslist = request.session['usercart']
        # check if the username is not in the list
        if username not in userslist:
            # if there isn't, add to the list 
            userslist.append(useremail)
        # set the request.session as the new list
        request.session['usercart'] = userslist

        # set the url to direct to
        url = request.META.get('HTTP_REFERER')
        # redirect back to the addusersingroup page
        return redirect(url)

# RemoveUserFromCart
# Processes the removal of users in cart
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class RemoveUserFromCart(View):
    # gets the groupname and username
    def get(self, request, groupname, username):
        # checks if the username is valid
        get_object_or_404(User, username = username)
        # gets the meail
        useremail = User.objects.filter(username = username).values_list('email')[0][0]
        # create new list
        userslist = []
        # check if there is a session
        if 'usercart' in request.session:
            # if there is, add to the list
            userslist = request.session['usercart']
        # check if the email in the list
        if useremail in userslist:
            # remove the user from the list
            userslist.remove(useremail)
        # set the new session
        request.session['usercart'] = userslist

        # set the url to redirect to 
        url = request.META.get('HTTP_REFERER')
        # redirect to the addusersingroup page
        return redirect(url)

# UserGroupCommit View
# handles the commiting of adding user into group
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class UserGroupCommit(View):
    # gets the groupname
    def get(self, request, groupname):
        # checks the usercart session
        if 'usercart' in request.session:
            # if there is, set the userslist
            userslist = request.session['usercart']

        # for loop for each student
        for student in userslist:
            # get the studentid of the user
            studentid = User.objects.get(email = student)
            # get the groupid of the group 
            groupid = Group.objects.get(groupname = groupname)
            # create a new studentgroup object
            obj = StudentGroup(studentid = studentid, groupid = groupid)
            # save the object
            obj.save()

        messages.success(request, 'User(s) Successfully Added to Group')
        # set the url to redirect to
        url = "/teachers/groupmanagement/" + groupname
        # delete the session
        del request.session['usercart']
        # redirect to the group view
        return redirect(url)

# RemoveStudentFromGroup View
# removes the student from the group
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class RemoveStudentFromGroup(View):
    # gets the groupname and username
    def get(self, request, groupname, username):
        # gets the student object from the username
        studentid = User.objects.get(username = self.kwargs['username'])
        # gets the group object from the groupname
        groupid = Group.objects.get(groupname = groupname)
        # gets the studentgroup objects from the two objects above
        selecteduser = StudentGroup.objects.get(studentid = studentid, groupid = groupid)
        # delete the studentgroup object
        selecteduser.delete()

        # set url to redirect to 
        url = '/teachers/groupmanagement/' + groupname
        # redirect to groupview
        return redirect(url)

# MakeLeader View
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class MakeLeader(View):
    # gets the groupname and username
    def get(self, request, groupname, username):
        # gets the student object from the username
        studentid = User.objects.get(username = self.kwargs['username'])
        # gets the groupobject using groupname
        group = Group.objects.get(groupname = groupname)
        # sets the groupleader as the new studentid
        group.groupleader = studentid
        # save the group object
        group.save()

        # set the url to redirect
        url = "/teachers/groupmanagement/" + groupname
        # redirect to the group view
        return redirect(url)

# DeleteGroup View
# delete the group
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DeleteGroup(View):
    # gets the groupname
    def get(self, request, groupname):
        # gets the group object using group name
        groupobj = Group.objects.get(groupname = groupname)
        # gets the groupid
        groupid = Group.objects.filter(groupname = groupname).values_list('groupid')[0][0]
        # gets the fake group object using the groupid
        fakegroupobj = FakeStudentGroup.objects.filter(groupid = groupid)
        # delete the fake object
        fakegroupobj.delete()
        # delete the actual object
        groupobj.delete()
        # redirect to group management
        return redirect('/teachers/groupmanagement')

#################################################################
# The following code will support Range Management 
# RangeManagement View
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class RangeManagement(FilterView, ListView):
    # use template teachers/rangemanagement.html
    template_name = 'teachers/rangemanagement.html'
    # set contextobjectname as ranges
    context_object_name = 'ranges'
    # paginate by 10
    paginate_by = 10
    # set filtersetclass as RangeFilter
    filterset_class = RangeFilter

    # get_queryset function
    def get_queryset(self):
        # get the current user (teacher)
        user = self.request.user
        # get the ranges that are not disabled and created by the user
        ranges = Range.objects.all().filter(isdisabled = False, createdby=user).order_by('-lastmodifieddate', '-datecreated')
        # return the queryset
        return ranges

# ArchivedRangeManagement View
# manage all the archived ranges
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ArchivedRangeManagement(FilterView, ListView):
    # use template teachers/archivedrangemanagement.html
    template_name = 'teachers/archivedrangemanagement.html'
    # set contextobjectname as ranges
    context_object_name = 'ranges'
    # paginate by 10
    paginate_by = 10
    # set filtersetclass as RangeFilter
    filterset_class = RangeFilter

    # get_queryset function    
    def get_queryset(self):
        # get the ranges that are disabled
        ranges = Range.objects.all().filter(isdisabled = True)
        # return the queryset
        return ranges

# CreateRange View
# allows teachers to create a new range
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class CreateRange(CreateView, RedirectView):
    # use the template teachers/addrange.html
    template_name = 'teachers/addrange.html'
    # use Range model
    model = Range
    # use RangeForm
    form_class = RangeForm

    # get_form_kwargs to get request for form
    def get_form_kwargs(self):
        # call super
        kwargs = super(CreateRange, self).get_form_kwargs()
        # set the request in kwargs
        kwargs.update({'request': self.request})
        # return kwargs
        return kwargs

    # def get function
    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return CreateView.get(self, request, *args, **kwargs)

    # def post
    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        # check if form is valid
        if self.form.is_valid():
            # save form
            self.form.save()
            # get the rangeurl
            rangeurl = self.form.cleaned_data['rangeurl']
            # set the url to redirect to
            url = '/teachers/rangemanagement/view/' + rangeurl
            # set the message
            messages.success(request, 'Range Created.')
            # redirect to the newly created range
            return redirect(url)
        else:
            # if not valid,
            # return back to the form
            return CreateView.get(self, request, *args, **kwargs)

# RangeView
# Manage the range 
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class RangeView(ListView, FilterView):
    # use the teachers/rangeview.html
    template_name = 'teachers/rangeview.html'
    # set the contextobjectname as result
    context_object_name = 'result'
    # use the QuestionFilter
    filterset_class = QuestionFilter

    # getqueryset
    def get_queryset(self):
        # get the current range object by the rangeurl
        selectedrange = Range.objects.get(rangeurl= self.kwargs['rangeurl'])
        # get the rangeid
        selectedrangeid = selectedrange.rangeid
        # get the questions using the rangeid
        result = Questions.objects.filter(rangeid = selectedrangeid, isarchived = False)
        # check if got no questions
        if len(result) == 0:
            # return None
            return None
        # return queryset
        return result
    
    # get_context_data
    def get_context_data(self, **kwargs):
        # get super
        context = super().get_context_data(**kwargs)
        # get the range object
        selectedrange = Range.objects.get(rangeurl= self.kwargs['rangeurl'])
        # get the rangeid
        selectedrangeid = selectedrange.rangeid

        # set isopen as context
        context['isopen'] = selectedrange.isopen
        # set the rangename as context
        context['rangename'] = selectedrange.rangename
        # set the range object as context
        context['range'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl'])
        # set the rangeurl as context
        context['rangeurl'] = self.kwargs['rangeurl']
        # set the topics as context
        context['topics'] = QuestionTopic.objects.all()
        # set the rangeactive as context
        context['activated'] = selectedrange.rangeactive
        # get the students in range
        studentsinrange = RangeStudents.objects.filter(rangeID = selectedrangeid).values_list('studentID')
        # check if there are students in the range
        if len(studentsinrange) != 0:
            # get the first student in range
            result = User.objects.filter(email = (studentsinrange[0][0]))
            # forloop for all the students
            for x in range(1, len(studentsinrange)):
                # append the users as a queryset
                currentuser = User.objects.filter(email = studentsinrange[x][0])
                result = result | currentuser
        else:
            # if no students, set result as None
            result = None
        
        # set the students as context
        context['students'] = result

        # get the students in group in range
        groupstudent = RangeStudents.objects.filter(rangeID = selectedrangeid, groupid__isnull = False)
        # set the groupstudent as context
        context['groupstudent'] = groupstudent

        # get the students in group in range, exclude if the groupid is null
        groupsinrange = RangeStudents.objects.filter(rangeID = selectedrangeid).exclude(groupid__isnull=True).values_list('groupid').distinct()
        # check if the length is not 0
        if len(groupsinrange) != 0:
            # get the first group object
            groups = Group.objects.filter(groupid = groupsinrange[0][0])
            # forloop the groups in range
            for x in range(1, len(groupsinrange)):
                # append the groups as a queryset
                currentgroup = Group.objects.filter(groupid = groupsinrange[x][0])
                groups = groups | currentgroup
        else:
            # if no groups, set groups as None
            groups = None
        
        # set groups as context
        context['groups'] = groups
        # return context
        return context

# ReportView
# Displays the selected user's report of the range
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ReportView(generic.ListView):
    # use template teachers/report.html
    template_name='teachers/report.html'
    # set contextobjectname as questionsobject
    context_object_name = 'questionsobject'
    def get_queryset(self):
        # get the rangeurl
        rangeurl = self.kwargs['rangeurl']
        # get the username
        username = self.kwargs['username']
        # get the rangeid 
        rangeid = Range.objects.filter(rangeurl=rangeurl).values_list('rangeid')[0][0]
        # get the user email
        useremail = User.objects.filter(username=username).values_list('email')[0][0]
        # get the rangestudents object
        rangestudentobj = RangeStudents.objects.filter(studentID=useremail, rangeID__rangeid=rangeid)

        # get the studentquestionsobject
        studentquestionsobj = StudentQuestions.objects.filter(rangeid=rangeid, studentid=useremail)
        # create new list
        answeredquestionlist = []
        # forloop the studentquestions object
        for question in studentquestionsobj:
            # get the questionid
            questionid = question.questionid.questionid
            # check if the questionid is not in the list
            if questionid not in answeredquestionlist:
                # append the questionid into the list
                answeredquestionlist.append(questionid)

        # get the questionsobject excluding the questions in the list
        questionsobj = Questions.objects.filter(rangeid=rangeid).exclude(questionid__in=answeredquestionlist)
        # return object
        return questionsobj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the rangeurl
        rangeurl = self.kwargs['rangeurl']
        # get the username
        username = self.kwargs['username']
        # get the rangeid
        rangeid = Range.objects.filter(rangeurl=rangeurl).values_list('rangeid')[0][0]
        # get the useremail
        useremail = User.objects.filter(username=username).values_list('email')[0][0]
        # get the rangeobject
        rangeobj = Range.objects.get(rangeurl=rangeurl)
        # get the rangestudents object
        rangestudentsobj = RangeStudents.objects.get(studentID=useremail, rangeID=rangeid)
        # get the studentquestions object
        studentquestionsobj = StudentQuestions.objects.filter(studentid=useremail, rangeid=rangeid)
 
        # set the rangename as context
        context['rangename'] = rangeobj.rangename
        # set the maxscore as context
        context['maxscore'] = rangeobj.maxscore
        # set the points awarded as context
        pointsawarded = rangestudentsobj.points
        context['pointsawarded'] = pointsawarded

        # get the hintpenaly queryset
        hintpenaltyqueryset = StudentHints.objects.filter(studentid=username, rangeid = rangeid, hintactivated = True).values_list('questionid')
        # set the number to 0
        totalhintpenalty = 0
        
        # forloop the number of hintused
        for x in range(0, len(hintpenaltyqueryset)):
            # get the hintpenalty
            points = Questions.objects.filter(questionid = hintpenaltyqueryset[x][0]).values_list('hintpenalty')[0][0]
            # append to the hintpenalty
            totalhintpenalty = totalhintpenalty + int(points)

        # set hintpenalty as context
        context['hintpenalty'] = totalhintpenalty
        # get the unobtained points
        unobtained = rangeobj.maxscore - totalhintpenalty - pointsawarded
        # set as context
        context['unobtained'] = unobtained
        # set the rangestudents object as context
        context['rangestudentsobj'] = rangestudentsobj
        # set the studentquestions object as context
        context['studentquestionsobj'] = studentquestionsobj
        # set all the quetions as context
        context['allquestions'] = Questions.objects.filter(rangeid=rangeid)
        # get the rangeactive as context
        context['rangeactive'] = Range.objects.filter(rangeid=rangeid).values_list('rangeactive')[0][0]

        # get the rankings of all the students
        ranking = RangeStudents.objects.filter(rangeID=rangeid).order_by('-points')
        # set the username as context
        context['username'] = username
        # set the ranking as context
        context['ranking'] = ranking
        # return context
        return context

# OEMarkCorrect View
# This will process to mark a student's openended answer as correct
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class OEMarkCorrect(View):
    # get the rangeurl, username and questionid
    def get(self, request, rangeurl, username, questionid):
        # get the range object
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        # get the student object
        studentinstance = User.objects.get(username = username)
        # get the question object
        questioninstance = Questions.objects.get(questionid = questionid)
        # check the number of times the student attempted this question
        repeatedcheck = StudentQuestions.objects.filter(questionid = questionid, studentid = studentinstance, rangeid = rangeinstance).count()
        # get the studentquestion object
        studentquestionobj = StudentQuestions.objects.get(rangeid = rangeinstance, questionid = questioninstance, studentid = studentinstance, attempts = repeatedcheck)
        # set the answer correct flag to 1
        studentquestionobj.answercorrect = 1

        # get the question points
        questionpoints = Questions.objects.filter(questionid = questionid).values_list('points')[0][0]
        # set the marks awarded
        studentquestionobj.marksawarded = questionpoints
        # set the ismarked flag to True
        studentquestionobj.ismarked = True
        # get the rangestudents object
        rangestudentsobj = RangeStudents.objects.get(studentID = studentinstance, rangeID = rangeinstance)
        # add the questoin points
        rangestudentsobj.points += questionpoints

        # save the objects
        studentquestionobj.save()
        rangestudentsobj.save()

        # redirect back to the report
        return redirect('../../../')

# OEMarkWrong View
# This will process to mark a student's openended answer as wrong
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class OEMarkWrong(View):
    def get(self, request, rangeurl, username, questionid):
        # get the range object
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        # get the student instance
        studentinstance = User.objects.get(username = username)
        # get the question instance
        questioninstance = Questions.objects.get(questionid = questionid)
        # get the number of times the student attempted the question
        repeatedcheck = StudentQuestions.objects.filter(questionid = questionid, studentid = studentinstance, rangeid = rangeinstance).count()
        # get the studentquestions object
        studentquestionobj = StudentQuestions.objects.get(rangeid = rangeinstance, questionid = questioninstance, studentid = studentinstance, attempts = repeatedcheck)
        # set the answer correct flag to 0
        studentquestionobj.answercorrect = 0
        # set the ismarked flag as True
        studentquestionobj.ismarked = True
        # save the object
        studentquestionobj.save()
        # redirect to the report
        return redirect('../../../')

# ArchivedRangeQuestions View
# Manage all the archived range questions
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ArchivedRangeQuestions(ListView, FilterView):
    # use the teachers/archivedrangequestions.html
    template_name = 'teachers/archivedrangequestions.html'
    # set contextobjectname as result
    context_object_name = 'result'
    # set filsterclass as QuestionFilter
    filterset_class = QuestionFilter

    # get_queryset function
    def get_queryset(self):
        # get the range object
        selectedrange = Range.objects.get(rangeurl= self.kwargs['rangeurl'])
        # get the rangeid 
        selectedrangeid = selectedrange.rangeid
        # get the questions in the range
        result = Questions.objects.filter(rangeid = selectedrangeid, isarchived = True)
        # return result
        return result

    # get_context_data
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # get the range object
        selectedrange = Range.objects.get(rangeurl= self.kwargs['rangeurl'])
        # get the rangeid
        selectedrangeid = selectedrange.rangeid

        # set the rangename as context
        context['rangename'] = selectedrange.rangename
        # set the range object as context
        context['range'] = selectedrange
        # set the range url as context
        context['rangeurl'] = self.kwargs['rangeurl']
        # set the questiontopics as context
        context['topics'] = QuestionTopic.objects.all()
        # set the number of archived questions as context
        context['archivednumber']= Questions.objects.filter(rangeid = selectedrangeid, isarchived = True).count()
        # return context
        return context

# AddQuestioninRange
# show the questions that can be added into the range, allow the teacher to select and add to cart
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddQuestioninRange(FilterView, ListView):
    # use the template teachers/addquestionsinrange.html
    template_name = 'teachers/addquestionsinrange.html'
    # set contextobjectname as questions
    context_object_name = 'questions'
    #set the QuestionFilter as filtersetclass
    filterset_class = QuestionFilter
    # paginate by 10
    paginate_by = 10

    # get_queryset function
    def get_queryset(self):
        # first i have to get all the questions in the current range
        # then i filter that our from the final queryset
        
        # get current range id
        currentrangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        # get the questions in range
        questionsinrange = Questions.objects.filter(rangeid = currentrangeid).values_list('questionid')
        # get the questions from the database, exclude the questions already in the range
        unimportedquestions = Questions.objects.exclude(questionid__in=questionsinrange)
        # check if the length of unimportedquestions is 0
        if len(unimportedquestions) == 0:
            # if 0, return None
            return None
        # otherwise, return the queryset
        return unimportedquestions

    # get_context_data function
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set the rangename as context
        context['rangename'] = Range.objects.filter(rangeurl= self.kwargs['rangeurl']).values_list('rangename')[0][0]
        # set the topics as context
        context['topics'] = QuestionTopic.objects.all()

        # create empty list 
        questionslist = []
        # check if there is a quetions cart in session
        if 'questionscart' in self.request.session:
            # get the questionscart
            cart = self.request.session.get('questionscart', {})
            # set the cart as context
            context['cart'] = cart

        # return the context
        return context

# AddQuestionsToCart View
# adds the question selected to the cart
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddQuestionToCart(View):
    # def get function
    # gets the questionid and rangeurl
    def get(self, request, questionid, rangeurl):
        # checks if questionid and rangeurl is valid
        get_object_or_404(Questions, questionid = questionid)
        get_object_or_404(Range, rangeurl = rangeurl)

        # create empty list
        questionslist = []
        # check if there is a questionscart in session
        if 'questionscart' in request.session:
            # get the session list
            questionslist = request.session['questionscart']
        # check if the question selected in the list
        if questionid not in questionslist:
            # append the questionid to the list
            questionslist.append(questionid)
        # set the list in session
        request.session['questionscart'] = questionslist

        # set the url to redirect to
        url = request.META.get('HTTP_REFERER')
        # redirect to the addquestionsinrange page
        return redirect(url)

# RemoveQuestionFromCart View
# removes the question in the cart
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class RemoveQuestionFromCart(View):
    # def get function
    # gets the questionid and rangeurl
    def get(self, request, questionid, rangeurl):
        # checks if questionid and rangeurl are valid
        get_object_or_404(Questions, questionid = questionid)
        get_object_or_404(Range, rangeurl = rangeurl)
        
        # create new list
        questionslist = []
        # check if there is a questionscart in session
        if 'questionscart' in request.session:
            # add the list to the cart
            questionslist = request.session['questionscart']
        # check if the questionid is in the questionslist
        if questionid in questionslist:
            # remove the question from the list
            questionslist.remove(questionid)
        # set the questionslist as session
        request.session['questionscart'] = questionslist

        # set the url to redirect to
        url = request.META.get('HTTP_REFERER')
        # redirect to the addqustionsinrange 
        return redirect(url)

# AddQuestioninRangeCommit View
# will save the changes to the database when adding questions from database
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddQuestioninRangeCommit(View):
    # def get function
    # gets the rangeurl
    def get(self, request, rangeurl):
        # get the range object
        rangeobj = Range.objects.get(rangeurl=rangeurl)

        # check if there is a cart in session
        if 'questionscart' in request.session:
            # get the questionscart in session as questionslist
            questionslist = request.session['questionscart']

        # forloop questionid in the questionslist
        for questionid in questionslist:
            # get the questionobject
            questionobj = Questions.objects.get(questionid = questionid)
            # set the primarykey as none 
            # this is to duplicate the object
            questionobj.pk = None
            questionobj.rangeid = rangeobj
            # set the isarchived is False
            questionobj.isarchived = False
            # save the questionobject
            questionobj.save()

            # check if it is mcq
            questiontype = questionobj.questiontype
            if questiontype == 'MCQ':
                mcqoptionsobj = MCQOptions.objects.get(questionid = questionid)
                mcqoptionsobj.pk = None
                mcqoptionsobj.rangeid = rangeobj
                newquestionobj = Questions.objects.get(questionid = questionobj.questionid)
                mcqoptionsobj.questionid = newquestionobj
                mcqoptionsobj.save()

            # get the question points
            questionpoints = questionobj.points
            # get the questionid
            questionid = questionobj.questionid
            # get the imageid
            imageid = questionobj.registryid
            # add the question points to the range max score
            rangeobj.maxscore = rangeobj.maxscore + questionpoints
            # save the range object
            rangeobj.save()

            # check if the question uses docker
            if questionobj.usedocker is True:
                # run the CreateImage View
                error = CreateImage.get(self, request, rangeurl, questionid, imageid)
                # check if successful
                if error is not 0:
                    # if it is not, get the error page
                    Error.get(self, request, error)
        
        # set the url to redirect to 
        messages.success(request, 'Questions Successfully Imported')
        url = '/teachers/rangemanagement/view/' + rangeurl
        # delete the session
        del request.session['questionscart']
        # redirect to the rangeview
        return redirect(url)

# EditQuestion View
# An UpdateView to allow teachers to modify questions
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class EditQuestion (UpdateView):
    # use the ModifyQuestionForm formclass
    form_class = ModifyQuestionForm
    # use the Questions model
    model = Questions
    # use the template teachers/editquestion.html
    template_name = 'teachers/editquestion.html'
    # redirect back if successful
    success_url = '../../'
    # set contextobjectname as result
    context_object_name = 'result'

    # get_form_kwargs function
    def get_form_kwargs(self):
        # get super
        kwargs = super(EditQuestion, self).get_form_kwargs()
        # set request as kwargs
        kwargs.update({'request': self.request})
        # get questionid
        questionid = self.kwargs['questionid']
        # set questionid as kwargs
        kwargs.update({'questionid': self.kwargs['questionid']})
        # return kwargs
        return kwargs

    # get_object function
    def get_object(self):
        # get question object
        questionobj = Questions.objects.get(questionid = self.kwargs['questionid'])
        # return question object
        return questionobj
    
    # get_context_data
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # get question object 
        questionobj = Questions.objects.get(questionid = self.kwargs['questionid'])
        # set questionid as context
        context['questionid'] = questionobj.questionid
        # get all questiontopic
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        # set questiontopic as context
        context['questiontopic'] = questiontopic
        # check if question is MCQ
        if questionobj.questiontype == 'MCQ':
            # get the mcqoptions object for that question
            mcqoptions_obj = MCQOptions.objects.get(questionid = selectedquestion)
            # set the options as context
            context['optionone'] = mcqoptions_obj.optionone
            context['optiontwo'] = mcqoptions_obj.optiontwo
            context['optionthree'] = mcqoptions_obj.optionthree
            context['optionfour'] = mcqoptions_obj.optionfour

        # return context
        return context

# EditRangeQuestion View
# edit the rangequestion, different from the above. This is from rangeview.
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class EditRangeQuestion (UpdateView):
    # use the ModifyRangeQuestionForm
    form_class = ModifyRangeQuestionForm
    # use the Questions model
    model = Questions
    # use the template teachers/editquestion.html
    template_name = 'teachers/editquestion.html'
    # redirect back if successful
    success_url = '../../'
    # set contextobjectname as result
    context_object_name = 'result'

    # get_form_kwargs
    def get_form_kwargs(self):
        # get super
        kwargs = super(EditRangeQuestion, self).get_form_kwargs()
        # set request as kwarg
        kwargs.update({'request': self.request})
        # get rangeurl
        rangeurl = self.kwargs['rangeurl']
        # set rangeurl as kwarg
        kwargs.update({'rangeurl': self.kwargs['rangeurl']})
            
        # return kwargs
        return kwargs

    # get object 
    def get_object(self):
        # get the question object
        questionobj = Questions.objects.get(questionid = self.kwargs['questionid'])
        # return question object
        return questionobj
    
     # get_context_data
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # get question object 
        questionobj = Questions.objects.get(questionid = self.kwargs['questionid'])
        # set questionid as context
        context['questionid'] = questionobj.questionid
        # get all questiontopic
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        # set questiontopic as context
        context['questiontopic'] = questiontopic
        # check if question is MCQ
        if questionobj.questiontype == 'MCQ':
            # get the mcqoptions object for that question
            mcqoptions_obj = MCQOptions.objects.get(questionid = questionobj.questionid)
            # set the options as context
            context['optionone'] = mcqoptions_obj.optionone
            context['optiontwo'] = mcqoptions_obj.optiontwo
            context['optionthree'] = mcqoptions_obj.optionthree
            context['optionfour'] = mcqoptions_obj.optionfour

        # return context
        return context

# ModifyRange View
# modify the details of the range
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ModifyRange(UpdateView):
    # set ModifyRangeForm as formclass
    form_class = ModifyRangeForm
    # use Range model
    model = Range
    # use template teachers/editrange.html
    template_name = 'teachers/editrange.html'
    # redirect back if success
    success_url = '../'

    # get_object
    def get_object(self, queryset = None):
        # get the rangeobject
        selectedrange = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
        # return the rangeobject
        return selectedrange

    # get_context_data
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # get the rangeobject
        rangeobject = Range.objects.filter(rangeurl = self.kwargs['rangeurl'])
        # set the rangeobject as context
        context['range'] = rangeobject
        # get all the questiontopic
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        # set the questiontopic as context
        context['questiontopic'] = questiontopic
        # set the rangeurl as context
        context['rangeurl'] = self.kwargs['rangeurl']

        # get the startdate
        startdate = rangeobject.values_list('datestart')[0][0]
        # check if start date is not None
        if startdate is not None:
            # format the startdate
            startdate = startdate.strftime('%Y-%m-%d')
            # set the startdate as context
            context['startdate'] = startdate
        # get the enddate
        enddate = rangeobject.values_list('dateend')[0][0]
        # check if the enddate is not None
        if enddate is not None:
            # format the enddate 
            enddate = enddate.strftime('%Y-%m-%d')
            # set the enddate as context
            context['enddate'] = enddate

        # get the starttime
        starttime = rangeobject.values_list('timestart')[0][0]
        # check if starttime is not None
        if starttime is not None:
            # format all the variables
            amorpm = starttime.strftime('%p')
            minutes = starttime.strftime('%M')
            hours = starttime.strftime('%H')
            # set the starttime as context
            context['starttime'] = str(hours) + ':' + str(minutes)

        # get the endtime
        endtime = rangeobject.values_list('timeend')[0][0]
        # check if the starttime is not None
        if endtime is not None:
            # format all the variables
            amorpm = endtime.strftime('%p')
            minutes = endtime.strftime('%M')
            hours = endtime.strftime('%H')
            # set the endtime as context
            context['endtime'] = str(hours) + ':' + str(minutes)
        # return context
        return context

    # get_form_kwargs
    def get_form_kwargs(self):
        # call super
        kwargs = super(ModifyRange, self).get_form_kwargs()
        # set the request as kwarg
        kwargs.update({'request': self.request})
        # return kwargs
        return kwargs

# ArchiveRange View
# functionality to archive range
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ArchiveRange(View):
    # def get function
    # get the rangeurl
    def get(self, request, rangeurl):
        # get the referer
        previousurl = request.META.get('HTTP_REFERER')
        # get the rangeobject
        selectedrange = Range.objects.get(rangeurl=self.kwargs['rangeurl'])
        # set as disabled
        selectedrange.isdisabled = 1
        # save the object
        selectedrange.save()

        # redirect to the previousurl
        return redirect(previousurl)
# UnarchiveRange View
# allows the teacher to unarchive the range
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class UnarchiveRange(View):
    # get the rangeurl
    def get(self, request, rangeurl):
        # get the previousurl
        previousurl = request.META.get('HTTP_REFERER')
        # get the rangeobject
        selectedrange = Range.objects.get(rangeurl=self.kwargs['rangeurl'])
        # set as not disabled
        selectedrange.isdisabled = 0
        # save the object
        selectedrange.save()

        # redirect back
        return redirect(previousurl)

# DeleteRange View
# allows the teacher to delete the range
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DeleteRange(View):
    # def get 
    # gets the rangeurl
    def get(self, request, rangeurl):
        # gets the rangeobject
        rangeobj = Range.objects.get(rangeurl = rangeurl)
        # get the rangeid
        rangeid = Range.objects.filter(rangeurl = rangeurl).values_list('rangeid')[0][0]
        # get the rangestudents object
        rangestudentsobj = RangeStudents.objects.filter(rangeID = rangeid)
        # get the rangequestionsobject
        rangequestionsobj = Questions.objects.filter(rangeid = rangeid)
        # get the fake range object
        fakerangeobj = FakeRange.objects.filter(rangeid = rangeid)

        # delete all the objects
        rangequestionsobj.delete()
        rangestudentsobj.delete()
        fakerangeobj.delete()
        rangeobj.delete()

        # redirect back
        return redirect('../../')

# ArchiveQuestion View
# archives the selected question
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ArchiveQuestion(View):
    # get rangeurl and the questionid
    def get(self, request, rangeurl, questionid):
        # get the previous url
        previousurl = request.META.get('HTTP_REFERER')
        # get the rangeinstance
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        # get the questioninstance
        selectedquestioninstance = Questions.objects.get(questionid = questionid)
        # get the questions object
        selectedrangequestion = Questions.objects.get(rangeid=rangeinstance, questionid=questionid)
        # set object as archived
        selectedrangequestion.isarchived = 1
        # save the object
        selectedrangequestion.save()
        # deduct the points from the maxscore of the rangeinstance
        updatedscore = rangeinstance.maxscore - selectedrangequestion.points
        # set the updatedscore
        rangeinstance.maxscore = updatedscore
        # save the object
        rangeinstance.save()
        # redirect to the previous url
        return redirect(previousurl)

# UnarchiveQuestion View
# unarchives the question
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class UnarchiveQuestion(View):
    # get rangeurl and questionid
    def get(self, request, rangeurl, questionid):
        # get previousurl
        previousurl = request.META.get('HTTP_REFERER')
        # get the rangeinstance
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        # get the rangequestion object
        selectedrangequestion = Questions.objects.get(rangeid=rangeinstance, questionid=questionid)
        # set the israchived to 0
        selectedrangequestion.isarchived = 0
        # save the object
        selectedrangequestion.save()
        # add the points to the maxscore
        updatedscore = rangeinstance.maxscore + selectedrangequestion.points
        # set the maxscore 
        rangeinstance.maxscore = updatedscore
        # save the rangeinstance
        rangeinstance.save()
        # redirect to the previous url
        return redirect(previousurl)

# DeleteQuestionFromRange
# allows the teacher to delete question from the range
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DeleteQuestionFromRange(View):
    # get the rangeurl and questionid
    def get(self, request, rangeurl, questionid):
        # get the prevoius url
        previousurl = request.META.get('HTTP_REFERER')
        # get the rangeinstance
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        # get the selected question instance object
        selectedquestioninstance = Questions.objects.get(questionid = questionid)
        # get the questionid
        # check if its an mcq question
        questiontype = selectedquestioninstance.questiontype
        if questiontype == 'MCQ':
            questionid = selectedquestioninstance.questionid
            mcqoptionsobject = MCQOptions.objects.get(questionid = questionid)
            mcqoptionsobject.delete()
        # delete object
        selectedquestioninstance.delete()
        # redirect to the previous url
        return redirect(previousurl)

# AssignUser View
# lists all the students that can be added into the range
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AssignUser(FilterView, ListView):
    # use the template teachers/assignuserrange.html
    template_name = 'teachers/assignuserrange.html'
    # set the contextobjectname as usersobject
    context_object_name = 'usersobject'
    # paginate by 10
    paginate_by = 10
    # set the filterset class as StudentFilter
    filterset_class = StudentFilter

    # get_queryset
    def get_queryset(self):
        # get the rangeid
        rangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        # get the students in the range
        studentsinrange = RangeStudents.objects.filter(rangeID = rangeid).values_list('studentID')
        # get all the students excluding those in the range already
        allstudents = User.objects.filter(is_superuser = False, is_staff = False, isdisabled = False).exclude(email__in=studentsinrange).order_by('-lastmodifieddate')
        # set the self.allstudents for the context below 
        self.allstudents = allstudents
        # return allstudents
        return allstudents

    # get_context_data
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set all userclass as context
        context['classesobject'] = UserClass.objects.all()
        # set the number of students as context
        context['studentnumber'] = len(self.allstudents)
        # set the rangename as context
        context['rangename'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]

        # check for userrangecart in session
        if "userrangecart" in self.request.session:
            # get the cart 
            cart = self.request.session.get('userrangecart', {})
            # set the cart as context
            context['cart'] = cart

        # return context
        return context

# AddUserRangeCart
# allows the teacher to add the user into the add range cart
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddUserRangeCart(View):
    # def get function
    # get the rangeurl and username
    def get(self, request, rangeurl, username):
        # check if user is valid
        get_object_or_404(User, username = username)
        # get the email
        useremail = User.objects.filter(username = username).values_list('email')[0][0]
        # create new list
        userslist = []
        # check if there is a userrangecart in session
        if 'userrangecart' in request.session:
            # set the userrangecart in userslist
            userslist = request.session['userrangecart']
        # check if the email not in the userslist
        if useremail not in userslist:
            # if not in the list,
            # append the email into the list
            userslist.append(useremail)
        # set the userslist as the session
        request.session['userrangecart'] = userslist
        # set the url to redirect to
        url = request.META.get('HTTP_REFERER')
        # redirect to the assignusers page
        return redirect(url)

# RemoveUserRangeCart
# removes the user from the add to range cart
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class RemoveUserRangeCart(View):
    # get the rangeurl and username
    def get(self, request, rangeurl, username):
        # check if user is valid
        get_object_or_404(User, username = username)
        # get the useremail
        useremail = User.objects.filter(username = username).values_list('email')[0][0]
        # create a new list
        userslist = []
        # check if userrangecart in session
        if 'userrangecart' in request.session:
            # get the userslist from session
            userslist = request.session['userrangecart']
        # check if the useremail in userslist
        if useremail in userslist:
            # remove the email from the list
            userslist.remove(useremail)
        # update the session with the new list
        request.session['userrangecart'] = userslist
        # set the url to redirect to
        url = request.META.get('HTTP_REFERER')
        # redirect to the assignusers page
        return redirect(url)

# UserRangeCommit
# saves the changes of the assigning of users into the database
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class UserRangeCommit(View):
    # get the rangeurl
    def get(self, request, rangeurl):
        # check if the userrangecart in session
        if 'userrangecart' in request.session:
            # set the userslist as the cart
            userslist = request.session['userrangecart']

        # forloop for each student in userslist
        for student in userslist:
            # get the user object
            studentid = User.objects.get(email = student)
            # get the range object
            rangeid = Range.objects.get(rangeurl = rangeurl)
            # get the current date
            datejoined = datetime.date.today()
            # create new rangestudents object
            obj = RangeStudents(studentID = studentid, rangeID = rangeid, dateJoined = datejoined)
            # save the object
            obj.save()

        messages.success(request, 'User(s) Successfully Added to Range')
        # set the url to redirect to
        url = "/teachers/rangemanagement/view/" + rangeurl
        # delete the session
        del request.session['userrangecart']
        # redirect to the range view
        return redirect(url)

# AssignGroup View
# assign groups a range
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AssignGroup(FilterView, ListView):
    # use the template teachers/assigngrouprange.html
    template_name = 'teachers/assigngrouprange.html'
    # set the contextobjectname as groupobject
    context_object_name = 'groupobject'
    # paginate by 10
    paginate_by = 10
    # set the filterset class as GroupFilter
    filterset_class = GroupFilter

    def get_queryset(self):
        # get the rangeid
        rangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        # get the groups in the range
        groupsinrange = RangeStudents.objects.filter(rangeID = rangeid, groupid__isnull=False).values_list('groupid')
        # get all the groups excluding the groups already in the ranges
        allgroups = Group.objects.exclude(groupid__in = groupsinrange).order_by('-lastmodifieddate')
        # set the self.allgroups for context below
        self.allgroups = allgroups
        # return all groups
        return allgroups

    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set the rangename as context
        context['rangename'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]
        # set the groupcount as context
        context['groupcount'] = len(self.allgroups)

        # check if there is a grouprangecart in session
        if "grouprangecart" in self.request.session:
            # get the cart
            cart = self.request.session.get('grouprangecart', {})
            # set cart as context
            context['cart'] = cart

        # return context
        return context

# AddGroupRangeCart
# add the group into the cart to be added
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddGroupRangeCart(View):
    # get the rangeurl and groupname
    def get(self, request, rangeurl, groupname):
        # check if the group is valid
        get_object_or_404(Group, groupname = groupname)
        # create a new list
        groupslist = []
        # check if there is a grouprangecart in session
        if 'grouprangecart' in request.session:
            # set the grouprangecart as list 
            groupslist = request.session['grouprangecart']
        # check if the groupname not in the grouplist
        if groupname not in groupslist:
            # if it isn't, add to the list
            groupslist.append(groupname)
        # set the new grouplist as the session
        request.session['grouprangecart'] = groupslist
        # set the url to be redirected to
        url = request.META.get('HTTP_REFERER')
        # redirect to the assigngroups page
        return redirect(url)

# RemoveGroupRangeCart View
# remove the group from the cart
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class RemoveGroupRangeCart(View):
    # get the rangeurl and groupname
    def get(self, request, rangeurl, groupname):
        # check if the groupname is valid
        get_object_or_404(Group, groupname = groupname)
        # create a new list
        groupslist = []
        # check if the grouprangecart in session
        if 'grouprangecart' in request.session:
            # if there is, set the session as list
            groupslist = request.session['grouprangecart']
        # check if the groupname is in the list
        if groupname in groupslist:
            # if it is, remove the group from the list
            groupslist.remove(groupname)
        # update the session
        request.session['grouprangecart'] = groupslist
        # set the url to redirect to
        url = request.META.get('HTTP_REFERER')
        # redirect to the assigngroups page
        return redirect(url)

# GroupRangeCommit
# save the cart of adding group to range into the database
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class GroupRangeCommit(View):
    # get the rangeurl
    def get(self, request, rangeurl):
        # get the students that are already in the range
        # get the rangeid
        rangeid = Range.objects.filter(rangeurl = rangeurl).values_list('rangeid')[0][0]
        # get the students in the range
        studentsinrange = RangeStudents.objects.filter(rangeID = rangeid)
        # create empty list
        rangestudentslist = []
        # forloop the students in the range
        for student in studentsinrange:
            # append the studentID to list
            rangestudentslist.append(student.studentID.email)

        # check if the grouprangecart in session
        if 'grouprangecart' in request.session:
            # set the grouplist as the session
            groupslist = request.session['grouprangecart']

        # forloop for each group
        for groupname in groupslist:
            # get the group id
            groupid = Group.objects.filter(groupname = groupname).values_list('groupid')[0][0]
            # get the students in the group
            studentsingroup = StudentGroup.objects.filter(groupid = groupid).exclude(studentid__in=rangestudentslist).values_list('studentid')

            # forloop the students in the students in group
            for students in studentsingroup:
                # get the student object
                studentobj = User.objects.get(email = students[0])
                # get the rangeid 
                rangeid = Range.objects.get(rangeurl = rangeurl)
                # get the current datetime
                datejoined = datetime.date.today()
                # get the group object
                groupobj = Group.objects.get(groupname = groupname)
                # before creating, we need to check if there is the student already in the range
                checkobj = RangeStudents.objects.filter(studentID = studentobj, rangeID = rangeid).count()
                print(checkobj)
                # check if count is 0
                if checkobj == 0:
                    # then can save
                    # create a new rangestudents object
                    obj = RangeStudents(studentID = studentobj, rangeID = rangeid, dateJoined = datejoined, groupid = groupobj)
                    # save the object
                    obj.save()

        messages.success(request, 'Group(s) Successfully Added to Range')
        # set the url to redirect to 
        url = "/teachers/rangemanagement/view/" + rangeurl 
        # delete session
        del request.session['grouprangecart']
        # redirect to the groupview
        return redirect(url)

# RemoveStudentFromRange View
# removes the student from a range
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class RemoveStudentFromRange(View):
    # get the rangeurl and username
    def get(self, request, rangeurl, username):
        # get the studentid
        studentid = User.objects.get(username = username)
        # get the rangeinstance
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        # get the selected user instances (hotfix incase a user has multiple ranges)
        selecteduser = RangeStudents.objects.filter(rangeID = rangeinstance, studentID = studentid)
        # use a forloop to loop the objects
        for selectedobject in selecteduser:
            # delete the objects
            selectedobject.delete()
        # delete the user
        # set the url to redirect to
        url = '/teachers/rangemanagement/view/' + rangeurl
        # redirect to the range view
        return redirect(url)

# RemoveGroupFromRange
# removes a whole group from a range
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class RemoveGroupFromRange(View):
    # get the rangeurl and groupname
    def get(self, request, rangeurl, groupname):
        # get the group object
        group = Group.objects.get(groupname = groupname)
        # get the group members id of the students in groups
        selectedgroupmembers = StudentGroup.objects.filter(groupid = group).values_list('studentid')
        # get the range instance
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        # get the students in range
        rangestudents = RangeStudents.objects.filter(rangeID = rangeinstance, groupid = group).values_list('studentID')
        # create new list
        studentlist = []
        # forloop each student in the range
        for student in rangestudents:
            # get the student
            student = student[0]
            # append the student in the list
            studentlist.append(student)

        # forloop the students in the groupmembers
        for student in selectedgroupmembers:
            student = student[0]
            # check if the student in the list
            if student in studentlist:
                # get the studented user object
                selecteduser = RangeStudents.objects.get(rangeID = rangeinstance, studentID = student, groupid = group)
                # delete the object
                selecteduser.delete()

        # set the url to redirect to 
        url = '/teachers/rangemanagement/view/' + rangeurl
        # redirect to the groupvieww
        return redirect(url)

# CreateQuestion View
# this view is the base view for creating questions
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class CreateQuestion(ListView, ModelFormMixin):
    # use the template teachers/addquestion.html
    template_name = 'teachers/addquestion.html'
    # set the contextobjectname to currentmarks
    context_object_name = 'currentmarks'
    # use the Questions model
    model = Questions
    # set the formclass to QuestionForm
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # if the form is valid, save the form
            # return question object and the topic name
            question, topicname = self.form.save()
            # need to get the range instance to add the score
            rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
            # get the points so that can add the score            
            points = request.POST.get('points',' ')
            # get the registryid so that we can create the image later
            registryid = self.request.POST.get('registryid','')
            # get the questionid of the current question for the image creation
            questionid = question.questionid
            # get the question instance
            questioninstance = Questions.objects.get(questionid = questionid)
            # get the range url
            rangeurl = self.kwargs['rangeurl']
            # get the current range score to append the score
            currentrangescore = rangeinstance.maxscore
            # check if the score is None
            if currentrangescore is None:
                # if it is, add the points to 0
                currentrangescore = 0 + int(points)
            else: 
                # else, add the points to the current points
                currentrangescore += int(points)
            
            # set the maxscore in the object
            rangeinstance.maxscore = currentrangescore
            # save the object
            rangeinstance.save()

            # check if the question uses docker
            if (request.POST.get('usedocker') == 'True'):
                # if it is, declare imageid as registryid (to not confuse yourself)
                imageid = registryid
                # call the createimage class
                error = CreateImage.get(self, request, rangeurl, questionid, imageid)
                # check if there is an error
                if error is not 0:
                    # if there is an error, show an error message
                   return HttpResponse('ERROR')

            # return to the form        
            return ListView.get(self, request, *args, **kwargs)
        else:
            # check if the user wants to add a new topic
            if (request.POST.get('newtopicname')):
                # conver the topicname to lower
                newtopicname = request.POST.get('newtopicname')
                # call the db to filter if there is a similar topic
                checkdb = QuestionTopic.objects.filter(topicname__iexact = newtopicname)
                # check if theres any entries
                if len(checkdb) == 0:
                    # if no entries, create a new questiontopic object
                    questiontopicobj = QuestionTopic(topicname = newtopicname)
                    # save the object
                    questiontopicobj.save()
                    # declare a message of success
                    messages.success(request, 'New Question Topic Created ')
                else:
                    # if there is an entry, declare a message to feedback to the user
                    messages.error(request, 'Topic Name Already Exists in Database ')
                # return to the form
                return ListView.get(self, request, *args, **kwargs)

            else:
                # return to the form if there is an error in the form
                return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        # get the currentmarks in the range
        currentmarks =  Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('maxscore')[0][0]
        # return currentmarks
        return currentmarks

    def get_form_kwargs(self):
        # call super
        kwargs = super(CreateQuestion, self).get_form_kwargs()
        # get the range instance
        rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
        # set the request and rangeinstance as kwargs
        kwargs.update({'request': self.request, 'rangeinstance': rangeinstance})
        # return kwargs
        return kwargs

    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set the questiontypechoices as context
        context['questiontypechoices'] = QUESTION_TYPE_CHOICES
        # set the rangename as context
        context['rangename'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]
        # set the questiontopics as context
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        context['questiontopic'] = questiontopic
        #return context
        return context

# CreateFLQuestion View
# This view is specifically to create flag type questions
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class CreateFLQuestion(ListView, ModelFormMixin):
    # use the teacheres/addflquestion.html template
    template_name = 'teachers/addflquestion.html'
    # set contextobjectname as currentmarks
    context_object_name = 'currentmarks'
    # use Questions mode
    model = Questions
    # set formclass as QuestionForm
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # if the form is valid, save the form
            # return question object and the topic name
            question, topicname = self.form.save()
            # need to get the range instance to add the score
            rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
            # get the points so that can add the score            
            points = request.POST.get('points',' ')
            # get the registryid so that we can create the image later
            registryid = self.request.POST.get('registryid','')
            # get the questionid of the current question for the image creation
            questionid = question.questionid
            # get the question instance
            questioninstance = Questions.objects.get(questionid = questionid)
            # get the range url
            rangeurl = self.kwargs['rangeurl']
            # get the current range score to append the score
            currentrangescore = rangeinstance.maxscore
            # check if the score is None
            if currentrangescore is None:
                # if it is, add the points to 0
                currentrangescore = 0 + int(points)
            else: 
                # else, add the points to the current points
                currentrangescore += int(points)
            
            # set the maxscore in the object
            rangeinstance.maxscore = currentrangescore
            # save the object
            rangeinstance.save()

            # check if the question uses docker
            if (request.POST.get('usedocker') == 'True'):
                # if it is, declare imageid as registryid (to not confuse yourself)
                imageid = registryid
                # call the createimage class
                error = CreateImage.get(self, request, rangeurl, questionid, imageid)
                # check if there is an error
                if error is not 0:
                    # if there is an error, show an error message
                   return HttpResponse('ERROR')

            # return to the form        
            return ListView.get(self, request, *args, **kwargs)
        else:
            # check if the user wants to add a new topic
            if (request.POST.get('newtopicname')):
                # conver the topicname to lower
                newtopicname = request.POST.get('newtopicname')
                # call the db to filter if there is a similar topic
                checkdb = QuestionTopic.objects.filter(topicname__iexact = newtopicname)
                # check if theres any entries
                if len(checkdb) == 0:
                    # if no entries, create a new questiontopic object
                    questiontopicobj = QuestionTopic(topicname = newtopicname)
                    # save the object
                    questiontopicobj.save()
                    # declare a message of success
                    messages.success(request, 'New Question Topic Created ')
                else:
                    # if there is an entry, declare a message to feedback to the user
                    messages.error(request, 'Topic Name Already Exists in Database ')
                # return to the form
                return ListView.get(self, request, *args, **kwargs)

            else:
                # return to the form if there is an error in the form
                return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        # get the currentmarks in the range
        currentmarks =  Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('maxscore')[0][0]
        # return currentmarks
        return currentmarks

    def get_form_kwargs(self):
        # call super
        kwargs = super(CreateFLQuestion, self).get_form_kwargs()
        # get the range instance
        rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
        # set the request and rangeinstance as kwargs
        kwargs.update({'request': self.request, 'rangeinstance': rangeinstance})
        # return kwargs
        return kwargs

    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set the questiontypechoices as context
        context['questiontypechoices'] = QUESTION_TYPE_CHOICES
        # set the rangename as context
        context['rangename'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]
        # set the questiontopics as context
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        context['questiontopic'] = questiontopic
        #return context
        return context

# CreateMCQQuestion View
# This view is to specifically create MCQ Questions
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class CreateMCQQuestion(ListView, ModelFormMixin):
    # use the template teachers/addmcqquestion.html
    template_name = 'teachers/addmcqquestion.html'
    # set contextobjectname as currentmarks
    context_object_name = 'currentmarks'
    # use Questions model
    model = Questions
    # set formclass as QuestionForm
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # if the form is valid, save the form
            # return question object and the topic name
            question, topicname = self.form.save()
            # need to get the range instance to add the score
            rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
            # get the points so that can add the score            
            points = request.POST.get('points',' ')
            # get the registryid so that we can create the image later
            registryid = self.request.POST.get('registryid','')
            # get the questionid of the current question for the image creation
            questionid = question.questionid
            # get the question instance
            questioninstance = Questions.objects.get(questionid = questionid)
            # get the range url
            rangeurl = self.kwargs['rangeurl']
            # get the current range score to append the score
            currentrangescore = rangeinstance.maxscore
            # check if the score is None
            if currentrangescore is None:
                # if it is, add the points to 0
                currentrangescore = 0 + int(points)
            else: 
                # else, add the points to the current points
                currentrangescore += int(points)
            
            # set the maxscore in the object
            rangeinstance.maxscore = currentrangescore
            # save the object
            rangeinstance.save()

            # next, we need to get all the mcq choices
            optionone = request.POST.get('optionone',' ')
            optiontwo = request.POST.get('optiontwo',' ')
            optionthree = request.POST.get('optionthree',' ')
            optionfour = request.POST.get('optionfour',' ')

            mcqobject = MCQOptions(optionone = optionone, optiontwo = optiontwo, optionthree = optionthree, optionfour = optionfour, questionid = questioninstance)
            mcqobject.save()

            # check if the question uses docker
            if (request.POST.get('usedocker') == 'True'):
                # if it is, declare imageid as registryid (to not confuse yourself)
                imageid = registryid
                # call the createimage class
                error = CreateImage.get(self, request, rangeurl, questionid, imageid)
                # check if there is an error
                if error is not 0:
                    # if there is an error, show an error message
                   return HttpResponse('ERROR')

            # return to the form        
            return ListView.get(self, request, *args, **kwargs)
        else:
            # check if the user wants to add a new topic
            if (request.POST.get('newtopicname')):
                # conver the topicname to lower
                newtopicname = request.POST.get('newtopicname')
                # call the db to filter if there is a similar topic
                checkdb = QuestionTopic.objects.filter(topicname__iexact = newtopicname)
                # check if theres any entries
                if len(checkdb) == 0:
                    # if no entries, create a new questiontopic object
                    questiontopicobj = QuestionTopic(topicname = newtopicname)
                    # save the object
                    questiontopicobj.save()
                    # declare a message of success
                    messages.success(request, 'New Question Topic Created ')
                else:
                    # if there is an entry, declare a message to feedback to the user
                    messages.error(request, 'Topic Name Already Exists in Database ')
                # return to the form
                return ListView.get(self, request, *args, **kwargs)

            else:
                # return to the form if there is an error in the form
                return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        # get the currentmarks in the range
        currentmarks =  Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('maxscore')[0][0]
        # return currentmarks
        return currentmarks

    def get_form_kwargs(self):
        # call super
        kwargs = super(CreateMCQQuestion, self).get_form_kwargs()
        # get the range instance
        rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
        # set the request and rangeinstance as kwargs
        kwargs.update({'request': self.request, 'rangeinstance': rangeinstance})
        # return kwargs
        return kwargs

    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set the questiontypechoices as context
        context['questiontypechoices'] = QUESTION_TYPE_CHOICES
        # set the rangename as context
        context['rangename'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]
        # set the questiontopics as context
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        context['questiontopic'] = questiontopic
        #return context
        return context

# CreateSAQuestion View
# This view is to specifically create short answer questions
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class CreateSAQuestion(ListView, ModelFormMixin):
    # use template teachers/addsaquestion.html
    template_name = 'teachers/addsaquestion.html'
    # set contextobjectname as currentmarks
    context_object_name = 'currentmarks'
    # use Questions model
    model = Questions
    # set formclass as QuestionForm
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # if the form is valid, save the form
            # return question object and the topic name
            question, topicname = self.form.save()
            # need to get the range instance to add the score
            rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
            # get the points so that can add the score            
            points = request.POST.get('points',' ')
            # get the registryid so that we can create the image later
            registryid = self.request.POST.get('registryid','')
            # get the questionid of the current question for the image creation
            questionid = question.questionid
            # get the question instance
            questioninstance = Questions.objects.get(questionid = questionid)
            # get the range url
            rangeurl = self.kwargs['rangeurl']
            # get the current range score to append the score
            currentrangescore = rangeinstance.maxscore
            # check if the score is None
            if currentrangescore is None:
                # if it is, add the points to 0
                currentrangescore = 0 + int(points)
            else: 
                # else, add the points to the current points
                currentrangescore += int(points)
            
            # set the maxscore in the object
            rangeinstance.maxscore = currentrangescore
            # save the object
            rangeinstance.save()

            # check if the question uses docker
            if (request.POST.get('usedocker') == 'True'):
                # if it is, declare imageid as registryid (to not confuse yourself)
                imageid = registryid
                # call the createimage class
                error = CreateImage.get(self, request, rangeurl, questionid, imageid)
                # check if there is an error
                if error is not 0:
                    # if there is an error, show an error message
                   return HttpResponse('ERROR')

            # return to the form        
            return ListView.get(self, request, *args, **kwargs)
        else:
            # check if the user wants to add a new topic
            if (request.POST.get('newtopicname')):
                # conver the topicname to lower
                newtopicname = request.POST.get('newtopicname')
                # call the db to filter if there is a similar topic
                checkdb = QuestionTopic.objects.filter(topicname__iexact = newtopicname)
                # check if theres any entries
                if len(checkdb) == 0:
                    # if no entries, create a new questiontopic object
                    questiontopicobj = QuestionTopic(topicname = newtopicname)
                    # save the object
                    questiontopicobj.save()
                    # declare a message of success
                    messages.success(request, 'New Question Topic Created ')
                else:
                    # if there is an entry, declare a message to feedback to the user
                    messages.error(request, 'Topic Name Already Exists in Database ')
                # return to the form
                return ListView.get(self, request, *args, **kwargs)

            else:
                # return to the form if there is an error in the form
                return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        # get the currentmarks in the range
        currentmarks =  Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('maxscore')[0][0]
        # return currentmarks
        return currentmarks

    def get_form_kwargs(self):
        # call super
        kwargs = super(CreateSAQuestion, self).get_form_kwargs()
        # get the range instance
        rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
        # set the request and rangeinstance as kwargs
        kwargs.update({'request': self.request, 'rangeinstance': rangeinstance})
        # return kwargs
        return kwargs

    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set the questiontypechoices as context
        context['questiontypechoices'] = QUESTION_TYPE_CHOICES
        # set the rangename as context
        context['rangename'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]
        # set the questiontopics as context
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        context['questiontopic'] = questiontopic
        #return context
        return context

# CreateOEQuestion View
# This view is to specifically create open ended answer questions
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class CreateOEQuestion(ListView, ModelFormMixin):
    # use template teachers/addoequestion.html
    template_name = 'teachers/addoequestion.html'
    # set contextobjectname as currentmarks
    context_object_name = 'currentmarks'
    # use Questions model
    model = Questions
    # set formclass as QuestionForm
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # if the form is valid, save the form
            # return question object and the topic name
            question, topicname = self.form.save()
            # need to get the range instance to add the score
            rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
            # get the points so that can add the score            
            points = request.POST.get('points',' ')
            # get the registryid so that we can create the image later
            registryid = self.request.POST.get('registryid','')
            # get the questionid of the current question for the image creation
            questionid = question.questionid
            # get the question instance
            questioninstance = Questions.objects.get(questionid = questionid)
            # get the range url
            rangeurl = self.kwargs['rangeurl']
            # get the current range score to append the score
            currentrangescore = rangeinstance.maxscore
            # check if the score is None
            if currentrangescore is None:
                # if it is, add the points to 0
                currentrangescore = 0 + int(points)
            else: 
                # else, add the points to the current points
                currentrangescore += int(points)
            
            # set the maxscore in the object
            rangeinstance.maxscore = currentrangescore
            # save the object
            rangeinstance.save()

            # check if the question uses docker
            if (request.POST.get('usedocker') == 'True'):
                # if it is, declare imageid as registryid (to not confuse yourself)
                imageid = registryid
                # call the createimage class
                error = CreateImage.get(self, request, rangeurl, questionid, imageid)
                # check if there is an error
                if error is not 0:
                    # if there is an error, show an error message
                   return HttpResponse('ERROR')

            # return to the form        
            return ListView.get(self, request, *args, **kwargs)
        else:
            # check if the user wants to add a new topic
            if (request.POST.get('newtopicname')):
                # convert the topicname to lower
                newtopicname = request.POST.get('newtopicname')
                # call the db to filter if there is a similar topic
                checkdb = QuestionTopic.objects.filter(topicname__iexact = newtopicname)
                # check if theres any entries
                if len(checkdb) == 0:
                    # if no entries, create a new questiontopic object
                    questiontopicobj = QuestionTopic(topicname = newtopicname)
                    # save the object
                    questiontopicobj.save()
                    # declare a message of success
                    messages.success(request, 'New Question Topic Created ')
                else:
                    # if there is an entry, declare a message to feedback to the user
                    messages.error(request, 'Topic Name Already Exists in Database ')
                # return to the form
                return ListView.get(self, request, *args, **kwargs)

            else:
                # return to the form if there is an error in the form
                return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        # get the currentmarks in the range
        currentmarks =  Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('maxscore')[0][0]
        # return currentmarks
        return currentmarks

    def get_form_kwargs(self):
        # call super
        kwargs = super(CreateOEQuestion, self).get_form_kwargs()
        # get the range instance
        rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
        # set the request and rangeinstance as kwargs
        kwargs.update({'request': self.request, 'rangeinstance': rangeinstance})
        # return kwargs
        return kwargs

    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set the questiontypechoices as context
        context['questiontypechoices'] = QUESTION_TYPE_CHOICES
        # set the rangename as context
        context['rangename'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]
        # set the questiontopics as context
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        context['questiontopic'] = questiontopic
        #return context
        return context

# CreateTFQuestion View
# This view is to specifically create true or false questions
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class CreateTFQuestion(ListView, ModelFormMixin):
    # use the template teachers/addtfquestion.html
    template_name = 'teachers/addtfquestion.html'
    # set contextobjectname as currentmarks
    context_object_name = 'currentmarks'
    # use Questions model
    model = Questions
    # set formclass as QuestionForm
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # if the form is valid, save the form
            # return question object and the topic name
            question, topicname = self.form.save()
            # need to get the range instance to add the score
            rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
            # get the points so that can add the score            
            points = request.POST.get('points',' ')
            # get the registryid so that we can create the image later
            registryid = self.request.POST.get('registryid','')
            # get the questionid of the current question for the image creation
            questionid = question.questionid
            # get the question instance
            questioninstance = Questions.objects.get(questionid = questionid)
            # get the range url
            rangeurl = self.kwargs['rangeurl']
            # get the current range score to append the score
            currentrangescore = rangeinstance.maxscore
            # check if the score is None
            if currentrangescore is None:
                # if it is, add the points to 0
                currentrangescore = 0 + int(points)
            else: 
                # else, add the points to the current points
                currentrangescore += int(points)
            
            # set the maxscore in the object
            rangeinstance.maxscore = currentrangescore
            # save the object
            rangeinstance.save()

            # check if the question uses docker
            if (request.POST.get('usedocker') == 'True'):
                # if it is, declare imageid as registryid (to not confuse yourself)
                imageid = registryid
                # call the createimage class
                error = CreateImage.get(self, request, rangeurl, questionid, imageid)
                # check if there is an error
                if error is not 0:
                    # if there is an error, show an error message
                   return HttpResponse('ERROR')

            # return to the form        
            return ListView.get(self, request, *args, **kwargs)
        else:
            # check if the user wants to add a new topic
            if (request.POST.get('newtopicname')):
                # conver the topicname to lower
                newtopicname = request.POST.get('newtopicname')
                # call the db to filter if there is a similar topic
                checkdb = QuestionTopic.objects.filter(topicname__iexact = newtopicname)
                # check if theres any entries
                if len(checkdb) == 0:
                    # if no entries, create a new questiontopic object
                    questiontopicobj = QuestionTopic(topicname = newtopicname)
                    # save the object
                    questiontopicobj.save()
                    # declare a message of success
                    messages.success(request, 'New Question Topic Created ')
                else:
                    # if there is an entry, declare a message to feedback to the user
                    messages.error(request, 'Topic Name Already Exists in Database ')
                # return to the form
                return ListView.get(self, request, *args, **kwargs)

            else:
                # return to the form if there is an error in the form
                return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        # get the currentmarks in the range
        currentmarks =  Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('maxscore')[0][0]
        # return currentmarks
        return currentmarks

    def get_form_kwargs(self):
        # call super
        kwargs = super(CreateTFQuestion, self).get_form_kwargs()
        # get the range instance
        rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
        # set the request and rangeinstance as kwargs
        kwargs.update({'request': self.request, 'rangeinstance': rangeinstance})
        # return kwargs
        return kwargs

    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set the questiontypechoices as context
        context['questiontypechoices'] = QUESTION_TYPE_CHOICES
        # set the rangename as context
        context['rangename'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]
        # set the questiontopics as context
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        context['questiontopic'] = questiontopic
        #return context
        return context

# ActivateRange View
# This view is to activate the range after the teacher clicks the activate button
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ActivateRange(View):
    # gets the rangeurl
    def get(self, request, rangeurl):
        # get the range object using rangeurl
        rangeobject = Range.objects.get(rangeurl = rangeurl)
        # set the rangeactive to True
        rangeobject.rangeactive = True
        # set the manualactive to True
        rangeobject.manualactive = True
        # set the manualdeactive to False
        rangeobject.manualdeactive = False
        # save the rangeobject
        rangeobject.save()
        # redirect back to the view
        return redirect('../')

# DeactivateRange View
# This view is to deactivate the range after the teacher clicks the deactivate button
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DeactivateRange(View):
    # get the rangeurl
    def get(self, request, rangeurl):
        # get the rangeobject using rangeurl
        rangeobject = Range.objects.get(rangeurl = rangeurl)
        # set the rangeactive to False
        rangeobject.rangeactive = False
        # set the manualdeactive to True
        rangeobject.manualdeactive = True
        # set the manualactive to False
        rangeobject.manualactive = False
        # save the rangeobject
        rangeobject.save()
        # redirect back to view
        return redirect('../')

# DownloadCSVTemplate View
# This will generate the CSV template for download
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DownloadCSVTemplate(View):
    def get(self, request, *args, **kwargs):
        # set the httpresponse content type to csv
        response = HttpResponse(content_type='text/csv')
        # set the filename
        response['Content-Disposition'] = 'attachment; filename="template.csv"'
        # use the writer to write the content
        writer = csv.writer(response)
        # use the writer to write the rows into the template
        writer.writerow(['QuestionType', 'Topic Name', 'Title', 'Text', 'Answer', 'Hint', 'Marks', 'Hint Penalty', 'Use Docker', 'Registry ID', 'Option One', 'Option Two', 'Option Three', 'Option Four'])
        # return response
        return response

# ImportCSV View
# This will receive the CSV from the user and store into the database
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ImportCSV(View):
    def get(self, request, *args, **kwargs):
        # get the rangeurl
        rangeurl = self.kwargs['rangeurl']
        # set the redirect
        redirect = ('/teachers/rangemanagement/view/' + str(rangeurl))
        # return to the importquestions page
        return render(request, 'teachers/importqns.html',  {"redirect": redirect})

    def post(self, request, *args, **kwargs):
        # get the rangeurl
        rangeurl = self.kwargs['rangeurl']
        # set the redirect
        redirect = ('/teachers/rangemanagement/view/' + str(rangeurl))
        # create empty dataset
        data = {}
        try:
            # request the file
            csv_file = request.FILES["qnsfile"]
            # check if the file is a csv file
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return render(request, 'teachers/importqns.html')
            #if file is too large, return
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return render(request, 'teachers/importqns.html')
            
            # read with utf-8
            file_data = csv_file.read().decode("utf-8")		
            # split the lines
            lines = file_data.split("\n")

            #loop over the lines and save them in db. If error , store as string and then display
            x = 0
            for line in lines:
                if line and x > 0:
                    marks=0
                    fields = line.split(",")

                    data_dict = {}
                    questiontype = fields[1]
                    topicname = fields[2]
                    title = fields[3]
                    text = fields[4]
                    answer = fields[5]
                    hint = fields[6]
                    marks = fields[7]
                    hintpenalty = fields[8]
                    createdby = fields[9]
                    if createdby == '':
                        createdby = self.request.user
                    usedocker = fields[10]
                    registryid = fields[11]

                    docker = False
                    if usedocker == 1:
                        docker = True
                    elif usedocker == 0:
                        docker = False
                        
                    if answer == 'TRUE':
                        answer = 'True'
                    if answer == 'FALSE':
                        answer = 'False'

                    datetimenow = datetime.datetime.now()
                    username = self.request.user
                    userinstance = User.objects.get(username = username)
                    rangeinstance = Range.objects.get(rangeurl = rangeurl)

                    try:
                        questiontopicinstance = QuestionTopic.objects.get(topicname = topicname)
                    except QuestionTopic.DoesNotExist:
                        newquestiontopic = QuestionTopic(topicname = topicname)
                        newquestiontopic.save()
                        questiontopicinstance = QuestionTopic.objects.all().order_by('-topicid')[0]

                    question_obj = Questions(topicid = questiontopicinstance, questiontype = questiontype, title = title, text = text, hint = hint, points = marks, answer = answer, usedocker = docker, datecreated = datetimenow, createdby = userinstance, rangeid = rangeinstance, hintpenalty = hintpenalty, registryid = registryid, isarchived = 0)
                    question_obj.save()
                    
                    if str(questiontype) == 'MCQ':
                        questioninstance = Questions.objects.all().order_by('-questionid')[0]
                        optionone = fields[11]
                        optiontwo = fields[12]
                        optionthree = fields[13]
                        optionfour = fields[14]
                        mcqoptions_obj = MCQOptions(optionone = optionone, optiontwo = optiontwo, optionthree = optionthree, optionfour = optionfour, questionid = questioninstance)
                        mcqoptions_obj.save()
                    
                    rangeinstance = Range.objects.get(rangeurl = rangeurl)
                    updatedmarks = rangeinstance.maxscore + int(marks)
                    rangeinstance.maxscore = updatedmarks
                    rangeinstance.save()
                x = x + 1

        except Exception as e:
            logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
            messages.error(request,"Unable to upload file. "+repr(e))
            return render(request, 'teachers/importqns.html', {"redirect": redirect})

        messages.success(request, 'Questions Successfully Imported From CSV File')    
        return render(request, 'teachers/importqns.html', {"redirect": redirect})


@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ExportCSV(View):
    def get(self, request, *args, **kwargs):
        rangeurl = self.kwargs['rangeurl']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        rangeid = rangeinstance.rangeid
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="questions.csv"'

        writer = csv.writer(response)
        writer.writerow(['Question ID', 'QuestionType', 'Topic Name', 'Title', 'Text', 'Answer', 'Hint', 'Marks', 'Hint Penalty', 'Created By', 'Use Docker', 'Registry ID', 'Option One', 'Option Two', 'Option Three', 'Option Four'])

        questions = Questions.objects.filter(rangeid = rangeinstance).values_list('questionid', 'questiontype', 'topicid', 'title', 'text', 'answer', 'hint', 'points', 'hintpenalty', 'createdby', 'usedocker' ,'registryid')
        for qns in questions:
            topicname = QuestionTopic.objects.get(topicid = qns[2])
            if qns[1] == 'MCQ':
                questioninstance = Questions.objects.get(questionid = qns[0])
                mcqoptionsinstance = MCQOptions.objects.get(questionid = questioninstance)
                writer.writerow([qns[0], qns[1], topicname.topicname, qns[3], qns[4], qns[5], qns[6], qns[7], qns[8], qns[9], qns[10], qns[11], mcqoptionsinstance.optionone, mcqoptionsinstance.optiontwo,  mcqoptionsinstance.optionthree,  mcqoptionsinstance.optionfour])

            else:
                writer.writerow([qns[0], qns[1], topicname.topicname, qns[3], qns[4], qns[5], qns[6], qns[7], qns[8], qns[9], qns[10], qns[11], '-', '-', '-', '-'])
                
        return response

# IsOpen View
# This will allow the teacher to set whether the rangecode can be used to add the range
# whether the range 'IsOpen' to be added by range code
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class IsOpen(View):
    def get(self, request, *args, **kwargs):
        # get the current rangeurl
        rangeurl = self.kwargs['rangeurl']
        # get the range object
        selectedrangeinstance = Range.objects.get(rangeurl = rangeurl)
        # set the isopen flag to 1
        selectedrangeinstance.isopen = 1
        # save the range object
        selectedrangeinstance.save()

        # set the url to return to
        returnurl = ('/teachers/rangemanagement/view/' + str(rangeurl))
        # redirect to the range view
        return HttpResponseRedirect(returnurl)

# IsClose View
# Opposite of the IsOpen View, allow the teacher to disable adding range by range code
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class IsClose(View):
    def get(self, request, *args, **kwargs):
        # get the current rangeurl
        rangeurl = self.kwargs['rangeurl']
        # get the range object
        selectedrangeinstance = Range.objects.get(rangeurl = rangeurl)
        # set the isopen flag to 0
        selectedrangeinstance.isopen = 0
        # save the rangeobject
        selectedrangeinstance.save()
        # set the url to redirect to
        returnurl = ('/teachers/rangemanagement/view/' + str(rangeurl))
        # redirect to the group view
        return HttpResponseRedirect(returnurl)

#################################################################
# The following will support the question management functionalities of Ostrich

# QuestionManagement View
# Displays all the (active) questions as a table
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class QuestionManagement(FilterView, ListView):
    # use the template teachers/questionmanagement.html
    template_name = 'teachers/questionmanagement.html'
    # set contextobjectname as questions
    context_object_name = 'questions'
    # paginate by 10
    paginate_by = 10
    # use the QuestionFilter
    filterset_class = QuestionFilter

    def get_queryset(self):
        # query all the questions that are not archived
        questions = Questions.objects.filter(isarchived = 0)
        # return queryset
        return questions

    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # set the topics as context
        context['topics'] = QuestionTopic.objects.all()
        # set the currentuser as context
        context['creator'] = self.request.user
        # return the context
        return context

# ArchiveQuestioninManagement View
# This view will archive the question selected by the teacher
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ArchiveQuestioninManagement(View):
    # get the questionid
    def get(self, request, questionid):
        # get the question object using the questionid
        questioninstance = Questions.objects.get(questionid = questionid)
        # set the archived flag to 1
        questioninstance.isarchived = 1
        # save the object
        questioninstance.save()
        # get the previous url
        previousurl = request.META.get('HTTP_REFERER')
        # redirect back
        return redirect(previousurl)

# ArchivedQuestionManagement
# displays all the archived questions
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ArchivedQuestionManagement(FilterView, ListView):
    # use the template teachers/archivedquestionmanagement.html
    template_name = 'teachers/archivedquestionmanagement.html'
    # set the contextobjectname as questions
    context_object_name = 'questions'
    # paginate by 10
    paginate_by = 10
    # use the QuestionFilter
    filterset_class = QuestionFilter

    def get_queryset(self):
        # query all the questions that are archived
        questions = Questions.objects.filter(isarchived = 1)
        # return queryset
        return questions

    def get_context_data(self, **kwargs):
        # call super 
        context = super().get_context_data(**kwargs)
        # set the question topics as context
        context['topics'] = QuestionTopic.objects.all()
        # set the createdby as context
        context['createdby'] = self.request.user
        # return context
        return context

# UnarchiveFromQuestionmanagement View
# This will unarchive the question selected by the teacher
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class UnarchiveFromQuestionManagement(View):
    def get(self, request, *args, **kwargs):
        # get the questionid 
        selectedquestionid = self.kwargs['questionid']
        # get the question object
        selectedquestioninstance = Questions.objects.get(questionid = selectedquestionid)
        # set the archived flag to 0
        selectedquestioninstance.isarchived = 0
        # save the question object
        selectedquestioninstance.save()
        # get the previous url
        previousurl = request.META.get('HTTP_REFERER')
        # redirect back
        return redirect(previousurl)

# ViewQuestion View
# teachers can view the question and all its details with this view
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ViewQuestion(ListView):
    # use the template teachers/viewquestion.html
    template_name = 'teachers/viewquestion.html'
    # set the contextobjectname as result
    context_object_name = 'result'
    
    def get_queryset(self):
        # get the question object
        selectedquestion = Questions.objects.get(questionid = self.kwargs['questionid'])
        # return the object
        return selectedquestion
    
    def get_context_data(self, **kwargs):
        # call super
        context = super().get_context_data(**kwargs)
        # get the question object
        selectedquestion = Questions.objects.get(questionid = self.kwargs['questionid'])
        # get all the questiontopics
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        # set the questiontopics as context
        context['questiontopic'] = questiontopic
        # get the question topic id
        getthistopicid = (selectedquestion.topicid.topicid)
        # get the questiontopic name
        currentquestiontopicname = QuestionTopic.objects.get(topicid=getthistopicid)
        # set the questiontopic name as context
        context['currentquestiontopicname'] = currentquestiontopicname.topicname
        # set the question type choices as context
        context['questiontypechoices'] = QUESTION_TYPE_CHOICES
        # set the archived flag as context
        context['check'] = selectedquestion.isarchived
        # set the question points as context
        context['points'] = selectedquestion.points

        # check if the question is MCQ
        if selectedquestion.questiontype == 'MCQ':
            # get the mcqoptions object
            mcqoptions_obj = MCQOptions.objects.get(questionid = selectedquestion)
            # set all the options as context
            context['optionone'] = mcqoptions_obj.optionone
            context['optiontwo'] = mcqoptions_obj.optiontwo
            context['optionthree'] = mcqoptions_obj.optionthree
            context['optionfour'] = mcqoptions_obj.optionfour

        # return context
        return context

# DeleteQuestion
# allows the teacher to delete question from the archived question management
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DeleteQuestion(View):
    # get the rangeurl and questionid
    def get(self, request, questionid):
        # get the prevoius url
        previousurl = request.META.get('HTTP_REFERER')
        # get the selected question instance object
        selectedquestioninstance = Questions.objects.get(questionid = questionid)
        # get the questionid
        # check if its an mcq question
        questiontype = selectedquestioninstance.questiontype
        if questiontype == 'MCQ':
            questionid = selectedquestioninstance.questionid
            mcqoptionsobject = MCQOptions.objects.get(questionid = questionid)
            mcqoptionsobject.delete()
        # delete object
        selectedquestioninstance.delete()
        # redirect to the previous url
        return redirect(previousurl)

#################################################################
# The following will support the docker management 

# Docker Management
# Lists all the dockers currently being opened, allows the teachers to manually kill dockers
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DockerManagement(ListView):
    # use template teachers/dockermanagement.html
    template_name = 'teachers/dockermanagement.html'
    # set context object name as dockerobjects
    context_object_name = 'dockerobjects'
    # paginate_by = 10
    paginate_by = 20

    def get_queryset(self):
        # get the queryset of all the opened dockers
        dockers = UnavailablePorts.objects.all()
        # return the queryset
        return dockers

# AdminDockerKill
# kills the selected container
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AdminDockerKill(View):
    def get(self, request, containername):
        # get the port number that the teacher is trying to kill
        portnumber = UnavailablePorts.objects.filter(containername = containername).values_list('portnumber')[0][0]
        # determine which server it is from the port number
        if int(portnumber) >= 9051:
            # if it is more than 9051 inclusivve, it is the docker server
            server = '192.168.100.42'
        else:
            # else it is the web server
            server = '192.168.100.43'
        # delete old port if existing
        endpoint = 'http://' + server + ':8051/containers/' + containername + '?force=True'
        response = requests.delete(endpoint)
        # need to delete from containernamed
        deleteportsdb = UnavailablePorts.objects.filter(containername = containername)
        # delete the entry
        deleteportsdb.delete()
        # redirect back to dockermanagement
        return redirect('/teachers/dockermanagement/')

#################################################################
# The following will support the teacher management functionalities

# Teacher View
# lists all the teachers accounts
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class TeacherView(FilterView, ListView):
    # use the template teachers/teachermanagement.html
    template_name = 'teachers/teachermanagement.html'
    # set the contextobjectname as teacherobjects
    context_object_name = 'teacherobjects'
    # use the TeacherFilter
    filterset_class = TeacherFilter

    def get_queryset(self):
        # get all the teachers
        allteachers = User.objects.filter(is_staff = 1)
        # return queryset
        return allteachers

# AddTeacher View
# allows teachers to add more teachers
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddTeacher(ListView, ModelFormMixin):
    # use template teachers/addteacher.html
    template_name = 'teachers/addteacher.html'
    # set contextobjectname as teachersobject
    context_object_name = 'teachersobject'
    # use User model
    model = User
    # use the TeacherRegisterForm
    form_class = TeacherRegisterForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # save the form
            self.form.save(request)
            # set the message
            messages.success(request, 'Teacher account successfully created')
            # direct to teacher
            return redirect('/teachers/teachermanagement/')

        else:
            return ListView.get(self, request, *args, **kwargs)

#################################################################
# The following will support the class management functionalities

# ClassView
# list all the classes in the class management
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ClassView(FilterView, ListView):
    # use template teachers/classmanagement.html
    template_name = 'teachers/classmanagement.html'
    # set contextobjectname as classobjects
    context_object_name = 'classobjects'
    # use ClassFilter
    filterset_class = ClassFilter

    def get_queryset(self):
        # get the user classes
        alluserclass = UserClass.objects.all()
        return alluserclass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # set the number of users as context
        context['classcount'] = UserClass.objects.all().count()
        # return context
        return context

# AddClass View
# form to add new class into database
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddClass(ListView, ModelFormMixin):
    # use template teachers/addclass.html
    template_name = 'teachers/addclass.html'
    # set contextobjectname as classobjects
    context_object_name = 'classobjects'
    # use UserClass model
    model = UserClass
    # use ClassForm
    form_class = ClassForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # save the form
            self.form.save()
            # set the message
            messages.success(request, 'New Class Added Successfuly')
            # return to the 
            return redirect('/teachers/classmanagement/')
        
        else:
            return ListView.get(self, request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AddClass, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

#################################################################
# The following will support the self-directed learning management functionalities

# SDLManagement View
# manage all the self directed learning materials
# able to view all posts, edit and create new posts
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class SDLManagement(FilterView, ListView):
    # use template teachers/SDLmanagement.html
    template_name='teachers/SDLmanagement.html'
    # set the contextobjectname as posts
    context_object_name = 'posts'
    # paginate by 10
    paginate_by = 10
    # use the SDLPostFilter
    filterset_class = SDLPostFilter

    def get_queryset(self):
        # get all the posts
        allposts = SDLPost.objects.all().order_by('-lastmodifieddate','-lastmodifiedtime', '-datecreated', '-timecreated', '-postid')
        # return queryset
        return allposts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # set the teachers as context
        context['teachers'] = User.objects.filter(is_staff=1)
        # return context
        return context

# AddPost View
# form to allow teachers to create posts
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class AddPost(FormView):
    # use the template teachers/addSDLpost.html
    template_name = 'teachers/addSDLpost.html'
    # use SDLPost model
    model = SDLPost
    # use SDLAddPostForm
    form_class = SDLAddPostForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return FormView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # save the form
            self.form.save()
            # redirect back to SDL management
            return redirect('/teachers/SDLmanagement')
        else:
            return FormView.get(self, request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(AddPost, self).get_form_kwargs()
        # set the request as a kwarg
        kwargs.update({'request': self.request})
        # return kwargs
        return kwargs

# EditPost View
# allows the teacher to edit existing posts
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class EditPost(UpdateView):
    # use the template teachers/modifypost.html
    template_name = 'teachers/modifypost.html'
    # set the contextobjectname as result
    context_object_name = 'result'
    # use the PostModifyForm class
    form_class = PostModifyForm
    # use the SDLPost model
    model = SDLPost
    # set the success url to sdl management
    success_url = '/teachers/SDLmanagement'

    def get_object(self):
        # get the selected post object
        selectedpost = SDLPost.objects.get(postid = self.kwargs['postid'])
        # return object
        return selectedpost

    def get_form_kwargs(self):
        kwargs = super(EditPost, self).get_form_kwargs()
        # set the request as kwarg
        kwargs.update({'request': self.request})
        # return kwargs
        return kwargs

# PublishPost View
# allow teachers to publish the post so that the users can see
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class PublishPost(View):
    # get the postid
    def get(self, request, postid):
        # get the post object
        selectedpost = SDLPost.objects.get(postid = postid)
        # set the post active flag to True
        selectedpost.postactive = True
        # If a teacher chooses to set a post to active, the date and time posted will be updated.
        selectedpost.dateposted = datetime.date.today()
        selectedpost.timeposted = datetime.datetime.now().time()
        # save the object
        selectedpost.save()
        # redirect to SDL management
        return redirect('/teachers/SDLmanagement')

# WithdrawPost View
# allow teachers to withdraw post to hide from users
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class WithdrawPost(View):
    # get the postid
    def get(self, request, postid):
        # get the sdlpost object
        selectedpost = SDLPost.objects.get(postid = postid)
        # set the postactive flag to False
        selectedpost.postactive = False
        # save the object
        selectedpost.save()
        # redirect to SDL management
        return redirect('/teachers/SDLmanagement')

# DeletePost View
# allow teachers to delete a post
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DeletePost(View):
    # get the postid
    def get(self, request, postid):
        # get the sdlpost object
        selectedpost = SDLPost.objects.get(postid = postid)
        # delete the object
        selectedpost.delete()
        # redirect to SDL management
        return redirect('/teachers/SDLmanagement')

# ViewPost View
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class ViewPost(ListView, ModelFormMixin):
    # use the template teachers/viewpost.html
    template_name='teachers/viewpost.html'
    # set the contextobjectname as post
    context_object_name = 'post'
    # use the SDLPost model
    model = SDLPost
    # use the SDLPostComment formclass
    form_class = SDLPostComment

    def get_queryset(self):
        # get the postid
        postid = self.kwargs['postid']
        # get the object
        post = SDLPost.objects.filter(postid=postid)
        # return the post object
        return post

    def get_form_kwargs(self):
        kwargs = super(ViewPost, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            # get the postinstance
            postid = self.kwargs['postid']
            postinstance = SDLPost.objects.get(postid=postid)
            # get the currenctuser
            user = self.request.user
            # save the form
            self.form.save(postinstance, user)
            # set the url redirect to
            url = '/teachers/SDLmanagement/view/' + postid
            # return to the post 
            return redirect(url)
        else:
            return ListView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the postid
        postid = self.kwargs['postid']
        # get the comments queryset
        comments = SDLComment.objects.filter(postid=postid)
        # set the comments as context
        context['comments'] = comments
        # return context
        return context

# DeleteComment View
# allows teachers to delete the comment
@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_staff, name='dispatch')
class DeleteComment(View):
    def get(self, request, postid, commentid):
        # get the sdlcomment object
        comment = SDLComment.objects.get(commentid=commentid)
        # delete the comment object
        comment.delete()
        # get the url to redirect to
        url = '/teachers/SDLmanagement/view/' + postid
        # redirect back to the post
        return redirect(url)

