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

# Create your views here.

class TeacherDashboard(generic.TemplateView):
    template_name = 'teachers/teacherdashboard.html'


class UserManagement(FilterView, ListView):
    template_name = 'teachers/usermanagement.html'
    context_object_name = 'usersobject'
    paginate_by = 10
    filterset_class = StudentFilter

    def get_queryset(self):
        allstudents = User.objects.filter(is_superuser = False, is_staff = False).order_by('-lastmodifieddate')
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
        userslist = []
        if 'usercart' in request.session:
            userslist = request.session['usercart']
        userobject = username
        if username not in userslist:
            userslist.append(userobject)
        request.session['usercart'] = userslist

        url = "/teachers/groupmanagement/" + groupname + "/addusers"
        return redirect(url)

class RemoveUserFromCart(View):
    def get(self, request, groupname, username):
        get_object_or_404(User, username = username)
        userslist = []
        if 'usercart' in request.session:
            userslist = request.session['usercart']
        userobject = username
        if username in userslist:
            userslist.remove(userobject)
        request.session['usercart'] = userslist

        url = "/teachers/groupmanagement/" + groupname + "/addusers"
        return redirect(url)

class UserGroupCommit(View):
    def get(self, request, groupname):
        if 'usercart' in request.session:
            userslist = request.session['usercart']

        for student in userslist:
            #print(student)
            studentid = User.objects.get(username = student)
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
    success_url = '/teachers/groupmanagement/'
    def get_object(self, queryset = None):
        studentid = User.objects.get(username = self.kwargs['username'])
        groupname = self.kwargs['groupname']
        groupid = Group.objects.get(groupname = groupname)
        selecteduser = StudentGroup.objects.get(studentid = studentid, groupid = groupid)
        return selecteduser

class DeleteGroup(DeleteView):
    template_name = 'teachers/confirmdeletegroup.html'
    success_url = '/teachers/groupmanagement/'

    def get_object(self, queryset = None):
        groupname = self.kwargs['groupname']
        groupid = Group.objects.get(groupname = groupname)
        return groupid

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


class CreateRange(CreateView, RedirectView):
    template_name = 'teachers/rangemanagement.html'
    model = Range
    form_class = RangeForm

    def get_form_kwargs(self):
        kwargs = super(CreateRange, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        data = Range.objects.all()
        args = { 'form' : self.form, 'data' : data}
        return render(request, 'teachers/addrange.html', args)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.form.save()
            CreateQuestionForm = QuestionForm()
            return redirect('./createquestion', permanent=True)

        return render(request, 'teachers/rangemanagement.html')


class RangeView(FilterView, ListView):
    template_name = 'teachers/rangeview.html'
    context_object_name = 'result'
    filterset_class = QuestionFilter

    def get_queryset(self):
        selectedrange = Range.objects.get(rangename= self.kwargs['rangename'])
        selectedrangeid = selectedrange.rangeid
        print(selectedrangeid)
        # use range id to get the questionids in the current range
        questions = RangeQuestions.objects.filter(rangeid = selectedrangeid).values_list('questionid')
        #print("1 --> ORDER" + str(questions))
        if len(questions) != 0:
            # get the first object of assigned range (because need to declare var before our little concat trick later)
            result = Questions.objects.filter(questionid=(questions[0][0]))
            #print('2 --> ' + str(result))
            for x in range(1, len(questions)):
                #this for loop will concat all the assigned ranges together for our template to call
                currentquestion= Questions.objects.filter(questionid=(questions[x][0]))
                result = result | currentquestion # if i didn't get the first object just now python will scold me
                # print('3 --> ' + str(result))
        else:
            # if there are no questions return None if not rip cause it shouldn't be none
            result = None

        return result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selectedrange = Range.objects.get(rangename= self.kwargs['rangename'])
        selectedrangeid = selectedrange.rangeid
        # use range id to get the questionids in the current range
        questions = RangeQuestions.objects.filter(rangeid = selectedrangeid).values_list('questionid')
        #print("1 --> ORDER" + str(questions))
        if len(questions) != 0:
            # get the first object of assigned range (because need to declare var before our little concat trick later)
            result = RangeQuestions.objects.filter(questionid=(questions[0][0]))
            #print('2 --> ' + str(result))
            for x in range(1, len(questions)):
                #this for loop will concat all the assigned ranges together for our template to call
                currentquestion= RangeQuestions.objects.filter(questionid=(questions[x][0]))
                result = result | currentquestion # if i didn't get the first object just now python will scold me
                # print('3 --> ' + str(result))
        else:
            # if there are no questions return None if not rip cause it shouldn't be none
            result = None
        
        context['answer'] = result
        context['rangename'] = self.kwargs['rangename']
        context['range'] = Range.objects.filter(rangename = self.kwargs['rangename'])
        context['topics'] = QuestionTopic.objects.all()
        return context

class EditQuestion (UpdateView):
    form_class = QuestionForm
    model = Questions
    template_name = 'teachers/editquestion.html'
    success_url = 'teachers/'
    context_object_name = 'result'

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

class DeleteRange(View):
    def get(self, request, rangeid):
        selectedrange = Range.objects.get(rangeid=self.kwargs['rangeid'])
        selectedrange.isdisabled = True
        updatedrange = selectedrange
        updatedrange.save()
        url = "/teachers/rangemanagement/"
        return redirect(url)

class CreateQuestion(CreateView):
    template_name = "teachers/addquestion.html"
    model = Questions
    form_class = QuestionForm

    def get(self, request, *args, **kwargs):

        newest_range = Range.objects.order_by('-rangeid')[0]
        print(newest_range.rangename)
        questionnumber = 1
        CreateQuestionForm = QuestionForm()
        questiontopic = QuestionTopic.objects.all().values_list('topicname')

        FLAG = 'FL'
        MCQ = 'MCQ'
        SHORTANS = 'SA'
        OPENENDED = 'OE'
        TRUEFALSE = 'TF'
        questiontypechoices = (
            (FLAG, 'Flag'),
            (MCQ, 'Multiple Choice'),
            (SHORTANS, 'Short Answer'),
            (OPENENDED, 'Open Ended'),
            (TRUEFALSE, 'True/False')
        )
        currentmarks = 0
        args = {'rangename': newest_range.rangename,
                'questionnumber':questionnumber,
                'form' : CreateQuestionForm,
                'rangeid' : newest_range.rangeid,
                'questiontopic' : questiontopic,
                'questiontypechoices' : questiontypechoices,
                'currentmarks' : currentmarks
                }

        return render(request, 'teachers/addquestion.html', args)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if (request.POST.get('done')):
            print('user is done')
            hidden_currentmarks = request.POST.get('currentmarks')
            hidden_rangeid = request.POST.get('rangeid')
            currentrange = Range.objects.get(rangeid = hidden_rangeid)
            currentrange.maxscore = hidden_currentmarks
            currentrange.save()
            url = "/teachers/rangemanagement/"
            return redirect(url)

        if (request.POST.get('newtopicname')):
            form_newtopicname = request.POST.get('newtopicname')
            hidden_questionnumber = request.POST.get('questionnumber')
            hidden_rangename = request.POST.get('rangename')
            hidden_rangeid = request.POST.get('rangeid')
            hidden_currentmarks = request.POST.get('currentmarks')

            currenttopicnameavail = QuestionTopic.objects.all().values_list('topicname')
            topiclist = []
            for x in range(0, len(currenttopicnameavail)):
                topiclist.append(Lower(currenttopicnameavail[x][0]))

            lowercase_form_newtopicname = Lower(form_newtopicname)

            if lowercase_form_newtopicname not in topiclist:
                QuestionTopic_obj = QuestionTopic(topicname = form_newtopicname)
                QuestionTopic_obj.save()
                messages.success(request, 'New Question Topic Created ')

            else:
                messages.error(request, 'Topic Name Already Exists in Database ')

            CreateQuestionForm = QuestionForm()
            questiontopic = QuestionTopic.objects.all().values_list('topicname')
            FLAG = 'FL'
            MCQ = 'MCQ'
            SHORTANS = 'SA'
            OPENENDED = 'OE'
            TRUEFALSE = 'TF'
            questiontypechoices = (
                (FLAG, 'Flag'),
                (MCQ, 'Multiple Choice'),
                (SHORTANS, 'Short Answer'),
                (OPENENDED, 'Open Ended'),
                (TRUEFALSE, 'True/False')
            )
            
            args = {'rangename': hidden_rangename,
                'form': CreateQuestionForm,
                'questionnumber': hidden_questionnumber,
                'questiontopic' : questiontopic,
                'rangeid' : hidden_rangeid,
                'questiontypechoices' : questiontypechoices,
                'questiontopic' : questiontopic,
                'currentmarks' : hidden_currentmarks 
                }

            return render(request, 'teachers/addquestion.html', args)

        elif self.form.is_valid():
            print("form is valid")
            form_topicname = request.POST.get('topicname','')
            form_questiontype = request.POST.get('questiontype','')
            form_title = request.POST.get('title','')
            form_text = request.POST.get('text','')
            form_answer = request.POST.get('answer','')
            form_hint = request.POST.get('hint','')
            form_marks = request.POST.get('marks','')
            form_optionone = request.POST.get('optionone','')
            form_optiontwo = request.POST.get('optiontwo','')
            form_optionthree = request.POST.get('optionthree','')
            form_optionfour = request.POST.get('optionfour','')
            hidden_questionnumber = request.POST.get('questionnumber','')
            hidden_rangename = request.POST.get('rangename','')
            hidden_rangeid = request.POST.get('rangeid','')

            print(form_answer)
            print(form_topicname)
            topic_object = QuestionTopic.objects.get(topicname = form_topicname)
            Questions_obj = Questions(questiontype = form_questiontype,
                                      title = form_title,
                                      text = form_text,
                                      hint = form_hint,
                                      marks = form_marks,
                                      topicid = topic_object
                                      )
            Questions_obj.save()

            newest_questions_id = Questions.objects.order_by('-questionid')[0]
            newest_question_object = Questions.objects.get(questionid = newest_questions_id.questionid)
            newest_range_object = Range.objects.get(rangeid = hidden_rangeid)
            RangeQuestions_obj = RangeQuestions(rangeid = newest_range_object,
                                                questionid = newest_question_object,
                                                answer = form_answer)

            RangeQuestions_obj.save()

            if form_questiontype == 'MCQ':
                MCQ_obj = MCQOptions(questionid = newest_question_object,
                                     optionone = form_optionone,
                                     optiontwo = form_optiontwo,
                                     optionthree = form_optionthree,
                                     optionfour = form_optionfour)

                MCQ_obj.save()

            questionnumber = int(hidden_questionnumber) + 1

            CreateQuestionForm = QuestionForm()

            FLAG = 'FL'
            MCQ = 'MCQ'
            SHORTANS = 'SA'
            OPENENDED = 'OE'
            TRUEFALSE = 'TF'
            questiontypechoices = (
                (FLAG, 'Flag'),
                (MCQ, 'Multiple Choice'),
                (SHORTANS, 'Short Answer'),
                (OPENENDED, 'Open Ended'),
                (TRUEFALSE, 'True/False')
            )
            questiontopic = QuestionTopic.objects.all().values_list('topicname')
            
            hidden_currentmarks = request.POST.get('currentmarks')
            added_question_marks = Questions.objects.get(questionid = newest_questions_id.questionid)
            totalmarks = int(hidden_currentmarks) + int(added_question_marks.marks)
            messages.success(request, 'Question Created Successfully')
            args = {'rangename': hidden_rangename,
                    'form': CreateQuestionForm,
                    'questionnumber': questionnumber,
                    'questiontopic' : questiontopic,
                    'rangeid' : hidden_rangeid,
                    'questiontypechoices' : questiontypechoices,
                    'questiontopic' : questiontopic,
                    'currentmarks' : totalmarks 
                    }
            return render(request, 'teachers/addquestion.html', args)

        else:
            print(self.form.errors)
            return render(request, 'teachers/base.html')