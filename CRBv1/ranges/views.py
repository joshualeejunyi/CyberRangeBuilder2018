from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import ModelFormMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic 
from .models import *
from .forms import *
import datetime
from django.utils import timezone
from django.urls import reverse
import requests
from django.views.generic import View
from django.contrib import messages
from accounts.models import User
import string
import random
from pexpect import pxssh

class ShellRandomPassword(View):
    def get(self, request, portnumber):
        randompass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        s = pxssh.pxssh()
        if not s.login ('192.168.100.42', port=portnumber, username='guest',password='root'):
            return HttpResponse(s)
        else:
            s.sendline ('passwd %s' % randompass)
            s.prompt()         # match the prompt
            # print everything before the prompt.
            s.logout()
            return randompass

class EnterCode(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ranges/joinrange.html')
    
    def post(self, request, *args, **kwargs):
        form_rangecode = request.POST.get('rangecode')
        
        try:
            selectedrange = Range.objects.get(rangecode = form_rangecode, isopen=1)
            user = self.request.user
            #print(user)
            requestuser = User.objects.get(username = user)
            requestemail = requestuser.email
            #print(requestemail)

            try:
                checkifstudentinrange = RangeStudents.objects.get(rangeid = selectedrange,
                                                                  email = requestuser)
                messages.error(request,'You already belong in the range')
                return render(request, 'ranges/entercode.html')

            except RangeStudents.DoesNotExist:
                datetimenow = datetime.datetime.now()
                rangestudents_obj = RangeStudents(rangeID = selectedrange,
                                                studentID = requestuser,
                                                dateJoined = datetimenow)
                
                rangestudents_obj.save()
                messages.success(request, 'Successfully Joined The Range')
                return render(request, 'ranges/joinrange.html')

        except Range.DoesNotExist:
            selectedrange = None
            messages.error(request, 'Invalid Range Code or Range Is Not Open')
            return render(request, 'ranges/joinrange.html')

class DockerKill(View):
    def get(self, request):
        # delete old port if existing
        previousport = UnavailablePorts.objects.filter(studentid = self.request.user).values_list('portnumber')
        if previousport:
            #print("HI")
            port = previousport[0][0]
            containername = UnavailablePorts.objects.filter(studentid = self.request.user).values_list('containername')[0][0]
            if int(port) >= 9051:
                serverip = '192.168.100.42'
            elif int(port) <= 9050:
                serverip = '192.168.100.43'
            #serverip = 'localhost'
            endpoint = 'http://' + serverip + ':8051/containers/{conid}?force=True'
            url = endpoint.format(conid=containername)
            #print(url)
            response = requests.delete(url)
            # need to delete from db
            deleteportsdb = UnavailablePorts.objects.filter(studentid = self.request.user)
            deleteportsdb.delete()
            
        # timeout for ports
        allentriesinportsdb = UnavailablePorts.objects.all()
        if allentriesinportsdb != 0:
            for entry in allentriesinportsdb:
                timediff = timezone.now() - entry.datetimecreated 
                #print(timediff)
                if timediff > datetime.timedelta(hours = 3):
                    containername = entry.containername
                    port = entry.portnumber
                    if int(port) >= 9052:
                        serverip = '192.168.100.42'
                    elif int(port) <= 9050:
                        serverip = '192.168.100.43'
                    #serverip = 'localhost'
                    endpoint = 'http://' + serverip + ':8051/containers/{conid}?force=True'
                    url = endpoint.format(conid=containername)
                    response = requests.delete(url)
                    
                    # need to delete from db
                    deleteportsdb = UnavailablePorts.objects.filter(studentid = self.request.user)
                    deleteportsdb.delete()

class AttemptQuestionView(ListView, ModelFormMixin):
    template_name = 'ranges/attemptquestion.html'
    context_object_name = 'question'
    model = StudentQuestions
    form_class = AnswerForm

    def checkPorts(self):
        database = UnavailablePorts.objects.all().values_list('portnumber')
        size = len(database)
        #print(size)

        dockerserver = []
        webserver = []

        if size > 0:
            # check if the database has any values
            for x in range(0, size):
                # if the port belongs to databaseserver, append to database list
                if database[x][0] <= 9050:
                    webserver.append(database[x])
                # if the port belongs to dockerserver, append to dockerserver list
                elif database[x][0] >=9051:
                    dockerserver.append(database[x])
        
        else:
            #return first available port for docker server
            return 9051

        #print('FIRST --->')
        #print(dockerserver, webserver)

        webserversize = len(webserver)
        dockerserversize = len(dockerserver)
        #print('SECOND --->')
        #print(webserversize, dockerserversize)
        
        if dockerserversize < 48:
            if int(dockerserver[dockerserversize - 1][0]) == 9098:
                for x in range(0, 46):
                    if int(dockerserver[x + 1][0]) - int(dockerserver[x][0]) != 1:
                        result = int(dockerserver[x][0]) + 1
                        return result
            else:
                result = int(dockerserver[dockerserversize - 1][0]) + 1
                return result
        elif webserversize < 50:
            if int(webserver[webserversize - 1][0]) == 9050:
                for x in range(0, 48):
                    if int(webserver[x + 1][0]) - int(webserver[x][0]) != 1:
                        result = int(webserver[x][0]) + 1
                        return result
            else:
                result = int(webserver[webserversize - 1][0]) + 1
                return result
        else:
            return -1

    def dockerContainerStart(self):
        # okay so before we start a new docker container
        # we need to check if there are any open containers
        # we have stored it in the session
        data = {}
        port = self.checkPorts()
        serverip = ''
        if port == -1:
            return HttpResponse('SERVER BUSY. PLEASE TRY AGAIN LATER.')
        # port 8051 is reserved for API
        elif port >= 9051:
            serverip = '192.168.100.42'
        elif port <= 9050:
            serverip = '192.168.100.43'
        port = str(port)
        rangename = self.kwargs['rangeurl']
        questionnumber = self.kwargs['questionid']
        imagename = str(rangename + '.' + questionnumber)
        #image = 'siab_server'
        payload = {
            'Image':imagename,
            'HostConfig': {
                "PortBindings": {
                "4200/tcp": [{
                    "HostIp": "",
                    "HostPort": port
                    }
                ],
                "22/tcp": [{
                    "HostIp": "",
                    "HostPort": '9052'
                }]
                }
            }
        }
        #serverip = 'localhost'
        url = 'http://' + serverip + ':8051/containers/create'
        response = requests.post(url, json=payload)
        #print('HI IM HERE')
        #print(response.status_code)
        if response.status_code == 201:
            test = True
            data = response.json()
            containerid = data['Id']
            starturl = 'http://' + serverip + ':8051/containers/%s/start' % containerid
            response = requests.post(starturl)

            portsdb = UnavailablePorts(portnumber = int(port), studentid = self.request.user, containername = containerid, datetimecreated = timezone.now())
            portsdb.save()
            # for testing
            finalsiaburl = 'dmit2.bulletplus.com:' + port
            #randompassword = ShellRandomPassword.get(self, self.request, portnumber = port)
            randompassword = False
            return randompassword, finalsiaburl

        elif response.status_code == 400:
            return redirect('/error')
        elif response.status_code == 409:
            return redirect('/error')
        else:
            return redirect('/error')


    def checkattemptlimit(self):
        attempted = False
        user = self.request.user
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        rangeurl = self.kwargs['rangeurl']
        rangeid = Range.objects.filter(rangeurl=rangeurl).values_list('rangeid')[0][0]
        numberofattempts = len(StudentQuestions.objects.filter(studentid = user, rangeid = rangeid, questionid = questioninstance))
        maxattempts = Range.objects.filter(rangeid = rangeid).values_list('attempts')[0][0]
        if maxattempts != 0 and numberofattempts == maxattempts:
            attempted = True
        return attempted

    def latestanswer(self):
        user = self.request.user
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        rangeurl = self.kwargs['rangeurl']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        result = StudentQuestions.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance).values_list('answergiven')
        if len(result) != 0:
            result = result[len(result) - 1][0]
        else:
            result = None
        print('-------------------------------------------------------result')
        print(result)
        
        return result

    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            user = self.request.user
            answergiven = self.form.cleaned_data['answergiven']
            questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
            rangeurl = self.kwargs['rangeurl']
            rangeinstance = Range.objects.get(rangeurl = rangeurl)
            questionid = Questions.objects.filter(questionid = self.kwargs['questionid']).values_list('questionid')[0][0]
            check = self.form.checkAnswer(user, answergiven, questioninstance, rangeinstance, questionid)
            return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        DockerKill.get(self, self.request)
        self.questionid = get_object_or_404(Questions, questionid=self.kwargs['questionid'])
        self.rangeid = get_object_or_404(Range, rangeurl=self.kwargs['rangeurl'], rangeactive=1)
        #print("1 --> " + str(self.kwargs['questionid']))
        question = Questions.objects.filter(questionid = self.kwargs['questionid'])[0]
        #print("2 --> "+ str(question))
        return question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionid = self.kwargs['questionid']
        rangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        usedocker = Questions.objects.filter(questionid = questionid).values_list('usedocker')[0][0]
        if usedocker is True:
            password, siab = self.dockerContainerStart()
            context['siab'] = siab
            context['password'] = password
        else:
            context['siab'] = False
            context['password'] = False

        context['hitmaxattempts'] = self.checkattemptlimit()
        print('----------------------------------')
        print(context['hitmaxattempts'])
        print('----------------------------------')
        context['latestanswer'] = self.latestanswer()

        #gotta check if it's mcq, and if it is, get options from database
        # first i gotta get the questionobject
        questiontype = Questions.objects.filter(questionid = questionid).values_list('questiontype')[0][0]

        if questiontype == 'MCQ':
            options = MCQOptions.objects.filter(questionid = questionid)
            context['mcqoptions'] = options

        context['questionpoints'] = Questions.objects.filter(rangeid = self.rangeid, questionid = questionid).values_list('points')[0][0]
        
        hintactivated = StudentHints.objects.filter(rangeid = self.rangeid, questionid = questionid, studentid = self.request.user).values_list('hintactivated')
        if len(hintactivated) != 0:
            hint = hintactivated[0][0]
        else:
            hint = None
        context['hint'] = hint

        correctcheck = StudentQuestions.objects.filter(studentid = self.request.user, rangeid = rangeid, questionid = questionid, answercorrect = 1)
        if len(correctcheck) == 1:
            context['correct'] = True
        else:
            context['correct'] = False
        print('>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<')
        print(context['correct'])

        questiontopic = Questions.objects.filter(rangeid = self.rangeid, questionid = questionid).values_list('topicid')[0][0]
        topicname = QuestionTopic.objects.filter(topicid = questiontopic).values_list('topicname')[0][0]
        context['topic'] = topicname

        return context


