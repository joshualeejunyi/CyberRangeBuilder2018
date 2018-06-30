from django import forms
from accounts.models import *
import datetime

class AddGroup(forms.ModelForm):
    groupname = forms.CharField(label = "Group Name", widget=forms.TextInput(attrs={'class' : 'form-group has-feedback'})),
    class Meta:
        model = Group
        fields = ('groupname',)

class AddGroupCommit(AddGroup):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(AddGroupCommit, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        group = super().save(commit=False)
        group.datecreated = datetime.date.today()
        group.timecreated = datetime.datetime.now().time()
        group.grouppoints = 0
        admin = self.request.user
        group.createdby = User.objects.get(username = admin)

        if commit:
            group.save()
        return group
    
    class Meta:
        model = Group
        fields = ('groupname',)