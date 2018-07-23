from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, ModelFormMixin, UpdateView, DeleteView, CreateView
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


# Create your views here.
@method_decorator(user_is_staff, name='dispatch')
class CreateImage(View):
    def get(self, request, rangeurl, questionid, imageid):
        #PULL FROM REGSITRY FROM IP ADDRESS 192.168.40.134:5000
        data = {}
        serverip = ['192.168.100.42:8051', '192.168.100.43:8051']
        imageid = imageid.lower()
        
        for ip in serverip:
            endpoint1 = 'http://' + ip + '/images/create?fromImage=dmit2.bulletplus.com:9100/{conid}'
            header1 = {"X-Registry-Auth": "eyAidXNlcm5hbWUiOiAiYWRtaW4iLCAicGFzc3dvcmQiOiAicGFzc3dvcmQiLCAic2VydmVyYWRkcmVzcyI6ICJkbWl0Mi5idWxsZXRwbHVzLmNvbTo5MTAwIiB9Cg=="}
            url1 = endpoint1.format(conid=imageid)
            response = requests.post(url1, headers=header1)
            if response.status_code == 200:
                pass
                # data['Id'] = id
                # data['message'] = 'success'
            elif response.status_code == 404:
                return -1 # no container
                # data['message'] = 'no such container'
            elif response.status_code == 500:
                return -2 # server error
            else:
                return response.status_code


            #RENAME THE IMAGE NAME
            #IMAGE NAME CANNOT HAVE CAPITAL LETTERS!!!!!!!!!!!!!!!!!!!!!!!!!
            reference = {}
            imagename = str(rangeurl) + '.' + str(questionid)
            endpoint2 = 'http://' + ip + '/images/dmit2.bulletplus.com:9100/' + imageid + '/tag?repo=' + imagename
            response = requests.post(endpoint2)
            
            if response.status_code == 201:
                # reference['Id'] = range
                # reference['message'] = 'success'
                pass
            elif response.status_code == 400:
                return -3
                # reference['message'] = 'Bad Parameter'
            elif response.status_code == 404:
                return -4
                # reference['message'] = 'no such image'
            elif response.status_code == 409:
                return -5 # conflict
                # reference['message'] = 'conflict'
            elif response.status_code == 500:
                return -2 # server error
                # reference['message'] = 'server error'
            else:
                return response.status_code

        return 0

@method_decorator(user_is_staff, name='dispatch')
class TeacherDashboard(ListView, PermissionRequiredMixin):
    template_name = 'teachers/teacherdashboard.html'
    context_object_name = 'usersobject'
    paginate_by = 10
    filterset_class = StudentFilter

    def get_queryset(self):
        unacceptedstudents = User.objects.filter(is_superuser = False, is_staff = False, isdisabled=True, isaccepted=False).order_by('-lastmodifieddate', '-lastmodifiedtime')
        print(unacceptedstudents)
        return unacceptedstudents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classesobject'] = UserClass.objects.values_list('userclass')
        return context

@method_decorator(user_is_staff, name='dispatch')
class UserManagement(FilterView, ListView):
    template_name = 'teachers/usermanagement.html'
    context_object_name = 'usersobject'
    paginate_by = 10
    filterset_class = StudentFilter

    def get_queryset(self):
        allstudents = User.objects.filter(is_superuser = False, is_staff = False, isdisabled=False, isaccepted=True).order_by('-lastmodifieddate', '-lastmodifiedtime')
        return allstudents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classesobject'] = UserClass.objects.values_list('userclass')
        return context

@method_decorator(user_is_staff, name='dispatch')
class DisabledUserManagement(FilterView, ListView):
    template_name = 'teachers/disabledusermanagement.html'
    context_object_name = 'usersobject'
    paginate_by = 10
    filterset_class = StudentFilter

    def get_queryset(self):
        allstudents = User.objects.filter(is_superuser = False, is_staff = False, isdisabled=True, isaccepted=True).order_by('-lastmodifieddate')
        print(allstudents)
        return allstudents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classesobject'] = UserClass.objects.values_list('userclass')
        return context

