from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views import generic 
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms import RegisterForm
from ranges.models import *
from accounts.models import * 

# Create your views here.

class TeacherDashboard(generic.TemplateView):
    template_name = 'teachers/teacherdashboard.html'


class UserManagement(generic.ListView):
    template_name = 'teachers/usermanagement.html'
    context_object_name = 'usersobject'

    def get_queryset(self):
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
