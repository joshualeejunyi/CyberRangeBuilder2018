from django.views import generic
from django.views.generic.list import ListView, View
from django.views.generic.edit import ModelFormMixin
from SDL.models import SDLPost
from accounts.models import*
from django_filters.views import FilterView
from teachers.filters import *
from django.utils.dateparse import parse_date
from .filters import *
from .forms import *
import re
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from ranges.decorators import *

@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_student, name='dispatch')
class SDLView(FilterView, ListView):
    template_name = 'SDL/SDL.html'
    context_object_name = 'posts'
    paginate_by = 10
    filterset_class = SDLPostFilter

    # Returns all active posts
    def get_queryset(self):
        activeposts = SDLPost.objects.filter(postactive='1').order_by('-dateposted','-timeposted')
        return activeposts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Return list of teachers to select for search filter
        context['teachers'] = User.objects.filter(is_staff=1)
        return context

@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_student, name='dispatch')
class ViewPost(ListView, ModelFormMixin):
    template_name='SDL/viewpost.html'
    context_object_name = 'post'
    model = SDLPost
    form_class = SDLPostComment

    # Returns all posts
    def get_queryset(self):
        postid = self.kwargs['postid']
        post = SDLPost.objects.filter(postid=postid)
        return post

    # Obtain comment form arguments
    def get_form_kwargs(self):
        kwargs = super(ViewPost, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    # Once user submits a comment, they will be redirected to the same page.
    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            postid = self.kwargs['postid']
            postinstance = SDLPost.objects.get(postid=postid)
            user = self.request.user
            self.form.save(postinstance, user)
            url = '/selfdirected/view/' + postid
            return redirect(url)
        else:
            return ListView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        postid = self.kwargs['postid']
        comments = SDLComment.objects.filter(postid=postid)

        context['comments'] = comments
        
        return context

@method_decorator(change_password, name='dispatch')
@method_decorator(user_is_student, name='dispatch')
class DeleteComment(View):
    # After a user deletes their comment, they will simply be redirected to their own page.
    def get(self, request, commentid):
        postid = str(SDLComment.objects.filter(commentid=commentid).values_list('postid')[0][0])
        selectedcomment = SDLComment.objects.get(commentid = commentid)
        selectedcomment.delete()
        return redirect('/SDL/view/'+postid)