class AttemptMCQQuestionView(ListView, ModelFormMixin):
    template_name = 'ranges/attemptquestion.html'
    context_object_name = 'question'
    model = StudentQuestions
    form_class = AnswerMCQForm

    def checkPorts(self):
        database = UnavailablePorts.objects.all().values_list('portnumber')
        size = len(database)
        #print(size)

        dockerserver = []
        webserver = []

        if size > 0:
            # check if the database has any values
            for x in range(0, size):
                # if the port belongs to databaseserver, append to database list
                if database[x][0] <= 9050:
                    webserver.append(database[x])
                # if the port belongs to dockerserver, append to dockerserver list
                elif database[x][0] >=9051:
                    dockerserver.append(database[x])
        
        else:
            #return first available port for docker server
            return 9051

        #print('FIRST --->')
        #print(dockerserver, webserver)

        webserversize = len(webserver)
        dockerserversize = len(dockerserver)
        #print('SECOND --->')
        #print(webserversize, dockerserversize)
        
        if dockerserversize < 48:
            if int(dockerserver[dockerserversize - 1][0]) == 9098:
                for x in range(0, 46):
                    if int(dockerserver[x + 1][0]) - int(dockerserver[x][0]) != 1:
                        result = int(dockerserver[x][0]) + 1
                        return result
            else:
                result = int(dockerserver[dockerserversize - 1][0]) + 1
                return result
        elif webserversize < 50:
            if int(webserver[webserversize - 1][0]) == 9050:
                for x in range(0, 48):
                    if int(webserver[x + 1][0]) - int(webserver[x][0]) != 1:
                        result = int(webserver[x][0]) + 1
                        return result
            else:
                result = int(webserver[webserversize - 1][0]) + 1
                return result
        else:
            return -1

    def dockerContainerStart(self):
        # okay so before we start a new docker container
        # we need to check if there are any open containers
        # we have stored it in the session
        data = {}
        port = self.checkPorts()
        serverip = ''
        if port == -1:
            return HttpResponse('SERVER BUSY. PLEASE TRY AGAIN LATER.')
        # port 8051 is reserved for API
        elif port >= 9051:
            serverip = '192.168.100.42'
        elif port <= 9050:
            serverip = '192.168.100.43'
        port = str(port)
        rangename = self.kwargs['rangeurl']
        questionnumber = self.kwargs['questionid']
        imagename = str(rangename + '.' + questionnumber)
        #image = 'siab_server'
        payload = {
            'Image':imagename,
            'HostConfig': {
                "PortBindings": {
                "4200/tcp": [{
                    "HostIp": "",
                    "HostPort": port
                    }
                ],
                "22/tcp": [{
                    "HostIp": "",
                    "HostPort": '9052'
                }]
                }
            }
        }
        #serverip = 'localhost'
        url = 'http://' + serverip + ':8051/containers/create'
        response = requests.post(url, json=payload)
        #print('HI IM HERE')
        #print(response.status_code)
        if response.status_code == 201:
            test = True
            data = response.json()
            containerid = data['Id']
            starturl = 'http://' + serverip + ':8051/containers/%s/start' % containerid
            response = requests.post(starturl)

            portsdb = UnavailablePorts(portnumber = int(port), studentid = self.request.user, containername = containerid, datetimecreated = timezone.now())
            portsdb.save()
            # for testing
            finalsiaburl = 'dmit2.bulletplus.com:' + port
            #randompassword = ShellRandomPassword.get(self, request, portnumber = port)
            randompassword = False
            return randompassword, finalsiaburl

        elif response.status_code == 400:
            return redirect('/error')
        elif response.status_code == 409:
            return redirect('/error')
        else:
            return redirect('/error')

    def checkattemptlimit(self):
        attempted = False
        user = self.request.user
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        rangeurl = self.kwargs['rangeurl']
        rangeid = Range.objects.filter(rangeurl=rangeurl).values_list('rangeid')[0][0]
        numberofattempts = len(StudentQuestions.objects.filter(studentid = user, rangeid = rangeid, questionid = questioninstance))
        maxattempts = Range.objects.filter(rangeid = rangeid).values_list('attempts')[0][0]
        if maxattempts != 0 and numberofattempts == maxattempts:
            attempted = True
        return attempted

    def latestanswer(self):
        user = self.request.user
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        rangeurl = self.kwargs['rangeurl']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        result = StudentQuestions.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance).values_list('answergiven')
        if len(result) != 0:
            result = result[len(result) - 1][0]
        else:
            result = None
        print('-------------------------------------------------------result')
        print(result)
        
        return result

    def get_form_kwargs(self):
        kwargs = super(AttemptMCQQuestionView, self).get_form_kwargs()
        list = ['one', 'two', 'three', 'four']
        newlist = []
        for x in list:
            options = MCQOptions.objects.filter(questionid = self.kwargs['questionid']).values_list('option'+str(x))[0][0]
            choice = (options, options)
            #print(choice)
            newlist.append(choice)
            #print(newlist)
        kwargs['choices'] = newlist
        return kwargs
    
    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)

        if self.form.is_valid():
            user = self.request.user
            answergiven = self.form.cleaned_data['answergiven']
            questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
            rangeurl = self.kwargs['rangeurl']
            rangeinstance = Range.objects.get(rangeurl = rangeurl)
            questionid = Questions.objects.filter(questionid = self.kwargs['questionid']).values_list('questionid')[0][0]
            check = self.form.checkAnswer(user, answergiven, questioninstance, rangeinstance, questionid)
            return ListView.get(self, request, *args, **kwargs)

    
    def get_queryset(self):
        DockerKill.get(self, self.request)
        self.questionid = get_object_or_404(Questions, questionid=self.kwargs['questionid'])
        self.rangeid = get_object_or_404(Range, rangeurl=self.kwargs['rangeurl'], rangeactive=1)
        #print("1 --> " + str(self.kwargs['questionid']))
        question = Questions.objects.filter(questionid = self.kwargs['questionid'])[0]
        #print("2 --> "+ str(question))
        return question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questionid = self.kwargs['questionid']
        rangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        usedocker = Questions.objects.filter(questionid = questionid).values_list('usedocker')[0][0]
        if usedocker is True:
            password, siab = self.dockerContainerStart()
            context['siab'] = siab
            context['password'] = password
        else:
            context['siab'] = False
            context['password'] = False

        context['hitmaxattempts'] = self.checkattemptlimit()
        context['latestanswer'] = self.latestanswer()

        #gotta check if it's mcq, and if it is, get options from database
        # first i gotta get the questionobject
        questiontype = Questions.objects.filter(questionid = questionid).values_list('questiontype')[0][0]

        if questiontype == 'MCQ':
            options = MCQOptions.objects.filter(questionid = questionid)
            context['mcqoptions'] = options

        context['questionpoints'] = Questions.objects.filter(rangeid = self.rangeid, questionid = questionid).values_list('points')[0][0]
        
        hintactivated = StudentHints.objects.filter(rangeid = self.rangeid, questionid = questionid, studentid = self.request.user).values_list('hintactivated')
        if len(hintactivated) != 0:
            hint = hintactivated[0][0]
        else:
            hint = None
        context['hint'] = hint

        correctcheck = StudentQuestions.objects.filter(studentid = self.request.user, rangeid = rangeid, questionid = questionid, answercorrect = 1)
        if len(correctcheck) == 1:
            context['correct'] = True
        else:
            context['correct'] = False
        print('>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<')
        print(context['correct'])
        return context


