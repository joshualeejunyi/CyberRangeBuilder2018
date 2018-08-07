from django.core.exceptions import PermissionDenied
from accounts.models import *
from functools import wraps
from urllib.parse import urlparse
from django.http import HttpResponseRedirect, Http404

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.shortcuts import resolve_url, redirect


# The main use of this method decorator is to prevent a teacher from accessing the student portal side #
def user_is_student(function):
    def wrap(request, *args, **kwargs):

        profile = request.user
        if profile.is_staff == 0:
            return function(request, *args, **kwargs)
        else:
            raise Http404
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

# The use of this method decorator is to make sure that the user changes their password upon login if it is default or resetted password #
def change_password(function):
    def wrap(request, *args, **kwargs):
        profile = request.user
        if profile.isdefault == 1:
            if profile.is_staff == 1:
                redirecturl = ('/ranges/'+str(profile.username)+'/changepassword')
                print(redirecturl)
                return redirect(redirecturl)
        else:
            return function(request, *args, **kwargs)
    
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap