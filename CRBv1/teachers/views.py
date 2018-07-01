from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, ModelFormMixin, UpdateView, DeleteView
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