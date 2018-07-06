from .models import User, UserClass
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.forms import AuthenticationForm

class CheckUserDisabled(AuthenticationForm):
    def confirm_login_allowed(self, user):
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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.isdisabled = True
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