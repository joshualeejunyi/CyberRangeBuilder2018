from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.edit import ModelFormMixin
from django.views import generic 
from accounts.models import *
from django.views.generic import View
# Create your views here.

class LoginRedirect():
    def loginsuccess(request):
        if request.user.is_staff:
            return redirect("/teachers")    
        else:
            return redirect("/dashboard")

class Landing():
    def redirectuser(request):
        if request.user.is_anonymous:
            return redirect("/login")
        else:
            return(LoginRedirect.loginsuccess(request))
            

class RegisterView(ListView, ModelFormMixin):
    template_name = 'accounts/register.html'
    context_object_name = 'classesobject'
    model = User
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            self.form.save()
            return redirect('/register/success/')
        else:
            return ListView.get(self, request, *args, **kwargs)
    
    def get_queryset(self):
        classes = UserClass.objects.all()
        return classes

class RegistrationSucess(generic.TemplateView):
    template_name = 'accounts/registersuccess.html'
