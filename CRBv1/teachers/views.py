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

# Create your views here.

class TeacherDashboard(generic.TemplateView):
    template_name = 'teachers/teacherdashboard.html'


class UserManagement(ListView):
    template_name = 'teachers/usermanagement.html'
    context_object_name = 'usersobject'
    paginate_by = 10

    def get_queryset(self):
        allstudents = User.objects.filter(is_superuser = False, is_staff = False).order_by('-lastmodifieddate')
        return allstudents

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

class GroupManagement(ListView):
    template_name = 'teachers/groupmanagement.html'
    context_object_name = 'groupobjects'

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
            for x in range(0, len(studentsingroup)):
                students = User.objects.filter(email = studentsingroup[x][0])
        else:
            students = None

        return students

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groupname'] = self.kwargs['groupname']

        return context

# class AddUserInGroup()