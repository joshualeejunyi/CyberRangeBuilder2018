from accounts.models import User, UserClass
from django import forms
from django.utils.translation import gettext, gettext_lazy as _

from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

from django.contrib.auth import password_validation
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import AuthenticationForm
import re

class UserModifyModelForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address', widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    username = forms.CharField(label = "Username", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    name = forms.CharField(label = "Full Name", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean(self):
        cleaned_data = super(UserModifyModelForm, self).clean()
        username = cleaned_data.get("username")
        
        if not re.match("^[A-Za-z0-9_-]*$", username):
            msg = u"Username should only contain letters, numbers, dashes or underscore!"
            self._errors["username"] = self.error_class([msg])

    class Meta:
        model = User
        fields = ('name', 'username',)

class UserModifyForm(UserModifyModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(UserModifyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.lastmodifieddate = datetime.date.today()
        user.lastmodifiedtime = datetime.datetime.now().time()
        admin = self.request.user
        user.lastmodifiedby = User.objects.get(username = admin)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('name', 'username',)


class ResetPasswordModelForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address', widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'wrong_old_password': _("You entered the wrong existing password."),
    }

    oldpassword = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        user = self.request.user
        oldpassword = self.cleaned_data.get("oldpassword")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        matchcheck = user.check_password(oldpassword)

        print(matchcheck)

        if not matchcheck:
            raise forms.ValidationError(
                self.error_messages['wrong_old_password'],
                code='wrong_old_password',
            )

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    class Meta:
        model = User
        fields = ('password1',)

class ResetPasswordForm(ResetPasswordModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ResetPasswordForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.lastmodifieddate = datetime.date.today()
        user.lastmodifiedtime = datetime.datetime.now().time()
        admin = self.request.user
        user.lastmodifiedby = User.objects.get(username = admin)
        user.isdefault = False
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('password1',)
