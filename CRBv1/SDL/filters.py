from SDL.models import *
import django_filters

class SDLPostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', initial="")

    class Meta:
        model = SDLPost
        fields = ['title', 'createdby__username', 'postactive']