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

# Create your views here.

class TeacherDashboard(ListView, PermissionRequiredMixin):
    template_name = 'teachers/teacherdashboard.html'
    context_object_name = 'usersobject'
    paginate_by = 10
    filterset_class = StudentFilter

    def get_queryset(self):
        unacceptedstudents = User.objects.filter(is_superuser = False, is_staff = False, isdisabled=False, isaccepted=False).order_by('-lastmodifieddate', '-lastmodifiedtime')
        print(unacceptedstudents)
        return unacceptedstudents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classesobject'] = UserClass.objects.values_list('userclass')
        return context


class UserManagement(FilterView, ListView):
    template_name = 'teachers/usermanagement.html'
    context_object_name = 'usersobject'
    paginate_by = 10
    filterset_class = StudentFilter

    def get_queryset(self):
        allstudents = User.objects.filter(is_superuser = False, is_staff = False, isdisabled=False).order_by('-lastmodifieddate', '-lastmodifiedtime')
        return allstudents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classesobject'] = UserClass.objects.values_list('userclass')
        return context

class DisabledUserManagement(FilterView, ListView):
    template_name = 'teachers/disabledusermanagement.html'
    context_object_name = 'usersobject'
    paginate_by = 10
    filterset_class = StudentFilter

    def get_queryset(self):
        allstudents = User.objects.filter(is_superuser = False, is_staff = False, isdisabled=True).order_by('-lastmodifieddate')
        print(allstudents)
        return allstudents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classesobject'] = UserClass.objects.values_list('userclass')
        return context

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

class AddUserSuccess(generic.TemplateView):
    template_name = 'teachers/addusersuccess.html'

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

class DisableUser(View):
    def get(self, request, username):
        selecteduser = User.objects.get(username = username)
        selecteduser.isdisabled = True
        selecteduser.save()

        return redirect('/teachers/usermanagement')

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

class EnableUser(View):
    def get(self, request, username):
        selecteduser = User.objects.get(username = username)
        selecteduser.isdisabled = False
        selecteduser.save()

        return redirect('/teachers/usermanagement/disabled')

class DeleteUser(DeleteView):
    template_name = 'teachers/confirmdelete.html'
    success_url = '/teachers/usermanagement'
    def get_object(self, queryset = None):
        selecteduser = User.objects.get(username = self.kwargs['username'])
        return selecteduser

class GroupManagement(FilterView, ListView):
    template_name = 'teachers/groupmanagement.html'
    context_object_name = 'groupobjects'
    filterset_class = GroupFilter

    def get_queryset(self):
        allgroups = Group.objects.all().order_by('-lastmodifieddate')
        return allgroups

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

class AddGroupSuccess(generic.TemplateView):
    template_name = 'teachers/addgroupsuccess.html'

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

class RemoveStudentFromGroup(DeleteView):
    template_name = 'teachers/confirmdeletestudentfromgroup.html'
    success_url = '../'
    def get_object(self, queryset = None):
        studentid = User.objects.get(username = self.kwargs['username'])
        groupname = self.kwargs['groupname']
        groupid = Group.objects.get(groupname = groupname)
        selecteduser = StudentGroup.objects.get(studentid = studentid, groupid = groupid)
        return selecteduser

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

class MakeLeader(View):
    def get(self, request, groupname, username):
        studentid = User.objects.get(username = self.kwargs['username'])
        groupname = self.kwargs['groupname']
        group = Group.objects.get(groupname = groupname)
        group.groupleader = studentid
        group.save()

        url = "/teachers/groupmanagement/" + groupname
        return redirect(url)

class RangeManagement(FilterView, ListView):
    template_name = 'teachers/rangemanagement.html'
    context_object_name = 'ranges'
    paginate_by = 10
    filterset_class = RangeFilter

    def get_queryset(self):
        ranges = Range.objects.all().filter(isdisabled = False)
        return ranges

class ArchivedRangeManagement(FilterView, ListView):
    template_name = 'teachers/archivedrangemanagement.html'
    context_object_name = 'ranges'
    paginate_by = 10
    filterset_class = RangeFilter

    def get_queryset(self):
        ranges = Range.objects.all().filter(isdisabled = True)
        return ranges


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

