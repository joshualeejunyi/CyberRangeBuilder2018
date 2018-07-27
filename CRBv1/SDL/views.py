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
        context['teachers'] = User.objects.filter(is_staff=1).values_list('username', flat=True)
        return context

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
            postinstance = SDLPost.objects.get(postid=self.kwargs['postid'])
            user = self.request.user
            self.form.save(postinstance, user)
            return HttpResponseRedirect("")
        else:
            return ListView.get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtain comment IDs and commenter's emails
        commentidlist = SDLComment.objects.filter(postid=self.kwargs['postid']).values_list('commentid', flat=True).order_by('-dateposted','-timeposted')
        commenterlist = SDLComment.objects.filter(postid=self.kwargs['postid']).values_list('commenter',flat=True).order_by('-dateposted', '-timeposted')

        user = self.request.user

        # Obtain all comments from a post
        commentlist = []
        for id in commentidlist:
            comment = SDLComment.objects.filter(commentid=id).values_list('comment')[0][0]
            commentlist.append(comment)

        # Obtain all commenter usernames from a post
        usernamelist = []
        for id in commenterlist:
            username = User.objects.filter(email=id).values_list('username')[0][0]
            usernamelist.append(username)

        # Obtain date of comment of a post
        datepostedlist = []
        for id in commentidlist:
            dateposted = SDLComment.objects.filter(commentid=id).values_list('dateposted')[0][0]
            datepostedlist.append(dateposted)

        # Obtain time of comment of a post
        timepostedlist = []
        for id in commentidlist:
            timeposted = SDLComment.objects.filter(commentid=id).values_list('timeposted')[0][0]
            timepostedlist.append(timeposted)

        # Obtain list of booleans, which identify which comment is made by the current user.
        isuserlist = []
        for id in commenterlist:
            username = User.objects.filter(email=id).values_list('username')[0][0]
            if str(username) == str(user):
                isuser=1
            else:
                isuser=0
            isuserlist.append(isuser)

        # Obtain list of booleans, which identify which comment is made by a teacher.
        isteacherlist = []
        for id in commenterlist:
            isteacher = User.objects.filter(email=id).values_list('is_staff')[0][0]
            print(isteacher)
            if isteacher:
                teacher = 1
            else:
                teacher = 0
            isteacherlist.append(teacher)

        # Zipped a total of 7 lists to be sent to the template.
        context['comments'] = zip(commentidlist, commentlist, usernamelist, datepostedlist, timepostedlist, isuserlist, isteacherlist)

        return context

class DeleteComment(View):
    # After a user deletes their comment, they will simply be redirected to their own page.
    def get(self, request, commentid):
        postid = str(SDLComment.objects.filter(commentid=commentid).values_list('postid')[0][0])
        selectedcomment = SDLComment.objects.get(commentid = commentid)
        selectedcomment.delete()
        return redirect('/SDL/view/'+postid)