class ActivateHint(View):
    def get(self, request, questionid, rangeurl):
        user = self.request.user
        hintobj = StudentHints()
        hintobj.studentid = user
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        hintobj.rangeid = rangeinstance
        questioninstance = Questions.objects.get(questionid = questionid)
        hintobj.questionid = questioninstance
        hintobj.hintactivated = True
        hintobj.save()

        return redirect('./')


class QuestionsView(ListView):
    template_name = 'ranges/questions.html'
    context_object_name = 'questionobject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # first i need to get the range id.
        rangeurl = self.kwargs['rangeurl'] # get the rangename from the kwargs (url)
        # another thing to get is the current range id using rangeurl we got above
        currentrangeid = Range.objects.filter(rangeurl = rangeurl).values_list('rangeid')[0][0]
        # get the email address of current user
        username = self.request.user
        email = User.objects.filter(username = username).values_list('email')[0][0]
        # this is when the user opens the range
        # we need to enter this time as the last access
        rangestudentobj = RangeStudents.objects.get(rangeID = currentrangeid, studentID = email)
        rangestudentobj.lastaccess = datetime.datetime.now()
        rangestudentobj.save()

        # i need to find all the topics in a single range.
        # how do i do it?
        # what do i need?
        # i need to get the categories that appear in the range
        # how do i get that?
        # i need to get the questionids in the range (rangequestions)
        # then i need to get the categoryids of the questions (question)
        # do i need the categoryname?

        # get the questionids of the questions in the range in a queryset
        questionidsinrange = Questions.objects.filter(rangeid = currentrangeid).values_list("questionid")
        #print("firstquestionid ----->>>>>" + str(questionidsinrange))

        # create empty list for topics
        topiclist = []

        if len(questionidsinrange) != 0:
            #print("number --->>>>> " + str(len(questionidsinrange)))
            # get the queryset of the topicid of the first question
            topicidqueryset = Questions.objects.filter(questionid = (questionidsinrange[0][0]))
            #print("firstquestiontopic ----->>>>>> " + str(topicidqueryset))

            # loop so that i can get all the topic ids of the questions in the range
            for x in range(0, len(questionidsinrange)):
                #print("HI")
                currenttopicidqueryset = Questions.objects.filter(questionid=(questionidsinrange[x][0]))
                currenttopicidforlistinteger = Questions.objects.filter(questionid=(questionidsinrange[x][0])).values_list("topicid")[0][0]


                # check if the topic id is repeated, if its not, add to the list and append to queryset to get the QUESTIONS QUERYSET
                if currenttopicidforlistinteger not in topiclist:
                    topiclist.append(currenttopicidforlistinteger)  
                    topicidqueryset = topicidqueryset | currenttopicidqueryset

                    # but i need the questiontopic queryset
                    #print("TEST PLS WORK PLPSPLSPLS ----->>> " + str(topiclist[0]))

                    # get the first topicid for the loop
                    questiontopicqueryset = QuestionTopic.objects.filter(topicid = topiclist[0])
                    # check the list of topic ids
                    for tid in topiclist:
                        # gotta remove the first one cause we already have that in the variable
                        if tid != topiclist[0]:
                            # get the topic ids of all the topics in the range through the for loop
                            qs = QuestionTopic.objects.filter(topicid = tid)
                            # append the queryset together
                            questiontopicqueryset = questiontopicqueryset | qs

                # test print
                #print("TOPICS ------>>>>> " + str(questiontopicqueryset))
        else:
            # probably won't be none but still
            questiontopicqueryset = None

        # return topics as a context YEBOI YAY ME
        context['topics'] = questiontopicqueryset
        #print("OMG FML ___>>>" + str(context['topics']))

        # gotta get the instance cause django
        rangeinstance = Range.objects.get(rangeurl = rangeurl)

        # get the user id 
        user = self.request.user
        
        # get the queryset of the attempted questions that are correct
        correct = StudentQuestions.objects.filter(studentid = user, rangeid = currentrangeid, answercorrect = 1)
        context['correct'] = correct

        correctquestionsqueryset = Questions.objects.none()
        correctquestionslist = []
        for x in correct:
            correctquestionslist.append(x.questionid.questionid)
            correctquestionsqueryset = correctquestionsqueryset | Questions.objects.filter(rangeid = currentrangeid, questionid = x.questionid.questionid)

        # get the queryset of attempted questions that are not correct
        attemptedquestionid = StudentQuestions.objects.filter(studentid = user, rangeid = currentrangeid, answercorrect = 0).values('questionid').distinct()
        distinctquestions = Questions.objects.none()
        for questionid in attemptedquestionid:
            distinctquestionid = questionid.get('questionid')
            if distinctquestionid not in correctquestionslist:            
                distinctquestions = distinctquestions | Questions.objects.filter(questionid = distinctquestionid, rangeid = currentrangeid, isarchived = False)                
        context['attemptedquestions'] = distinctquestions
        allrangequestions = Questions.objects.filter(rangeid=currentrangeid, isarchived = False)

        thingstoexclude = distinctquestions | correctquestionsqueryset
        unattemptedquestions = Questions.objects.filter(rangeid=currentrangeid, isarchived =False).exclude(questionid__in=thingstoexclude)
        context['unattemptedquestions'] = unattemptedquestions

        print('--------------------------------------------')
        print('correct questions:')
        print(context['correct'])
        print(correctquestionslist)
        print(correctquestionsqueryset)
        print('attempted but not correct:')
        print(context['attemptedquestions'])
        print('unattempted:')
        print(context['unattemptedquestions'])
        print('--------------------------------------------')

        context['rangename'] = Range.objects.filter(rangeurl = rangeurl).values_list('rangename')[0][0]

        # okay i need the score that the user has in this range
        # also need the total score

        userscored = RangeStudents.objects.filter(rangeID = currentrangeid, studentID = user).values_list('points')[0][0]
        maxscore = Range.objects.filter(rangeurl = rangeurl).values_list('maxscore')[0][0]
        if maxscore is None or maxscore == 0:
            maxscore = 0
            percent = 0
        else:
            percent = int(userscored ) / int(maxscore) * 100
        context['userscored'] = userscored
        context['maxscore'] = maxscore
        context['percent'] = percent
        points = Questions.objects.filter(rangeid = currentrangeid)
        context['questionpoints'] = points
        context['rangeinfo'] = Range.objects.filter(rangeurl= rangeurl).values_list('rangeinfo')[0][0]
        adminemail = Range.objects.filter(rangeurl= rangeurl).values_list('createdbyusername')[0][0]
        adminusername = User.objects.filter(email=adminemail).values_list('name')[0][0]
        #print(adminusername)
        context['rangeadmin'] = adminusername
        context['attempts'] = Range.objects.filter(rangeurl=rangeurl).values_list('attempts')[0][0]
        rangeid = Range.objects.filter(rangeurl=rangeurl).values_list('rangeid')[0][0]
        #context['studentattempted'] = StudentQuestions.objects.filter(studentid = user, rangeid = rangeid)

        ## i need to get the number of attempts the student tried
        # first i'll get the distinct questionids that the student has already attempted
        studentattempts = StudentQuestions.objects.filter(studentid = user, rangeid = rangeid).values('questionid').distinct()
        # next, i will declare an empty queryset so I can concatenate later
        studentattemptsqueryset = StudentQuestions.objects.none()
        # i'll use a for loop to loop through all the questionids
        for questionid in studentattempts:
            # first need to get the questionid 
            studentattemptquestionid = questionid.get('questionid')
            # then i filter the database queryset by the question id, and get the length of the queryset (meaning the number of attempts)
            numberofattempts = len(StudentQuestions.objects.filter(studentid = user, rangeid = rangeid, questionid = studentattemptquestionid))
            # after that i will concatencate the main queryset with the filtered object with the latest number of attempts
            studentattemptsqueryset = studentattemptsqueryset | StudentQuestions.objects.filter(studentid = user, rangeid = rangeid, questionid = studentattemptquestionid, attempts = numberofattempts)

        # assign the studentattempts context with the final queryset
        context['studentattempts'] = studentattemptsqueryset
       
        ## i also need the points they got awarded with (in case they use hints or whatever)
        # this should be about the same as before
        # wait actually i can use the queryset from above

        return context

    def get_queryset(self):
        self.rangeurl = get_object_or_404(Range, rangeurl=self.kwargs['rangeurl'], rangeactive=1)
        DockerKill.get(self, self.request)
        currentrangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        questions = Questions.objects.filter(rangeid = currentrangeid)
        if len(questions) == 0:
            questions = None
        return questions

