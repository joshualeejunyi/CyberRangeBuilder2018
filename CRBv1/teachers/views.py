from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
<<<<<<< HEAD
from django.views.generic.edit import FormView, ModelFormMixin, UpdateView, DeleteView
from django.views import generic 
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms import *
=======
from django.views.generic.edit import FormView
from django.views import generic 
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms import RegisterForm
>>>>>>> bdb8423ccba0c0ca03a04d379199759b9343dedf
from ranges.models import *
from accounts.models import * 

# Create your views here.

class TeacherDashboard(generic.TemplateView):
    template_name = 'teachers/teacherdashboard.html'


<<<<<<< HEAD
class UserManagement(ListView):
=======
class UserManagement(generic.ListView):
>>>>>>> bdb8423ccba0c0ca03a04d379199759b9343dedf
    template_name = 'teachers/usermanagement.html'
    context_object_name = 'usersobject'

    def get_queryset(self):
<<<<<<< HEAD
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
=======
        allstudents = User.objects.filter(is_superuser = False, is_staff = False)
        print(allstudents)
        return allstudents
    

class AddUser(FormView):
    template_name = 'teachers/adduserform.html'
    form_class = RegisterForm
    success_url = 'success/'

    def form_valid(self, form):
        form.save()
        return render(self.request, 'teachers/addusersuccess.html', self.get_context_data())

# class ModifyUser(FormView):
>>>>>>> bdb8423ccba0c0ca03a04d379199759b9343dedf
