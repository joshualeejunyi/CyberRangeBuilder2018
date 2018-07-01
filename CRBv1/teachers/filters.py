from accounts.models import *
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