class RangesView(ListView):
    template_name = 'ranges/viewranges.html'
    context_object_name = 'rangeobject'

    def checkrangeexpiry(self, ranges):
        for x in ranges:
            dateend = Range.objects.filter(rangeid = x[0]).values_list("dateend")[0][0]
            timeend = Range.objects.filter(rangeid = x[0]).values_list("timeend")[0][0]
            if dateend != None:
                datecheck = datetime.date.today() > dateend
                if datecheck:
                    timecheck = datetime.datetime.now().time() > timeend
                    if timecheck:
                        checkifalreadyinactive = Range.objects.filter(rangeid = x[0]).values_list("rangeactive")[0][0]
                        if checkifalreadyinactive == 1:
                            studentobject = RangeStudents.objects.filter(rangeid = x[0], datecompleted=None)
                            studentobject.datecompleted = currenttime
                            studentobject.save()

                            rangeobject = Range.objects.get(rangeid = x[0])
                            rangeobject.rangeactive = 0
                            rangeobject.save()
                            
    def checkrangeactive(self, ranges):
        for x in ranges:
            datestart = Range.objects.filter(rangeid = x[0]).values_list('datestart')[0][0]
            timestart = Range.objects.filter(rangeid = x[0]).values_list('timestart')[0][0]

            if datestart != None:
                datecheck = datetime.date.today() > datestart
                if datecheck:
                    timecheck = datetime.datetime.now().time() > timestart
                    if timecheck:
                        checkifalreadyactive = Range.objects.filter(rangeid = x[0]).values_list("rangeactive")[0][0]
                        if checkifalreadyactive == 0:
                            rangeobject = Range.objects.get(rangeid = x[0])
                            rangeobject.rangeactive = 1
                            rangeobject.save()

    def checkmanualstart(self, ranges):
        for x in ranges:
            manualstart = Range.objects.filter(rangeid = x[0]).values_list('manualactive')[0][0]
            if manualstart is 1:
                rangeobject = Range.objects.get(rangeid = x[0])
                rangeobject.manualdeactive = 0
                rangeobject.rangeactive = 1
                rangeobject.save()

    def checkmanualstop(self, ranges):
        for x in ranges:
            manualstop = Range.objects.filter(rangeid = x[0]).values_list('manualdeactive')[0][0]
            if manualstop is 1:
                rangeobject = Range.objects.get(rangeid = x[0])
                rangeobject.manualactive = 0
                rangeobject.rangeactive = 0
                rangeobject.save()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        inactiveranges = RangeStudents.objects.filter(studentID=user, rangeID__rangeactive=0).order_by('-lastaccess', '-dateJoined', '-pk')

        context['inactive'] = inactiveranges
        return context

    def get_queryset(self):
        DockerKill.get(self, self.request)
        # get the email address of current user
        user = self.request.user
        # get the rangeIDs that are assigned to current user (in a queryset)
        assignedranges = RangeStudents.objects.filter(studentID=user, rangeID__rangeactive=1).order_by('-lastaccess', '-dateJoined', '-pk')
        currentranges = RangeStudents.objects.filter(studentID = user).values_list('rangeID')

        self.checkrangeexpiry(currentranges)
        self.checkrangeactive(currentranges)
        self.checkmanualstart(currentranges)
        self.checkmanualstop(currentranges)

        return assignedranges
