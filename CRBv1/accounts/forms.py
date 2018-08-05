from .models import User, UserClass
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import AuthenticationForm
import re

class CheckUserDisabled(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if user.is_staff == False:
            if user.isdisabled == True :
                raise forms.ValidationError(
                    ("Your account has disabled. Please contact your administrator."),
                    code='inactive',
                )
            if user.isaccepted == False:
                raise forms.ValidationError(
                    ("Your account has not yet been accepted. Please contact your administrator."),
                    code='inactive',
                )

class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
                
class UserCreationForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
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

    userclass = forms.CharField(label = "Class", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),

    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
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
        
    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        username = cleaned_data.get("username")
        
        if not re.match("^[A-Za-z0-9_-]*$", username):
            msg = u"Username should only contain letters, numbers, dashes or underscore!"
            self._errors["username"] = self.error_class([msg])

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.isdisabled = True
        user.isaccepted = False
        userclass = self.cleaned_data.get("userclass")
        userclassobj = UserClass.objects.get(userclass = userclass.userclass)
        userclassobj.studentcount += 1
        userclassobj.save()
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.datejoined = datetime.date.today()
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'name', 'username', 'userclass',)

class AdminRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdminRegisterForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.datejoined = datetime.date.today()
        user.lastmodifieddate = datetime.date.today()
        user.lastmodifiedtime = datetime.datetime.now().time()
        admin = self.request.user
        user.lastmodifiedby = User.objects.get(username = admin)
        user.acceptedby = User.objects.get(username = admin)
        user.isdisabled = False
        user.isaccepted = True
        user.isacceptedby = User.objects.get(username = admin)

        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'name', 'username', 'userclass',)

class AdminModifyModelForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address', widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    username = forms.CharField(label = "Username", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    name = forms.CharField(label = "Full Name", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    userclass = forms.CharField(label = "Class", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),

    class Meta:
        model = User
        fields = ('name', 'username', 'userclass',)

class AdminResetPassword(forms.ModelForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
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

    class Meta:
        model = User
        fields = ('password1',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
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

class AdminResetCommit(AdminResetPassword):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdminResetCommit, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.datejoined = datetime.date.today()
        user.lastmodifieddate = datetime.date.today()
        user.lastmodifiedtime = datetime.datetime.now().time()
        admin = self.request.user
        user.lastmodifiedby = User.objects.get(username = admin)
        user.acceptedby = User.objects.get(username = admin)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('password1',)


class AdminModifyForm(AdminModifyModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdminModifyForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AdminModifyForm, self).clean()
        username = cleaned_data.get("username")
        
        if not re.match("^[A-Za-z0-9_-]*$", username):
            msg = u"Username should only contain letters, numbers, dashes or underscore!"
            self._errors["username"] = self.error_class([msg])

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.lastmodifieddate = datetime.date.today()
            admin = self.request.user
            user.lastmodifiedby = User.objects.get(username = admin)
            user.lastmodifiedtime = datetime.datetime.now().time()
            user.save()
        return user

    class Meta:
        model = User
        fields = ('name', 'username', 'userclass')

class TeacherRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(TeacherRegisterForm, self).__init__(*args, **kwargs)

    def save(self, request, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.datejoined = datetime.date.today()
        user.lastmodifieddate = datetime.date.today()
        user.lastmodifiedtime = datetime.datetime.now().time()
        user.is_staff = 1
        user.isdisabled = 0
        user.isaccepted = 1
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'name', 'username')