class RangeView(ListView, FilterView):
    template_name = 'teachers/rangeview.html'
    context_object_name = 'result'
    filterset_class = QuestionFilter

    def get_queryset(self):
        selectedrange = Range.objects.get(rangeurl= self.kwargs['rangeurl'])
        selectedrangeid = selectedrange.rangeid
        #print(selectedrangeid)
        questions = RangeQuestions.objects.filter(rangeid = selectedrangeid, isdisabled = False).values_list('questionid')
        if len(questions) != 0:
            result = Questions.objects.filter(questionid=(questions[0][0]))
            for x in range(1, len(questions)):
                currentquestion= Questions.objects.filter(questionid=(questions[x][0]))
                
                result = result | currentquestion # if i didn't get the first object just now python will scold me
        else:
            result = None
        #print("result")
        #print(result)
        return result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selectedrange = Range.objects.get(rangeurl= self.kwargs['rangeurl'])
        selectedrangeid = selectedrange.rangeid
        questions = RangeQuestions.objects.filter(rangeid = selectedrangeid, isdisabled = False).values_list('questionid')
        if len(questions) != 0:
            result = RangeQuestions.objects.filter(questionid=(questions[0][0]))
            for x in range(1, len(questions)):
                currentquestion= RangeQuestions.objects.filter(questionid=(questions[x][0]))
                result = result | currentquestion # if i didn't get the first object just now python will scold me
        else:
            result = None
        
        context['answer'] = result
        context['rangename'] = Range.objects.filter(rangeurl= self.kwargs['rangeurl']).values_list('rangename')[0][0]
        context['range'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl'])
        context['rangeurl'] = self.kwargs['rangeurl']
        context['topics'] = QuestionTopic.objects.all()
        context['marks'] = RangeQuestions.objects.filter(rangeid = selectedrangeid)
        context['activated'] = Range.objects.filter(rangeurl= self.kwargs['rangeurl']).values_list('rangeactive')[0][0]
        rangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        studentsinrange = RangeStudents.objects.filter(rangeID = rangeid).values_list('studentID')
        print(studentsinrange)
        if len(studentsinrange) != 0:
            result = User.objects.filter(email = (studentsinrange[0][0]))
            print(result)
            for x in range(1, len(studentsinrange)):
                currentuser = User.objects.filter(email = studentsinrange[x][0])
                print(currentuser)
                result = result | currentuser # if i didn't get the first object just now python will scold me
                print(result)
        else:
            result = None

        print(result)

        context['students'] = result
        return context

class AddQuestioninRange(ListView, FilterView):
    template_name = 'teachers/addquestionsinrange.html'
    context_object_name = 'questions'
    filterset_class = QuestionFilter

    def get_queryset(self):
        # first i have to get all the questions in the current range
        # then i filter that our from the final queryset
        
        # get current range id
        currentrangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]

        questionsinrange = RangeQuestions.objects.filter(rangeid = currentrangeid).values_list('questionid')

        unimportedquestions = Questions.objects.exclude(questionid__in=questionsinrange)
        print(unimportedquestions)
        if len(unimportedquestions) == 0:
            return None
        return unimportedquestions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rangename'] = Range.objects.filter(rangeurl= self.kwargs['rangeurl']).values_list('rangename')[0][0]
        context['topics'] = QuestionTopic.objects.all()
        return context

class AddQuestionAnswer(View):
    def get(self, request, rangeurl, questionid):
        return render(request, template_name = 'teachers/addquestionanswer.html')

    def post(self, request, rangeurl, questionid):
        rqobject = RangeQuestions()
        currentrangeid = Range.objects.filter(rangeurl = rangeurl).values_list('rangeid')[0][0]
        rangeinstance = Range.objects.get(rangeid = currentrangeid)
        rqobject.rangeid = rangeinstance
        questioninstance = Questions.objects.get(questionid = questionid)
        rqobject.questionid = questioninstance
        rqobject.answer = request.POST.get('answer')
        print(request.POST.get('answer'))
        rqobject.isdisabled = False
        rqobject.save()

        return render(request, template_name = 'teachers/addquestionsuccess.html')

