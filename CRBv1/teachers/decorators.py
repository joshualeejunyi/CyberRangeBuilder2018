from django.core.exceptions import PermissionDenied
from accounts.models import *
from functools import wraps
from urllib.parse import urlparse
from django.http import HttpResponseRedirect, Http404

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url

def user_is_staff(function):
    def wrap(request, *args, **kwargs):

        profile = request.user
        if profile.is_staff == 1:
            return function(request, *args, **kwargs)
        else:
            raise Http404
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap