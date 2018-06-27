from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.edit import ModelFormMixin
from django.views import generic 
from accounts.models import *
# Create your views here.

<<<<<<< HEAD
class LoginRedirect():
    def loginsuccess(request):
        if request.user.is_staff:
            return redirect("/teachers")    
        elif request.user.is_superuser:
            return redirect("/admin")
        else:
            return redirect("/dashboard")
=======
def loginsuccess(request):
    if request.user.is_staff:
        return redirect("/teachers")    
    elif request.user.is_superuser:
        return redirect("/admin")
    else:
        return redirect("/dashboard")
>>>>>>> bdb8423ccba0c0ca03a04d379199759b9343dedf

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
    
    def get_queryset(self):
        classes =  UserClass.objects.values_list('userclass')
        return classes

class RegistrationSucess(generic.TemplateView):
    template_name = 'accounts/registersuccess.html'