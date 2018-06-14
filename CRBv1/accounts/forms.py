from .models import User
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation

class UserCreationForm(forms.ModelForm):
    errormessages = {
        'passwordmismatch': _("The two password fields didn't match."),
    }
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address'),
    username = forms.CharField(label = "Username"),
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput)
    password1 = forms.CharField(label=_("Password Confirmation"), strip=False, widget=forms.PasswordInput)

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
        fields = ('email', 'username', 'password')



class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'username', 'password')