class EditQuestion (UpdateView):
    form_class = QuestionForm
    model = Questions
    template_name = 'teachers/editquestion.html'
    success_url = 'teachers/'
    context_object_name = 'result'

    def get_form_kwargs(self):
        kwargs = super(EditQuestion, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_object(self):
        selectedquestion = Questions.objects.get(questionid = self.kwargs['questionid'])
        selectedquestionid = selectedquestion.questionid
        print(selectedquestionid)
        return selectedquestion
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selectedquestion = Questions.objects.get(questionid = self.kwargs['questionid'])
        selectedrangequestion = RangeQuestions.objects.get(questionid = self.kwargs['questionid'])
        context['rangequestions'] = selectedrangequestion
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        context['questiontopic'] = questiontopic

        getthistopicid = (selectedquestion.topicid.topicid)
        currentquestiontopicname = QuestionTopic.objects.get(topicid=getthistopicid)
        context['currentquestiontopicname'] = currentquestiontopicname.topicname

        FLAG = 'FL'
        MCQ = 'MCQ'
        SHORTANS = 'SA'
        OPENENDED = 'OE'
        TRUEFALSE = 'TF'
        context['questiontypechoices'] = (
            (FLAG, 'Flag'),
            (MCQ, 'Multiple Choice'),
            (SHORTANS, 'Short Answer'),
            (OPENENDED, 'Open Ended'),
            (TRUEFALSE, 'True/False')
        )

        return context

    def post(self, request, *args, **kwargs):
        print('it got into post')
        rangeid = self.kwargs['rangeid']
        selectedquestionid = request.POST.get('questionid')
        form_topicname = request.POST.get('topicname')
        form_title = request.POST.get('title')
        form_text = request.POST.get('text')
        form_hint = request.POST.get('hint')
        form_marks = request.POST.get('marks')
        form_answer = request.POST.get('answer')

        print('topic name is ' + str(form_topicname))
        alltopics = QuestionTopic.objects.all()
        form_topicid = ''
        for x in alltopics:
            if x.topicname == form_topicname:
                form_topicid = x.topicid
        
        topicinstance = QuestionTopic.objects.get(topicname = form_topicname)
        selectedquestioninstance = Questions.objects.get(questionid = selectedquestionid)
        selectedrangequestioninstance = RangeQuestions.objects.get(questionid = selectedquestioninstance)
        affectedrangequestioninstances = RangeQuestions.objects.filter(questionid = selectedquestionid)

        for x in affectedrangequestioninstances:
            affectedrangeinstance = Range.objects.get(rangeid = x.rangeid.rangeid)
            
            currentmaxscore = affectedrangeinstance.maxscore
            minusquestionmarks = currentmaxscore - selectedquestioninstance.marks
            plusbackmarks = minusquestionmarks + int(form_marks)
            affectedrangeinstance.maxscore = plusbackmarks
            affectedrangeinstance.save()

        selectedquestioninstance.title = form_title
        selectedquestioninstance.text = form_text
        selectedquestioninstance.hint = form_hint
        selectedquestioninstance.marks = form_marks
        selectedquestioninstance.topicid = topicinstance
        selectedrangequestioninstance.answer = form_answer

        selectedquestioninstance.save()
        selectedrangequestioninstance.save()

        return redirect('/teachers/rangemanagement')

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


class ArchiveRange(View):
    def get(self, request, rangeurl):
        previousurl = request.META.get('HTTP_REFERER')
        selectedrange = Range.objects.get(rangeurl=self.kwargs['rangeurl'])
        selectedrange.isdisabled = 1
        updatedrange = selectedrange
        updatedrange.save()

        return redirect(previousurl)

class DeleteRange(View):
    def get(self, request, rangeurl):
        rangeobj = Range.objects.get(rangeurl = rangeurl)
        rangeid = Range.objects.filter(rangeurl = rangeurl).values_list('rangeid')[0][0]
        fakerangeobj = FakeRange.objects.filter(rangeid = rangeid)
        fakerangeobj.delete()
        rangeobj.delete()
        return redirect('../../')

class UnarchiveRange(View):
    def get(self, request, rangeurl):
        previousurl = request.META.get('HTTP_REFERER')
        selectedrange = Range.objects.get(rangeurl=self.kwargs['rangeurl'])
        selectedrange.isdisabled = 0
        updatedrange = selectedrange
        updatedrange.save()

        return redirect(previousurl)

class ArchiveQuestion(View):
    def get(self, request, rangeurl, questionid):
        previousurl = request.META.get('HTTP_REFERER')
        rangeurl = self.kwargs['rangeurl']
        questionid = self.kwargs['questionid']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        selectedquestioninstance = Questions.objects.get(questionid = questionid)
        selectedrangequestion = RangeQuestions.objects.get(rangeid=rangeinstance, questionid=selectedquestioninstance)
        selectedrangequestion.isdisabled = 1
        selectedrangequestion.save()

        questionmarks = RangeQuestions.objects.filter(rangeid=rangeinstance, questionid = selectedquestioninstance).values_list('points')[0][0]
        updatedscore = rangeinstance.maxscore - questionmarks
        rangeinstance.maxscore = updatedscore
        rangeinstance.save()
        return redirect(previousurl)

class AssignUser(ListView, FilterView):
    template_name = 'teachers/assignuserrange.html'
    context_object_name = 'usersobject'
    paginate_by = 10
    filterset_class = StudentFilter

    def get_queryset(self):
        rangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        studentsinrange = RangeStudents.objects.filter(rangeID = rangeid).values_list('studentID')
        allstudents = User.objects.filter(is_superuser = False, is_staff = False).exclude(email__in=studentsinrange).order_by('-lastmodifieddate')
        print(allstudents)
        return allstudents

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classesobject'] = UserClass.objects.values_list('userclass')

        if "userrangecart" in self.request.session:
            cart = self.request.session.get('userrangecart', {})
            print("HI")
            print(cart)
            context['cart'] = cart

        return context

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
            question, topicname = self.form.save()
            optionone = request.POST.get('optionone',' ')
            answer = self.request.POST.get('answer','')
            points = self.request.POST.get('points','')
            registryid = self.request.POST.get('registryid','')
            questionid = question.questionid
            request.session['questionid'] = questionid
            questioninstance = Questions.objects.get(questionid = questionid)
            registryid = self.request.POST.get('registryid','')
            rangeinstance = Range.objects.get(rangeurl = self.kwargs['rangeurl'])
            rangequestionobject = RangeQuestions(rangeid = rangeinstance, questionid = questioninstance, answer = answer, points = points, registryid = registryid)
            rangequestionobject.save()

            currentrangescore = rangeinstance.maxscore
            if currentrangescore is None:
                currentrangescore = 0 + int(points)
            else: 
                currentrangescore += int(points)
            
            rangeinstance.maxscore = currentrangescore
            rangeinstance.save()
            request.session['TF'] = False

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
            ## IF THE USER IS DONE W CREATING QUESTION THEN WILL REDIRECT THEM TO VIEW RANGE ###
            if (request.POST.get('usedocker') == 'Yes' and request.POST.get('registryid') == ""):
                print("no registry")
                return ListView.get(self, request, *args, **kwargs)

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
                rangequestionobject = RangeQuestions.objects.get(questionid = questioninstance)
                rangequestionobject.answer = answer
                rangequestionobject.save()
                
                return ListView.get(self, request, *args, **kwargs)
            else:
                print("OMG")
                return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        currentmarks =  Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('maxscore')[0][0]
        return currentmarks

    def get_form_kwargs(self):
        kwargs = super(CreateQuestion, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questiontypechoices'] = QUESTION_TYPE_CHOICES
        context['rangename'] = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangename')[0][0]
        questiontopic = QuestionTopic.objects.all().values_list('topicname')
        context['questiontopic'] = questiontopic
        return context

class ActivateRange(View):
    def get(self, request, rangeurl):
        rangeobject = Range.objects.get(rangeurl = rangeurl)
        rangeobject.rangeactive = True
        rangeobject.save()
        return redirect('./')

class DeactivateRange(View):
    def get(self, request, rangeurl):
        rangeobject = Range.objects.get(rangeurl = rangeurl)
        rangeobject.rangeactive = False
        rangeobject.save()
        return redirect('./')

class QuestionManagement(ListView, FilterView):
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

class DockerManagement(ListView):
    template_name = 'teachers/dockermanagement.html'
    context_object_name = 'dockerobjects'
    paginate_by = 10

    def get_queryset(self):
        dockers = UnavailablePorts.objects.all()
        return dockers

class CreateImage(View):
    def get(self, request):
        data = {}
        id = request.POST.get('id')	
        endpoint1 = 'http://192.168.40.134:2376/images/create?fromImage=192.168.40.134:5000/{conid}'
        url1 = endpoint1.format(conid=id)
        response = requests.post(url1)
        if response.status_code == 200:
            data['Id'] = id
            data['message'] = 'success'
        elif response.status_code == 404:
            data['message'] = 'no such container'
        elif response.status_code == 500:
            data['message'] = 'conflict'
        else:
            data['message'] = 'Error %s' % response.status_code
        
        reference = {}
        range = request.POST.get('range')
        endpoint2 = 'http://192.168.40.134:2376/images/192.168.40.134:5000/{0}/tag?repo={1}'
        url2 = endpoint2.format(id, range)
        response = requests.post(url2)
        
        if response.status_code == 201:
            reference['Id'] = range
            reference['message'] = 'success'
        elif response.status_code == 400:
            reference['message'] = 'Bad Parameter'
        elif response.status_code == 404:
            reference['message'] = 'no such image'
        elif response.status_code == 409:
            reference['message'] = 'conflict'
        elif response.status_code == 500:
            reference['message'] = 'server error'
        else:
            reference['message'] = 'Error %s' % response.status_code

class AdminDockerKill(View):
    def get(self, request, containername):
        # delete old port if existing
        endpoint = 'http://localhost:3125/containers/{conid}?force=True'
        url = endpoint.format(conid=containername)
        response = requests.delete(url)
        endpoint = 'http://localhost:3125/containers/{conid}?force=True'
        url = endpoint.format(conid=containername)
        response = requests.delete(url)
        # need to delete from containernamed
        deleteportsdb = UnavailablePorts.objects.filter(containername = containername)
        deleteportsdb.delete()

        return redirect('/teachers/dockermanagement/')
