from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, ModelFormMixin, UpdateView, DeleteView, CreateView
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from settings.forms import *
from accounts.forms import *
from ranges.models import *
from accounts.models import User
from django.core.paginator import Paginator
from django_filters.views import FilterView
from django.views import View
from django.contrib import messages
from django.views.generic import RedirectView
from functools import reduce
from django.db.models.functions import Lower
from django.contrib.auth.mixins import PermissionRequiredMixin
import requests


class ModifyUser(UpdateView):
    form_class = UserModifyForm
    model = User
    template_name = 'settings/settings.html'
    success_url = '/settings/success'

    def get_object(self):
        user = self.request.user
        selecteduser = User.objects.get(username=user)
        return selecteduser

    def get_form_kwargs(self):
        kwargs = super(ModifyUser, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

class ResetPassword(UpdateView):
    form_class = ResetPasswordForm
    model = User
    template_name = 'settings/resetpassword.html'
    success_url = '/login/'

    def get_object(self):
        user = self.request.user
        selecteduser = User.objects.get(username=user)
        return selecteduser

    def get_form_kwargs(self):
        kwargs = super(ResetPassword, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

class ModifyUserSuccess(generic.TemplateView):
    template_name = 'settings/success.html'