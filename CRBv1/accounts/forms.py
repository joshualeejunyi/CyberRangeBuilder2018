from .models import User, UserClass
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
import datetime

class UserCreationForm(forms.ModelForm):
    errormessages = {
        'passwordmismatch': _("The two password fields didn't match."),
    }
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address', widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    username = forms.CharField(label = "Username", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    name = forms.CharField(label = "Full Name", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    userclass = forms.CharField(label = "Class", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-group has-feedback'})),
    password1 = forms.CharField(label=_("Password Confirmation"), strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-group has-feedback'})),
    def clean_password(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password != password1:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password

    class Meta:
        model = User
        fields = ('email', 'name', 'username', 'userclass', 'password',)



class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.datejoined = datetime.date.today()
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'name', 'username', 'userclass', 'password',)

class AdminRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdminRegisterForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
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
        fields = ('email', 'name', 'username', 'userclass', 'password',)

class AdminModifyModelForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address', widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    username = forms.CharField(label = "Username", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    name = forms.CharField(label = "Full Name", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    userclass = forms.CharField(label = "Class", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),

    class Meta:
        model = User
        fields = ('name', 'username', 'userclass',)

class AdminResetPassword(forms.ModelForm):
    errormessages = {
        'passwordmismatch': _("The two password fields didn't match."),
    }
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-group has-feedback'})),
    password1 = forms.CharField(label=_("Password Confirmation"), strip=False, widget=forms.PasswordInput(attrs={'class' : 'form-group has-feedback'})),
    def clean_password(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password != password1:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password

    class Meta:
        model = User
        fields = ('password',)

class AdminResetCommit(AdminResetPassword):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdminResetCommit, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
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
        fields = ('password',)


class AdminModifyForm(AdminModifyModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AdminModifyForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            print(user)
            print(type(user))
            user.lastmodifieddate = datetime.date.today()
            admin = self.request.user
            user.lastmodifiedby = User.objects.get(username = admin)
            user.lastmodifiedtime = datetime.datetime.now().time()
            user.save()
        return user

    class Meta:
        model = User
        fields = ('name', 'username', 'userclass')