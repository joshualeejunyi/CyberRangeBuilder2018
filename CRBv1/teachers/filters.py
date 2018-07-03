from accounts.models import *
from ranges.models import *
import django_filters

class StudentFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'userclass',]

class GroupFilter(django_filters.FilterSet):
    groupname = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Group
        fields = ['groupname']

class RangeFilter(django_filters.FilterSet):

    class Meta:
        model = Range
        fields = ['rangename', 'datecreated', 'datestart', 'timestart', 'dateend', 'timeend', 'maxscore', 'rangecode']

class QuestionFilter(django_filters.FilterSet):
    class Meta:
        model = Questions
        fields = ['title', 'questiontype', 'topicid__topicname']