@method_decorator(user_is_staff, name='dispatch')
class AddUser(ListView, ModelFormMixin):
    template_name = 'teachers/adduserform.html'
    context_object_name = 'classesobject'
    model = User
    form_class = AdminRegisterForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.form.save()
            return redirect('addusersuccess')
        else:
            print("BYE")
            return ListView.get(self, request, *args, **kwargs)
    
    def get_queryset(self):
        classes =  UserClass.objects.values_list('userclass')
        return classes

    def get_form_kwargs(self):
        kwargs = super(AddUser, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

@method_decorator(user_is_staff, name='dispatch')
class AddUserSuccess(generic.TemplateView):
    template_name = 'teachers/addusersuccess.html'

@method_decorator(user_is_staff, name='dispatch')
class ModifyUser(UpdateView):
    form_class = AdminModifyForm
    model = User
    template_name = 'teachers/modifyuserform.html'
    success_url = '/teachers/usermanagement'

    def get_object(self, queryset = None):
        selecteduser = User.objects.get(username = self.kwargs['username'])
        return selecteduser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classesobject'] = UserClass.objects.values_list('userclass')
        return context

    def get_form_kwargs(self):
        kwargs = super(ModifyUser, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

@method_decorator(user_is_staff, name='dispatch')
class ResetPasswordView(UpdateView):
    form_class = AdminResetCommit
    model = User
    template_name = 'teachers/resetpassword.html'
    success_url = '/teachers/usermanagement'

    def get_object(self, queryset = None):
        selecteduser = User.objects.get(username = self.kwargs['username'])
        return selecteduser

    def get_form_kwargs(self):
        kwargs = super(ResetPasswordView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

@method_decorator(user_is_staff, name='dispatch')
class DisableUser(View):
    def get(self, request, username):
        selecteduser = User.objects.get(username = username)
        selecteduser.isdisabled = True
        selecteduser.save()

        return redirect('/teachers/')

@method_decorator(user_is_staff, name='dispatch')
class AcceptUser(View):
    def get(self, request, username):
        selecteduser = User.objects.get(username = username)
        selecteduser.isaccepted = True
        selecteduser.lastmodifieddate = datetime.date.today()
        selecteduser.lastmodifiedtime = datetime.datetime.now().time()
        admin = self.request.user
        selecteduser.lastmodifiedby = User.objects.get(username = admin)
        selecteduser.acceptedby = User.objects.get(username = admin)
        selecteduser.save()

        return redirect('/teachers/usermanagement/')

@method_decorator(user_is_staff, name='dispatch')
class RejectUser(View):
    def get(self, request, username):
        selecteduser = User.objects.get(username = username)
        selecteduser.delete()
        return redirect('/teachers/usermanagement/')

@method_decorator(user_is_staff, name='dispatch')
class EnableUser(View):
    def get(self, request, username):
        selecteduser = User.objects.get(username = username)
        selecteduser.isdisabled = False
        selecteduser.save()

        return redirect('/teachers/usermanagement/disabled')

@method_decorator(user_is_staff, name='dispatch')
class DeleteUser(DeleteView):
    template_name = 'teachers/confirmdelete.html'
    success_url = '/teachers/usermanagement'
    def get_object(self, queryset = None):
        selecteduser = User.objects.get(username = self.kwargs['username'])
        return selecteduser

@method_decorator(user_is_staff, name='dispatch')
class GroupManagement(FilterView, ListView):
    template_name = 'teachers/groupmanagement.html'
    context_object_name = 'groupobjects'
    filterset_class = GroupFilter

    def get_queryset(self):
        allgroups = Group.objects.all().order_by('-lastmodifieddate')
        return allgroups

@method_decorator(user_is_staff, name='dispatch')
class AddGroup(ListView, ModelFormMixin):
    template_name = 'teachers/addgroupform.html'
    model = Group
    form_class = AddGroupCommit

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.form.save()
            return redirect('addgroupsuccess')
        else:
            return ListView.get(self, request, *args, **kwargs)
    
    def get_queryset(self):
        classes =  UserClass.objects.values_list('userclass')
        return classes

    def get_form_kwargs(self):
        kwargs = super(AddGroup, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

@method_decorator(user_is_staff, name='dispatch')
class AddGroupSuccess(generic.TemplateView):
    template_name = 'teachers/addgroupsuccess.html'

@method_decorator(user_is_staff, name='dispatch')
class GroupView(ListView):
    template_name = 'teachers/groupview.html'
    context_object_name = 'usersobject'

    def get_queryset(self):
        groupid = Group.objects.filter(groupname = self.kwargs['groupname']).values_list('groupid')[0][0]
        studentsingroup = StudentGroup.objects.filter(groupid = groupid).values_list('studentid')
        print(studentsingroup)

        if len(studentsingroup) != 0:
            students = User.objects.filter(email = studentsingroup[0][0])
            for x in range(1, len(studentsingroup)):
                result = User.objects.filter(email = studentsingroup[x][0])
                students = students | result
        else:
            students = None

        return students

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groupname'] = self.kwargs['groupname']
        context['groupobjects'] = Group.objects.filter(groupname = self.kwargs['groupname']).order_by('-lastmodifieddate')
        return context

@method_decorator(user_is_staff, name='dispatch')
class AddUserInGroup(FilterView, ListView):
    template_name = 'teachers/adduseringroup.html'
    context_object_name = 'usersobject'
    paginate_by = 10
    filterset_class = StudentFilter

    def get_queryset(self):
        groupid = Group.objects.filter(groupname = self.kwargs['groupname']).values_list('groupid')[0][0]
        studentsingroup = StudentGroup.objects.filter(groupid = groupid).values_list('studentid')
        allstudents = User.objects.filter(is_superuser = False, is_staff = False).exclude(email__in=studentsingroup).order_by('-lastmodifieddate')
        return allstudents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classesobject'] = UserClass.objects.values_list('userclass')
        context['groupname'] = self.kwargs['groupname']

        if "usercart" in self.request.session:
            cart = self.request.session.get('usercart', {})
            print("HI")
            print(cart)
            context['cart'] = cart

        return context

@method_decorator(user_is_staff, name='dispatch')
class AddUserToCart(View):
    def get(self, request, groupname, username):
        get_object_or_404(User, username = username)
        useremail = User.objects.filter(username = username).values_list('email')[0][0]
        userslist = []
        if 'usercart' in request.session:
            userslist = request.session['usercart']
        print(userslist)
        if username not in userslist:
            userslist.append(useremail)
        request.session['usercart'] = userslist

        url = "/teachers/groupmanagement/" + groupname + "/addusers"
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class RemoveUserFromCart(View):
    def get(self, request, groupname, username):
        get_object_or_404(User, username = username)
        useremail = User.objects.filter(username = username).values_list('email')[0][0]
        userslist = []
        if 'usercart' in request.session:
            userslist = request.session['usercart']
        print(userslist)
        if username not in userslist:
            userslist.remove(useremail)
        request.session['usercart'] = userslist

        url = "/teachers/groupmanagement/" + groupname + "/addusers"
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class UserGroupCommit(View):
    def get(self, request, groupname):
        if 'usercart' in request.session:
            userslist = request.session['usercart']

        for student in userslist:
            #print(student)
            studentid = User.objects.get(email = student)
            print(studentid)
            groupid = Group.objects.get(groupname = groupname)
            # print(groupid)
            obj = StudentGroup(studentid = studentid, groupid = groupid)
            obj.save()

        url = "/teachers/groupmanagement/" + groupname
        del request.session['usercart']
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class RemoveStudentFromRange(View):
    def get(self, request, rangeurl, username):
        studentid = User.objects.get(username = username)
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        selecteduser = RangeStudents.objects.get(rangeID = rangeinstance, studentID = studentid)
        selecteduser.delete()
        url = '/teachers/rangemanagement/view/' + rangeurl
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class RemoveGroupFromRange(View):
    def get(self, request, rangeurl, groupname):
        group = Group.objects.get(groupname = groupname)
        selectedgroupmembers = StudentGroup.objects.filter(groupid = group).values_list('studentid')
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        rangestudents = RangeStudents.objects.filter(rangeID = rangeinstance, groupid = group).values_list('studentID')
        studentlist = []
        for student in rangestudents:
            student = student[0]
            studentlist.append(student)

        for student in selectedgroupmembers:
            student = student[0]
            if student in studentlist:
                selecteduser = RangeStudents.objects.get(rangeID = rangeinstance, studentID = student, groupid = group)
                selecteduser.delete()
        url = '/teachers/rangemanagement/view/' + rangeurl
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class RemoveStudentFromGroup(DeleteView):
    template_name = 'teachers/confirmdeletestudentfromgroup.html'
    success_url = '../'
    def get_object(self, queryset = None):
        studentid = User.objects.get(username = self.kwargs['username'])
        groupname = self.kwargs['groupname']
        groupid = Group.objects.get(groupname = groupname)
        selecteduser = StudentGroup.objects.get(studentid = studentid, groupid = groupid)
        return selecteduser

@method_decorator(user_is_staff, name='dispatch')
class DeleteGroup(View):
    template_name = 'teachers/confirmdeletegroup.html'
    #success_url = '/teachers/groupmanagement/'

    def get(self, request, groupname):
        print(groupname)
        groupobj = Group.objects.get(groupname = groupname)
        groupid = Group.objects.filter(groupname = groupname).values_list('groupid')[0][0]
        fakegroupobj = FakeStudentGroup.objects.filter(groupid = groupid)
        fakegroupobj.delete()
        groupobj.delete()
        return redirect('/teachers/groupmanagement')

@method_decorator(user_is_staff, name='dispatch')
class MakeLeader(View):
    def get(self, request, groupname, username):
        studentid = User.objects.get(username = self.kwargs['username'])
        groupname = self.kwargs['groupname']
        group = Group.objects.get(groupname = groupname)
        group.groupleader = studentid
        group.save()

        url = "/teachers/groupmanagement/" + groupname
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class RangeManagement(FilterView, ListView):
    template_name = 'teachers/rangemanagement.html'
    context_object_name = 'ranges'
    paginate_by = 10
    filterset_class = RangeFilter

    def get_queryset(self):
        user = self.request.user
        print(user)
        ranges = Range.objects.all().filter(isdisabled = False, createdbyusername=user)
        return ranges

@method_decorator(user_is_staff, name='dispatch')
class ArchivedRangeManagement(FilterView, ListView):
    template_name = 'teachers/archivedrangemanagement.html'
    context_object_name = 'ranges'
    paginate_by = 10
    filterset_class = RangeFilter

    def get_queryset(self):
        ranges = Range.objects.all().filter(isdisabled = True)
        return ranges

@method_decorator(user_is_staff, name='dispatch')
class CreateRange(CreateView, RedirectView):
    template_name = 'teachers/addrange.html'
    model = Range
    form_class = RangeForm

    def get_form_kwargs(self):
        kwargs = super(CreateRange, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return CreateView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.form.save()
            rangeurl = self.form.cleaned_data['rangeurl']
            print(rangeurl)
            url = '/teachers/rangemanagement/view/' + rangeurl
            messages.success(request, 'Range Created.')
            return redirect(url)
        else:
            return CreateView.get(self, request, *args, **kwargs)

@method_decorator(user_is_staff, name='dispatch')
class RangeView(ListView, FilterView):
    template_name = 'teachers/rangeview.html'
    context_object_name = 'result'
    filterset_class = QuestionFilter

    def get_queryset(self):
        selectedrange = Range.objects.get(rangeurl= self.kwargs['rangeurl'])
        selectedrangeid = selectedrange.rangeid
        #print(selectedrangeid)
        result = Questions.objects.filter(rangeid = selectedrangeid, isarchived = False)
        if len(result) == 0:
            return None
        return result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selectedrange = Range.objects.get(rangeurl= self.kwargs['rangeurl'])
        selectedrangeid = selectedrange.rangeid

        context['isopen'] = selectedrange.isopen
        context['rangename'] = Range.objects.filter(rangeurl= self.kwargs['rangeurl']).values_list('rangename')[0][0]
        context['range'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl'])
        context['rangeurl'] = self.kwargs['rangeurl']
        context['topics'] = QuestionTopic.objects.all()
        context['activated'] = Range.objects.filter(rangeurl= self.kwargs['rangeurl']).values_list('rangeactive')[0][0]
        rangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        studentsinrange = RangeStudents.objects.filter(rangeID = rangeid).values_list('studentID')
        if len(studentsinrange) != 0:
            result = User.objects.filter(email = (studentsinrange[0][0]))
            for x in range(1, len(studentsinrange)):
                currentuser = User.objects.filter(email = studentsinrange[x][0])
                result = result | currentuser # if i didn't get the first object just now python will scold me
        else:
            result = None

        groupstudent = RangeStudents.objects.filter(rangeID = rangeid, groupid__isnull = False)
        context['groupstudent'] = groupstudent

        context['students'] = result

        groupsinrange = RangeStudents.objects.filter(rangeID = rangeid).exclude(groupid__isnull=True).values_list('groupid').distinct()
        if len(groupsinrange) != 0:
            groups = Group.objects.filter(groupid = groupsinrange[0][0])
            for x in range(1, len(groupsinrange)):
                currentgroup = Group.objects.filter(groupid = groupsinrange[x][0])
                groups = groups | currentgroup
        else:
            groups = None
        context['groups'] = groups
        return context

@method_decorator(user_is_staff, name='dispatch')
class ArchivedRangeQuestions(ListView, FilterView):
    template_name = 'teachers/archivedrangequestions.html'
    context_object_name = 'result'
    filterset_class = QuestionFilter

    def get_queryset(self):
        selectedrange = Range.objects.get(rangeurl= self.kwargs['rangeurl'])
        selectedrangeid = selectedrange.rangeid
        #print(selectedrangeid)
        result = Questions.objects.filter(rangeid = selectedrangeid, isarchived = True)
        # print(len(questions))
        # if len(questions) != 0:
        #     result = Questions.objects.filter(questionid=(questions[0][0]))
        #     for x in range(1, len(questions)):
        #         currentquestion= Questions.objects.filter(questionid=(questions[x][0]))
                
        #         result = result | currentquestion # if i didn't get the first object just now python will scold me
        # else:
        #     result = None
        # print(result)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        selectedrange = Range.objects.get(rangeurl= self.kwargs['rangeurl'])
        selectedrangeid = selectedrange.rangeid
        # questions = RangeQuestions.objects.filter(rangeid = selectedrangeid, isdisabled = True).values_list('questionid')
        # if len(questions) != 0:
        #     result = RangeQuestions.objects.filter(questionid=(questions[0][0]))
        #     for x in range(1, len(questions)):
        #         currentquestion= RangeQuestions.objects.filter(questionid=(questions[x][0]))
        #         result = result | currentquestion # if i didn't get the first object just now python will scold me
        # else:
        #     result = None
        
        # context['answer'] = result
        context['rangename'] = Range.objects.filter(rangeurl= self.kwargs['rangeurl']).values_list('rangename')[0][0]
        context['range'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl'])
        context['rangeurl'] = self.kwargs['rangeurl']
        context['topics'] = QuestionTopic.objects.all()
        # context['marks'] = RangeQuestions.objects.filter(rangeid = selectedrangeid)
        return context

@method_decorator(user_is_staff, name='dispatch')
class AddQuestioninRange(FilterView, ListView):
    template_name = 'teachers/addquestionsinrange.html'
    context_object_name = 'questions'
    filterset_class = QuestionFilter

    def get_queryset(self):
        # first i have to get all the questions in the current range
        # then i filter that our from the final queryset
        
        # get current range id
        currentrangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]

        questionsinrange = Questions.objects.filter(rangeid = currentrangeid).values_list('questionid')

        unimportedquestions = Questions.objects.exclude(questionid__in=questionsinrange)
        print(unimportedquestions)
        if len(unimportedquestions) == 0:
            return None
        return unimportedquestions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rangename'] = Range.objects.filter(rangeurl= self.kwargs['rangeurl']).values_list('rangename')[0][0]
        context['topics'] = QuestionTopic.objects.all()

        questionslist = []
        if 'questionscart' in self.request.session:
            cart = self.request.session.get('questionscart', {})
            print(cart)
            context['cart'] = cart

        return context

@method_decorator(user_is_staff, name='dispatch')
class AddQuestionToCart(View):
    def get(self, request, questionid, rangeurl):
        get_object_or_404(Questions, questionid = questionid)
        get_object_or_404(Range, rangeurl = rangeurl)
        #questiontitle = Questions.objects.filter(questionid=questionid).values_list('title')[0][0]
        questionslist = []
        if 'questionscart' in request.session:
            questionslist = request.session['questionscart']
        if questionid not in questionslist:
            questionslist.append(questionid)
        request.session['questionscart'] = questionslist

        url = '/teachers/rangemanagement/view/' + rangeurl + '/import/'
        return redirect(url)


@method_decorator(user_is_staff, name='dispatch')
class RemoveQuestionFromCart(View):
    def get(self, request, questionid, rangeurl):
        get_object_or_404(Questions, questionid = questionid)
        get_object_or_404(Range, rangeurl = rangeurl)
        #questiontitle = Questions.objects.filter(questionid=questionid).values_list('title')[0][0]
        questionslist = []
        if 'questionscart' in request.session:
            questionslist = request.session['questionscart']
        if questionid in questionslist:
            questionslist.remove(questionid)
        request.session['questionscart'] = questionslist

        url = '/teachers/rangemanagement/view/' + rangeurl + '/import/'
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class AddQuestioninRangeCommit(View):
    def get(self, request, rangeurl):
        rangeobj = Range.objects.get(rangeurl=rangeurl)

        if 'questionscart' in request.session:
            questionslist = request.session['questionscart']

        for questionid in questionslist:
            questionobj = Questions.objects.get(questionid = questionid)
            questionobj.pk = None
            questionobj.rangeid = rangeobj
            questionobj.save()
        
        url = '/teachers/rangemanagement/view/' + rangeurl
        del request.session['questionscart']
        return redirect(url)

# class AddQuestionAnswer(View):
#     def get(self, request, rangeurl, questionid):
#         return render(request, template_name = 'teachers/addquestionanswer.html')

#     def post(self, request, rangeurl, questionid):
#         rqobject = RangeQuestions()
#         currentrangeid = Range.objects.filter(rangeurl = rangeurl).values_list('rangeid')[0][0]
#         rangeinstance = Range.objects.get(rangeid = currentrangeid)
#         rqobject.rangeid = rangeinstance
#         questioninstance = Questions.objects.get(questionid = questionid)
#         rqobject.questionid = questioninstance
#         rqobject.answer = request.POST.get('answer')
#         print(request.POST.get('answer'))
#         rqobject.isdisabled = False
#         rqobject.save()

#         return redirect('../../')

@method_decorator(user_is_staff, name='dispatch')
class EditQuestion (UpdateView):
    form_class = ModifyQuestionForm
    model = Questions
    template_name = 'teachers/editquestion.html'
    success_url = '../../'
    context_object_name = 'result'

    def get_form_kwargs(self):
        kwargs = super(EditQuestion, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        kwargs.update({'rangeurl': self.kwargs['rangeurl']})
        kwargs.update({'questionid': self.kwargs['questionid']})
        return kwargs

    def get_object(self):
        selectedquestion = Questions.objects.get(questionid = self.kwargs['questionid'])
        selectedquestionid = selectedquestion.questionid
        return selectedquestion
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selectedquestion = Questions.objects.get(questionid = self.kwargs['questionid'])
        selectedrangequestion = Questions.objects.get(questionid = self.kwargs['questionid'])
        context['rangequestions'] = selectedrangequestion
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        context['questiontopic'] = questiontopic

        getthistopicid = (selectedquestion.topicid.topicid)
        currentquestiontopicname = QuestionTopic.objects.get(topicid=getthistopicid)
        context['currentquestiontopicname'] = currentquestiontopicname.topicname

        context['questiontypechoices'] = QUESTION_TYPE_CHOICES

        if selectedquestion.questiontype == 'MCQ':
            mcqoptions_obj = MCQOptions.objects.get(questionid = selectedquestion)
            context['optionone'] = mcqoptions_obj.optionone
            context['optiontwo'] = mcqoptions_obj.optiontwo
            context['optionthree'] = mcqoptions_obj.optionthree
            context['optionfour'] = mcqoptions_obj.optionfour

        return context

@method_decorator(user_is_staff, name='dispatch')
class ModifyRange(UpdateView):
    form_class = ModifyRangeForm
    model = Range
    template_name = 'teachers/editrange.html'
    success_url = '../'

    def get_object(self, queryset = None):
        selectedrange = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
        return selectedrange

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rangeobject = Range.objects.filter(rangeurl = self.kwargs['rangeurl'])
        context['range'] = rangeobject
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        context['questiontopic'] = questiontopic
        context['rangeurl'] = self.kwargs['rangeurl']

        startdate = rangeobject.values_list('datestart')[0][0]  
        startdate = startdate.strftime('%Y-%m-%d')
        context['startdate'] = startdate
        enddate = rangeobject.values_list('dateend')[0][0]
        enddate = enddate.strftime('%Y-%m-%d')
        context['enddate'] = enddate

        starttime = rangeobject.values_list('timestart')[0][0]
        if starttime is not None:
            amorpm = starttime.strftime('%p')
            minutes = starttime.strftime('%M')
            hours = starttime.strftime('%H')
            context['starttime'] = str(hours) + ':' + str(minutes)

        endtime = rangeobject.values_list('timeend')[0][0]
        if endtime is not None:
            amorpm = endtime.strftime('%p')
            minutes = endtime.strftime('%M')
            print(minutes)
            hours = endtime.strftime('%H')
            context['endtime'] = str(hours) + ':' + str(minutes)
        return context

    def get_form_kwargs(self):
        kwargs = super(ModifyRange, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

@method_decorator(user_is_staff, name='dispatch')
class ArchiveRange(View):
    def get(self, request, rangeurl):
        previousurl = request.META.get('HTTP_REFERER')
        selectedrange = Range.objects.get(rangeurl=self.kwargs['rangeurl'])
        selectedrange.isdisabled = 1
        updatedrange = selectedrange
        updatedrange.save()

        return redirect(previousurl)

@method_decorator(user_is_staff, name='dispatch')
class DeleteRange(View):
    def get(self, request, rangeurl):
        rangeobj = Range.objects.get(rangeurl = rangeurl)
        rangeid = Range.objects.filter(rangeurl = rangeurl).values_list('rangeid')[0][0]
        rangestudentsobj = RangeStudents.objects.filter(rangeID = rangeid)
        rangequestionsobj = Questions.objects.filter(rangeid = rangeid)
        fakerangeobj = FakeRange.objects.filter(rangeid = rangeid)
        rangequestionsobj.delete()
        rangestudentsobj.delete()
        fakerangeobj.delete()
        rangeobj.delete()
        return redirect('../../')

@method_decorator(user_is_staff, name='dispatch')
class UnarchiveRange(View):
    def get(self, request, rangeurl):
        previousurl = request.META.get('HTTP_REFERER')
        selectedrange = Range.objects.get(rangeurl=self.kwargs['rangeurl'])
        selectedrange.isdisabled = 0
        updatedrange = selectedrange
        updatedrange.save()

        return redirect(previousurl)

@method_decorator(user_is_staff, name='dispatch')
class ArchiveQuestion(View):
    def get(self, request, rangeurl, questionid):
        previousurl = request.META.get('HTTP_REFERER')
        rangeurl = self.kwargs['rangeurl']
        questionid = self.kwargs['questionid']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        selectedquestioninstance = Questions.objects.get(questionid = questionid)
        selectedrangequestion = Questions.objects.get(rangeid=rangeinstance, questionid=questionid)
        selectedrangequestion.isarchived = 1
        selectedrangequestion.save()

        # questionmarks = RangeQuestions.objects.filter(rangeid=rangeinstance, questionid = selectedquestioninstance).values_list('points')[0][0]
        updatedscore = rangeinstance.maxscore - selectedrangequestion.points
        rangeinstance.maxscore = updatedscore
        rangeinstance.save()
        return redirect(previousurl)

@method_decorator(user_is_staff, name='dispatch')
class UnarchiveQuestion(View):
    def get(self, request, rangeurl, questionid):
        previousurl = request.META.get('HTTP_REFERER')
        rangeurl = self.kwargs['rangeurl']
        questionid = self.kwargs['questionid']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        selectedquestioninstance = Questions.objects.get(questionid = questionid)
        selectedrangequestion = Questions.objects.get(rangeid=rangeinstance, questionid=selectedquestioninstance)
        selectedrangequestion.isarchived = 0
        selectedrangequestion.save()

        # questionmarks = RangeQuestions.objects.filter(rangeid=rangeinstance, questionid = selectedquestioninstance).values_list('points')[0][0]
        updatedscore = rangeinstance.maxscore + selectedrangequestion.marks
        rangeinstance.maxscore = updatedscore
        rangeinstance.save()
        return redirect(previousurl)

@method_decorator(user_is_staff, name='dispatch')
class DeleteQuestionFromRange(View):
    def get(self, request, rangeurl, questionid):
        previousurl = request.META.get('HTTP_REFERER')
        rangeurl = self.kwargs['rangeurl']
        questionid = self.kwargs['questionid']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        selectedquestioninstance = Questions.objects.get(questionid = questionid)
        selectedquestioninstance.delete()
        return redirect(previousurl)

@method_decorator(user_is_staff, name='dispatch')
class AssignUser(ListView, FilterView):
    template_name = 'teachers/assignuserrange.html'
    context_object_name = 'usersobject'
    paginate_by = 10
    filterset_class = StudentFilter

    def get_queryset(self):
        rangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        studentsinrange = RangeStudents.objects.filter(rangeID = rangeid).values_list('studentID')
        allstudents = User.objects.filter(is_superuser = False, is_staff = False, isdisabled = False).exclude(email__in=studentsinrange).order_by('-lastmodifieddate')
        print(allstudents)
        return allstudents

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classesobject'] = UserClass.objects.values_list('userclass')

        if "userrangecart" in self.request.session:
            cart = self.request.session.get('userrangecart', {})
            context['cart'] = cart

        return context

@method_decorator(user_is_staff, name='dispatch')
class AddUserRangeCart(View):
    def get(self, request, rangeurl, username):
        get_object_or_404(User, username = username)
        useremail = User.objects.filter(username = username).values_list('email')[0][0]
        userslist = []
        if 'userrangecart' in request.session:
            userslist = request.session['userrangecart']
        print(userslist)
        if username not in userslist:
            userslist.append(useremail)
        request.session['userrangecart'] = userslist
        url = "/teachers/rangemanagement/view/" + rangeurl + "/assignusers"
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class RemoveUserRangeCart(View):
    def get(self, request, rangeurl, username):
        get_object_or_404(User, username = username)
        useremail = User.objects.filter(username = username).values_list('email')[0][0]
        userslist = []
        if 'userrangecart' in request.session:
            userslist = request.session['userrangecart']
        print(userslist)
        if username not in userslist:
            userslist.remove(useremail)
        request.session['userrangecart'] = userslist
        url = "/teachers/rangemanagement/view/" + rangeurl + "/assignusers"
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class UserRangeCommit(View):
    def get(self, request, rangeurl):
        if 'userrangecart' in request.session:
            userslist = request.session['userrangecart']

        for student in userslist:
            #print(student)
            studentid = User.objects.get(email = student)
            print(studentid)
            rangeid = Range.objects.get(rangeurl = rangeurl)
            # print(groupid)
            datejoined = datetime.date.today()
            obj = RangeStudents(studentID = studentid, rangeID = rangeid, dateJoined = datejoined)
            obj.save()

        url = "/teachers/rangemanagement/view/" + rangeurl
        del request.session['userrangecart']
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class AssignGroup(ListView, FilterView):
    template_name = 'teachers/assigngrouprange.html'
    context_object_name = 'groupobject'
    paginate_by = 10
    filterset_class = GroupFilter

    def get_queryset(self):
        rangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        groupsinrange = RangeStudents.objects.filter(rangeID = rangeid, studentID = None).values_list('groupid')
        allgroups = Group.objects.exclude(groupid__in = groupsinrange).order_by('-lastmodifieddate')
        print(allgroups)
        return allgroups

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "grouprangecart" in self.request.session:
            cart = self.request.session.get('grouprangecart', {})
            print("HI")
            print(cart)
            context['cart'] = cart

        return context

@method_decorator(user_is_staff, name='dispatch')
class AddGroupRangeCart(View):
    def get(self, request, rangeurl, groupname):
        print(groupname)
        get_object_or_404(Group, groupname = groupname)
        groupslist = []
        if 'grouprangecart' in request.session:
            groupslist = request.session['grouprangecart']
        print(groupslist)
        if groupname not in groupslist:
            groupslist.append(groupname)
        request.session['grouprangecart'] = groupslist
        url = "/teachers/rangemanagement/view/" + rangeurl + "/assigngroups"
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class RemoveGroupRangeCart(View):
    def get(self, request, rangeurl, groupname):
        get_object_or_404(Group, groupname = groupname)
        groupslist = []
        if 'grouprangecart' in request.session:
            groupslist = request.session['grouprangecart']
        print(groupslist)
        if groupname in groupslist:
            groupslist.remove(groupname)
        request.session['grouprangecart'] = groupslist
        url = "/teachers/rangemanagement/view/" + rangeurl + "/assigngroups"
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class GroupRangeCommit(View):
    def get(self, request, rangeurl):
        if 'grouprangecart' in request.session:
            groupslist = request.session['grouprangecart']

        for groupname in groupslist:
            #print(student)
            groupid = Group.objects.filter(groupname = groupname).values_list('groupid')[0][0]
            studentsingroup = StudentGroup.objects.filter(groupid = groupid).values_list('studentid')

            for students in studentsingroup:
                studentobj = User.objects.get(email = students[0])
                rangeid = Range.objects.get(rangeurl = rangeurl)
                datejoined = datetime.date.today()
                groupobj = Group.objects.get(groupname = groupname)
                obj = RangeStudents(studentID = studentobj, rangeID = rangeid, dateJoined = datejoined, groupid = groupobj)
                obj.save()

        url = "/teachers/rangemanagement/view/" + rangeurl 
        del request.session['grouprangecart']
        return redirect(url)

@method_decorator(user_is_staff, name='dispatch')
class CreateQuestion(ListView, ModelFormMixin):
    template_name = 'teachers/addquestion.html'
    context_object_name = 'currentmarks'
    model = Questions
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
            question, topicname = self.form.save()
            optionone = request.POST.get('optionone',' ')
            points = request.POST.get('points',' ')
            answer = request.POST.get('answer',' ')
            registryid = self.request.POST.get('registryid','')
            questionid = question.questionid
            request.session['questionid'] = questionid
            questioninstance = Questions.objects.get(questionid = questionid)

            currentrangescore = rangeinstance.maxscore
            if currentrangescore is None:
                currentrangescore = 0 + int(points)
            else: 
                currentrangescore += int(points)
            
            rangeinstance.maxscore = currentrangescore
            rangeinstance.save()
        
            request.session['TF'] = False

            rangeurl = self.kwargs['rangeurl']
            if (request.POST.get('usedocker') == 'True'):

                print("YAY it works")
                imageid = request.POST.get('registryid')
                error = CreateImage.get(self, request, rangeurl, questionid, imageid)
                if error is not 0:
                   return HttpResponse('ERROR')


            if question.questiontype == 'MCQ' and optionone == ' ':
                rangename = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]
                questionobject = Questions.objects.filter(questionid = question.questionid)
                currentmarks =  Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('maxscore')[0][0]
                args = {
                    'rangename' : rangename,
                    'question' : questionobject,
                    'currentmarks' : currentmarks,
                    'points' : points,
                    'answer' : answer,
                    'topicname' : topicname,
                    }
                return render(request, 'teachers/addmcqquestion.html', args)

            if answer != "True" and answer  != "False" and question.questiontype == 'TF':
                request.session['TF'] = True
                rangename = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]
                questionobject = Questions.objects.filter(questionid = question.questionid)
                currentmarks =  Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('maxscore')[0][0]
                args = {
                    'rangename' : rangename,
                    'question' : questionobject,
                    'currentmarks' : currentmarks,
                    'points' : points,
                    'answer' : answer,
                    'topicname' : topicname,
                    }
                return render(request, 'teachers/addtfquestion.html', args)
                
                    
            return ListView.get(self, request, *args, **kwargs)
        else:
            ## IF THE USER IS DONE W CREATING QUESTION THEN WILL REDIRECT THEM TO VIEW RANGE ##
            if (request.POST.get('done')):
                rangeurl = self.kwargs['rangeurl']
                url = "/teachers/rangemanagement/view/" + rangeurl
                return redirect(url)

            ### IF THE USER WANTS TO SUBMIT NEW TOPIC NAME THEN REFRESHES THE CREATE QNS FOR THEM###
            elif (request.POST.get('newtopicname')):
                form_newtopicname = request.POST.get('newtopicname')
                currenttopicnameavail = QuestionTopic.objects.all().values_list('topicname')
                topiclist = []
                for x in range(0, len(currenttopicnameavail)):
                    topiclist.append(Lower(currenttopicnameavail[x][0]))

                lowercase_form_newtopicname = Lower(form_newtopicname)

                ### CHECKS IF TOPICNAME IS ALREADY IN DATABASE ###
                if lowercase_form_newtopicname not in topiclist:
                    QuestionTopic_obj = QuestionTopic(topicname = form_newtopicname)
                    QuestionTopic_obj.save()
                    messages.success(request, 'New Question Topic Created ')

                ### IF TOPICNAME IS ALREADY IN DATABASE, THEN WON'T ADD ###
                else:
                    messages.error(request, 'Topic Name Already Exists in Database ')

                return ListView.get(self, request, *args, **kwargs)

            elif (request.POST.get('optionone',' ') != ' '):
                optionone = request.POST.get('optionone', ' ')
                optiontwo = request.POST.get('optiontwo',' ')
                optionthree = request.POST.get('optionthree',' ')
                optionfour = request.POST.get('optionfour',' ')
                if 'questionid' in request.session:
                    questionid = request.session['questionid']
                questioninstance = Questions.objects.get(questionid = questionid)
                mcqobject = MCQOptions(optionone = optionone, optiontwo = optiontwo, optionthree = optionthree, optionfour = optionfour, questionid = questioninstance)
                mcqobject.save()
                return ListView.get(self, request, *args, **kwargs)

            elif (request.session['TF'] == True):
                answer = self.request.POST.get('answer','')
                if 'questionid' in request.session:
                    questionid = request.session['questionid']
                questioninstance = Questions.objects.get(questionid = questionid)
                questioninstance.answer = answer
                questioninstance.save()
                
                return ListView.get(self, request, *args, **kwargs)
            else:
                print("OMG")
                return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        currentmarks =  Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('maxscore')[0][0]
        return currentmarks

    def get_form_kwargs(self):
        kwargs = super(CreateQuestion, self).get_form_kwargs()
        rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
        kwargs.update({'request': self.request, 'rangeinstance': rangeinstance})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questiontypechoices'] = QUESTION_TYPE_CHOICES
        context['rangename'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        context['questiontopic'] = questiontopic
        return context

@method_decorator(user_is_staff, name='dispatch')
class ActivateRange(View):
    def get(self, request, rangeurl):
        rangeobject = Range.objects.get(rangeurl = rangeurl)
        rangeobject.rangeactive = True
        rangeobject.manualactive = True
        rangeobject.manualdeactive = False
        rangeobject.save()
        return redirect('./')

@method_decorator(user_is_staff, name='dispatch')
class DeactivateRange(View):
    def get(self, request, rangeurl):
        rangeobject = Range.objects.get(rangeurl = rangeurl)
        rangeobject.rangeactive = False
        rangeobject.manualdeactive = True
        rangeobject.manualactive = False
        rangeobject.save()
        return redirect('./')

@method_decorator(user_is_staff, name='dispatch')
class QuestionManagement(FilterView, ListView):
    template_name = 'teachers/questionmanagement.html'
    context_object_name = 'questions'
    paginate_by = 10
    filterset_class = QuestionFilter

    def get_queryset(self):
        questions = Questions.objects.all()
        return questions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = QuestionTopic.objects.all()
        print(context['topics'])
        return context

@method_decorator(user_is_staff, name='dispatch')
class DockerManagement(ListView):
    template_name = 'teachers/dockermanagement.html'
    context_object_name = 'dockerobjects'
    paginate_by = 10

    def get_queryset(self):
        dockers = UnavailablePorts.objects.all()
        return dockers

@method_decorator(user_is_staff, name='dispatch')
class AdminDockerKill(View):
    def get(self, request, containername):
        # i think i need to get the ports to check if it's web server or docker server
        portnumber = UnavailablePorts.objects.filter(containername = containername).values_list('portnumber')[0][0]
        if int(portnumber) > 9051:
            server = '192.168.100.42'
        else:
            server = '192.168.100.43'
        # delete old port if existing
        endpoint = 'http://' + server + ':8051/containers/' + containername + '?force=True'
        response = requests.delete(endpoint)
        # need to delete from containernamed
        deleteportsdb = UnavailablePorts.objects.filter(containername = containername)
        deleteportsdb.delete()

        return redirect('/teachers/dockermanagement/')

@method_decorator(user_is_staff, name='dispatch')
class ImportCSV(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'teachers/importqns.html')

    def post(self, request, *args, **kwargs):
        rangeurl = self.kwargs['rangeurl']
        data = {}
        try:
            csv_file = request.FILES["qnsfile"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request,'File is not CSV type')
                return render(request, 'teachers/importqns.html')
            #if file is too large, return
            if csv_file.multiple_chunks():
                messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return render(request, 'teachers/importqns.html')
            
            file_data = csv_file.read().decode("utf-8")		

            lines = file_data.split("\n")

            #loop over the lines and save them in db. If error , store as string and then display
            x = 0
            for line in lines:
                if line and x > 0:
                    fields = line.split(",")
                    data_dict = {}
                    questiontype = fields[0]
                    topicname = fields[1]
                    title = fields[2]
                    text = fields[3]
                    answer = fields[4]
                    hint = fields[5]
                    marks = fields[6]
                    usedocker = fields[7]

                    docker = False
                    if usedocker == 1:
                        docker = True
                    elif usedocker == 0:
                        docker = False
                        
                    if answer == 'TRUE':
                        answer = 'True'
                    if answer == 'FALSE':
                        answer = 'False'

                    print('questiontype is ' + str(questiontype))
                    print('topicname is ' + str(topicname))
                    print('title is ' + str(title))
                    print('text is ' + str(text))
                    print('answer is ' + str(answer))
                    print('hint is ' + str(hint))
                    print('marks is ' + str(marks))
                    print('--------------------------------------------------------------------------------')

                    datetimenow = datetime.datetime.now()
                    username = self.request.user
                    print(username)
                    userinstance = User.objects.get(username = username)
                    print(userinstance.email)
                    rangeinstance = Range.objects.get(rangeurl = rangeurl)
                    questiontopicinstance = QuestionTopic.objects.get(topicname = topicname)
                    question_obj = Questions(topicid = questiontopicinstance,
                                            questiontype = questiontype,
                                            title = title,
                                            text = text,
                                            hint = hint,
                                            marks = marks,
                                            answer = answer,
                                            usedocker = docker,
                                            datecreated = datetimenow,
                                            createdby = userinstance,
                                            rangeid = rangeinstance)
                    question_obj.save()
                    
                    questioninstance = Questions.objects.all().order_by('-questionid')[0]
                    print('range instance is ' + str(rangeinstance.rangeurl))
                    rangequestion_obj = RangeQuestions(questionid = questioninstance,
                                                        rangeid = rangeinstance,
                                                        isdisabled = False,
                                                        answer = answer,
                                                        registryid = '?')
                    rangequestion_obj.save()
                    print('its all for the range ' + str(rangeinstance.rangeurl))

                    if str(questiontype) == 'MCQ':
                        optionone = fields[8]
                        optiontwo = fields[9]
                        optionthree = fields[10]
                        optionfour = fields[11]
                        print(optionone)
                        print(optiontwo)
                        print(optionthree)
                        print(optionfour)
                        mcqoptions_obj = MCQOptions(optionone = optionone,
                                                    optiontwo = optiontwo,
                                                    optionthree = optionthree,
                                                    optionfour = optionfour,
                                                    questionid = questioninstance)
                        mcqoptions_obj.save()
                x = x + 1

        except Exception as e:
            logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
            messages.error(request,"Unable to upload file. "+repr(e))
            
        return render(request, 'teachers/importqns.html')


@method_decorator(user_is_staff, name='dispatch')
class ExportCSV(View):
    def get(self, request, *args, **kwargs):
        rangeurl = self.kwargs['rangeurl']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        rangeid = rangeinstance.rangeid
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="questions.csv"'

        writer = csv.writer(response)
        writer.writerow(['Question ID', 'QuestionType', 'Topic Name', 'Title', 'Text', 'Answer', 'Hint', 'Marks','Use Docker', 'Option One', 'Option Two', 'Option Three', 'Option Four'])

        questions = Questions.objects.filter(rangeid = rangeinstance).values_list('questionid', 'questiontype', 'topicid', 'title', 'text', 'answer', 'hint', 'marks')
        for qns in questions:

            if qns[1] == 'MCQ':
                print('got mcq')
                questioninstance = Questions.objects.get(questionid = qns[0])
                mcqoptionsinstance = MCQOptions.objects.get(questionid = questioninstance)
                writer.writerow(qns, mcqoptionsinstance.optionone, mcqoptionsinstance.optiontwo, mcqoptionsinstance.optionthree, mcqoptionsinstance.optionfour)

            else:
                print('it tried')
                writer.writerow(qns)
                
        return response

@method_decorator(user_is_staff, name='dispatch')
class ReportView(generic.ListView):
    template_name='teachers/report.html'
    context_object_name = 'questions'
    def get_queryset(self):
        username = self.kwargs['username']
        useremail = User.objects.filter(username=username).values_list('email')[0][0]
        rangeid = Range.objects.filter(rangeurl=self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        questions = Questions.objects.filter(rangeid=rangeid)
        print(questions)

        return questions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rangeurl = self.kwargs['rangeurl']
        username = self.kwargs['username']
        context['username'] = username
        useremail = User.objects.filter(username=username).values_list('email')[0][0]
        rangeid = Range.objects.filter(rangeurl=rangeurl).values_list('rangeid')[0][0]

        context['rangename'] = Range.objects.filter(rangeurl=rangeurl).values_list('rangename')[0][0]
        context['maxscore'] = Range.objects.filter(rangeurl=rangeurl).values_list('maxscore')[0][0]
        context['totalscore'] = RangeStudents.objects.filter(studentID=useremail).values_list('points')[0][0]
        context['useranswer'] = StudentQuestions.objects.filter(rangeid=rangeid, studentid=useremail).values_list('answergiven')[0][0]
        context['usermark'] = StudentQuestions.objects.filter(rangeid=rangeid, studentid=useremail).all()
        context['topic'] = QuestionTopic.objects.all()

        return context




@method_decorator(user_is_staff, name='dispatch')
class TeacherView(FilterView, ListView):
    template_name = 'teachers/teachermanagement.html'
    context_object_name = 'teacherobjects'
    filterset_class = TeacherFilter

    def get_queryset(self):
        allteachers = User.objects.filter(is_staff = 1)
        return allteachers

@method_decorator(user_is_staff, name='dispatch')
class AddTeacher(ListView, ModelFormMixin):
    template_name = 'teachers/addteacher.html'
    context_object_name = 'teachersobject'
    model = User
    form_class = TeacherRegisterForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            print('what')
            self.form.save(request)
            messages.success(request, 'Teacher account successfully created')
            return render(request, 'teachers/addteacher.html/')

        else:
            print(self.form.errors)
            print('not valid')

@method_decorator(user_is_staff, name='dispatch')
class ClassView(ListView):
    template_name = 'teachers/classmanagement.html'
    context_object_name = 'classobjects'

    def get_queryset(self):
        alluserclass = UserClass.objects.all()
        return alluserclass

@method_decorator(user_is_staff, name='dispatch')
class AddClass(ListView, ModelFormMixin):
    template_name = 'teachers/addclass.html'
    context_object_name = 'classobjects'
    model = UserClass
    form_class = ClassForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.form.save()
            messages.success(request, 'New Class Added Successfuly')
            return render(request, 'teachers/addclass.html')
        
        else:
            print(self.form.errors)
            print('not valid')

    def get_form_kwargs(self):
        kwargs = super(AddClass, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

@method_decorator(user_is_staff, name='dispatch')
class IsOpen(View):
    def get(self, request, *args, **kwargs):
        rangeurl = self.kwargs['rangeurl']
        selectedrangeinstance = Range.objects.get(rangeurl = rangeurl)
        selectedrangeinstance.isopen = 1
        selectedrangeinstance.save()

        returnurl = ('/teachers/rangemanagement/view/' + str(rangeurl))
        return HttpResponseRedirect(returnurl)

@method_decorator(user_is_staff, name='dispatch')
class IsClose(View):
    def get(self, request, *args, **kwargs):
        rangeurl = self.kwargs['rangeurl']
        selectedrangeinstance = Range.objects.get(rangeurl = rangeurl)
        selectedrangeinstance.isopen = 0
        selectedrangeinstance.save()

        returnurl = ('/teachers/rangemanagement/view/' + str(rangeurl))
        return HttpResponseRedirect(returnurl)