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
from .decorators import *
from django.utils.decorators import method_decorator
from django.contrib import messages

@method_decorator(user_is_student, name='dispatch')
class CheckPorts(View):
    def get(self):
        # get all the entries of the ports currently being used
        database = UnavailablePorts.objects.all().order_by('portnumber').values_list('portnumber')
        # determine the size of the database query
        size = len(database)

        # we need two lists for the two servers that we have
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

        # determine the length of both of the webserver and dockerserver lists
        webserversize = len(webserver)
        dockerserversize = len(dockerserver)
        
        if dockerserversize < 50:
            # check if the docker server is not full (used all 50 ports)
            if int(dockerserver[dockerserversize - 1][0]) == 9099:
                # check if the last entry is the last available port. 
                # if it is not the last available port, it means that there are gaps inbetween the list
                for x in range(0, 48):
                    # use a for loop to loop the number of available ports in one server minused one
                    # this means that because we have 49 ports, we will have to forloop between 0 and 48
                    if int(dockerserver[x + 1][0]) - int(dockerserver[x][0]) != 1:
                        # using the loop, we take the difference of the next port number and the current port number
                        # if the difference is one, it means that there is no gap in between
                        # else if the different is more than one, there is a gap
                        # so we will take the current portnumber and add one to determine the port number to give
                        result = int(dockerserver[x][0]) + 1
                        # return the port number
                        return result
            else:
                # takes the last used port and adds one 
                result = int(dockerserver[dockerserversize - 1][0]) + 1
                # return the port number
                return result
        elif webserversize < 50:
            # we need to check if the web server is currently being used
            if webserversize != 0:
                # because the docker server is full, we will now overflow to the web server
                if int(webserver[webserversize - 1][0]) == 9050:
                    # same logic:
                    # check if the last entry is the last available port. 
                    # if it is not the last available port, it means that there are gaps inbetween the list
                    for x in range(0, 49):
                        # use a for loop to loop the number of available ports in one server minused one
                        # this means that because we have 50 ports, we will have to forloop between 0 and 49
                        if int(webserver[x + 1][0]) - int(webserver[x][0]) != 1:
                            # using the loop, we take the difference of the next port number and the current port number
                            # if the difference is one, it means that there is no gap in between
                            # else if the different is more than one, there is a gap
                            # so we will take the current portnumber and add one to determine the port number to give
                            result = int(webserver[x][0]) + 1
                            # return the port number
                            return result
                else:
                    # takes the last used port and adds one 
                    result = int(webserver[webserversize - 1][0]) + 1
                    # return the port number
                    return result
            else:
                # if the web server is not currently being used, return the first port 9000
                return 9000
        else:
            # the server is completely full. return -1 to show an error.
            return -1


@method_decorator(user_is_student, name='dispatch')
class DockerContainerStart(View):
    def get(self):
                # okay so before we start a new docker container
        data = {}
        execdata = {}
        # calls the checkPorts function from above to get the available port
        port = CheckPorts.get(self)
        # declare an empty string for the server ip
        serverip = ''
        # checks if the port is -1
        if port == -1:
            # if the port is -1, it means that the server is busy, display an error
            return HttpResponse('SERVER BUSY. PLEASE TRY AGAIN LATER.')
        # determine the ip address using the port number        
        elif port >= 9051:
            # if it is 9051 inclusive, it must be the docker server
            serverip = '192.168.100.42'
        elif port <= 9050:
            # else if it is less than 9050 inclusive, it must be the web server
            serverip = '192.168.100.43'
        # in development mode, uncomment the following to override the serverip
        serverip = 'localhost'
        # convert the port to a string for concatenation later
        port = str(port)
        # get the current rangeurl
        rangename = self.kwargs['rangeurl']
        # get the current questionid
        questionnumber = self.kwargs['questionid']
        # gets the string of the imagename to be converted to
        # the format is <rangeurl>.<questionid>
        imagename = str(rangename + '.' + questionnumber)
        # create the payload for the docker engine api
        # the imagename used is to determine the image name to be created
        # the image should be already created in the docker server
        # in development mode, uncomment the following to override the serverip
        imagename = 'siab_server'
        payload = {
            'Image':imagename,
            'HostConfig': {
                "PortBindings": {
                    "4200/tcp": [{
                        "HostIp": "",
                        "HostPort": port
                    }]
                }
            }
        }
        # use the docker engine api to create the container
        url = 'http://' + serverip + ':8051/containers/create'
        print(url)
        # request with the payload
        response = requests.post(url, json=payload)
        if response.status_code == 201:
            test = True
            # get the data from the response
            data = response.json()
            # get the container id
            containerid = data['Id']
            # get the url to start the container
            starturl = 'http://' + serverip + ':8051/containers/%s/start' % containerid
            # request to start the container
            response = requests.post(starturl)
            # create a new entry in the database
            portsdb = UnavailablePorts(portnumber = int(port), studentid = self.request.user, containername = containerid, datetimecreated = timezone.now())
            # save the object to the database
            portsdb.save()
            # get the final url for the iframe
            finalsiaburl = 'dmit2.bulletplus.com:' + port
            # in development mode, uncomment the following to override the serverip
            finalsiaburl = 'localhost:' + port

            # generate a randompassword for the docker container
            randompassword = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            # changing the password using docker exec
            # set the payload
            execcmd = {
                'AttachStdin': True,
                'AttachStdout': True,
                'AttachStderr': True,
                'Tty': True,
                'Cmd': [
                    "/bin/bash",
                    "-c",
                    "echo \'guest:%s\' | chpasswd" % randompassword
                    ]
            }
            # set the url
            execurl = 'http://' + serverip + ':8051/containers/' + containerid + '/exec'
            # request the url with the json payload
            execresponse = requests.post(execurl, json=execcmd)
            # check if it is successful
            if execresponse.status_code == 201:
                # get the json response
                execdata = execresponse.json()
                # get the exec cond id
                execconid = execdata['Id']
                # set the exec payload
                execpayload = {
                    'Detach': False,
                    'Tty': False,
                }
                # set the exec start url
                execstarturl = 'http://' + serverip + ':8051/exec/' + execconid + '/start'
                # send the request
                startexecres = requests.post(execstarturl, json=execpayload)

            # return the password and the url
            return randompassword, finalsiaburl

        elif response.status_code == 400:
            # return error
            print('400')
            return -1, -1
        elif response.status_code == 409:
            # return error
            print('409')
            return -2, -2
        else:
            # return error
            print('something else')
            return -3, -3

@method_decorator(user_is_student, name='dispatch')
class EnterCode(View):
    def get(self, request, *args, **kwargs):
        # get will render the page.
        return render(request, 'ranges/joinrange.html')
    
    def post(self, request, *args, **kwargs):
        # from the form, get the entered rangecode
        rangecode = request.POST.get('rangecode')
        # use a try statement to attempt adding
        try:
            # get the range object identified by the unique rangecode
            selectedrange = Range.objects.get(rangecode = rangecode, isopen=1)
            # get the username of the current user
            user = self.request.user
            # get the email of the current user
            email = user.email

            userobject = User.objects.get(email=email)

            try:
                # use a try statement to get the range student object
                checkifstudentinrange = RangeStudents.objects.get(rangeID = selectedrange, studentID = userobject)
                #if the record exists, it means that the user is already in the range
                messages.error(request,'You already belong in the range')
                # returns the user back to the page to inform them that they are already in the range
                return render(request, 'ranges/joinrange.html')

            except RangeStudents.DoesNotExist:
                # if the user is not in the range already
                # get the current datetime
                datetimenow = datetime.datetime.now()
                # create a rangestudents object
                rangestudentsobj = RangeStudents(rangeID = selectedrange, studentID = userobject, dateJoined = datetimenow)
                # save the object to the database
                rangestudentsobj.save()
                # informs the user that they hae successfully joined the range
                messages.success(request, 'Successfully Joined The Range')
                # returns the user to the page
                return render(request, 'ranges/joinrange.html')

        except Range.DoesNotExist:
            # if the range does not exist, or is the rangecode is not open to be added
            selectedrange = None
            # informs the user that it is invalid
            messages.error(request, 'Invalid Range Code or Range Is Not Open')
            # returns the user to the page
            return render(request, 'ranges/joinrange.html')

@method_decorator(user_is_student, name='dispatch')
class DockerKill(View):
    # function to delete old ports and dockers 
    def get(self, request):
        # checks if the user has previously opened a docker container and a port
        previousport = UnavailablePorts.objects.filter(studentid = self.request.user).values_list('portnumber')
        if previousport:
            # if there is, get the portnumber
            port = previousport[0][0]
            # get the containername of the docker used previously
            containername = UnavailablePorts.objects.filter(studentid = self.request.user).values_list('containername')[0][0]
            # checks the port to determine the server to talk to
            if int(port) >= 9051:
                # if the port is more than 9051 inclusive, the server must be the docker service
                serverip = '192.168.100.42'
            elif int(port) <= 9050:
                # else if the port is less than 9051 inclusive, the server must be ther web server
                serverip = '192.168.100.43'
            # in development mode, uncomment the following to override the serverip
            serverip = 'localhost'
            # url for the web server to talk to
            endpoint = 'http://' + serverip + ':8051/containers/{conid}?force=True'
            url = endpoint.format(conid=containername)
            # request to delete the container
            response = requests.delete(url)
            
            # after it is deleted, we have to delete the entry from the database
            # get the object
            deleteportsdb = UnavailablePorts.objects.filter(studentid = self.request.user)
            # delete the entry
            deleteportsdb.delete()
            
        # we also have to timeout the ports in case the user did not close the docker container properly
        # first, we get all the used ports from the database
        allentriesinportsdb = UnavailablePorts.objects.all()
        # check if there are no entries
        if len(allentriesinportsdb) != 0:
            # if there are entries, use a forloop to traverse the queryset
            for entry in allentriesinportsdb:
                # check the time difference between now and the date and time the docker was created
                timediff = timezone.now() - entry.datetimecreated 
                # checks if the time difference is more than 3 hours
                if timediff > datetime.timedelta(hours = 3):
                    # if the container has been opened for more than 3 hours, get the container name
                    containername = entry.containername
                    # get the port number as well
                    port = entry.portnumber
                    # use the port number to determine the server that it is opened in
                    if int(port) >= 9051:
                        # if it is more than 9051 inclusive, it must be the docker server
                        serverip = '192.168.100.42'
                    elif int(port) <= 9050:
                        # else if is is less than 9051 inclusive, it must be the web srver
                        serverip = '192.168.100.43'
                    # in development mode, uncomment the following to override the serverip
                    serverip = 'localhost'
                    # get the url for the request
                    endpoint = 'http://' + serverip + ':8051/containers/{conid}?force=True'
                    url = endpoint.format(conid=containername)
                    # send the request to delete the container
                    response = requests.delete(url)
                    
                    # like before, we need to delete the entry in the database
                    deleteportsdb = UnavailablePorts.objects.filter(studentid = self.request.user)
                    deleteportsdb.delete()

@method_decorator(user_is_student, name='dispatch')
class AttemptQuestionView(ListView, ModelFormMixin):
    template_name = 'ranges/attemptquestion.html'
    context_object_name = 'question'
    model = StudentQuestions
    form_class = AnswerForm



    def checkattemptlimit(self):
        # this function is to determine if the user has reached his attempt limit
        # declare the attempted as false first
        attempted = False
        # get the current user
        user = self.request.user
        # get the question object of the current object
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        # get the rangeurl of the currenet range
        rangeurl = self.kwargs['rangeurl']
        # get the rangeid using the range url
        rangeid = Range.objects.filter(rangeurl=rangeurl).values_list('rangeid')[0][0]
        # check the number of attempts that the user has attempted this question before
        numberofattempts = len(StudentQuestions.objects.filter(studentid = user, rangeid = rangeid, questionid = questioninstance))
        # get the max number of attempts for this question
        maxattempts = Range.objects.filter(rangeid = rangeid).values_list('attempts')[0][0]
        # check if the user has reached his attempt limit 
        if maxattempts != 0 and numberofattempts == maxattempts:
            # if it is, return true
            attempted = True
        # otherwise, return false
        return attempted

    def latestanswer(self):
        # this function is to get the latest answer that the user has attempted
        # first, get the username
        user = self.request.user
        # then, get the question instnace
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        # get the rangeurl of the current range
        rangeurl = self.kwargs['rangeurl']
        # get the range instance object of the current range
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        # get the queryset of the studentquestions for the students attempts
        result = StudentQuestions.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance).values_list('answergiven')
        # check if the return is not 0
        if len(result) != 0:
            # get the latest given answer
            result = result[len(result) - 1][0]
        else:
            # set result as None
            result = None
        # return the result
        return result

    def get(self, request, *args, **kwargs):
        # this get function is to display the get method form
        # declare self.object as none
        self.object = None
        # get the form using the form class stated at the start of this view
        self.form = self.get_form(self.form_class)
        # return the list view
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # this post function is to display the post method form
        # declare self.object as none
        self.object = None
        # get the form using the form class stated at the start of this view
        self.form = self.get_form(self.form_class)

        # check if the form is valid
        if self.form.is_valid():
            # if the form is valid
            # get the user
            user = self.request.user
            # get the answer they gave
            answergiven = self.form.cleaned_data['answergiven']
            # get the question object of current question
            questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
            # get the current range url
            rangeurl = self.kwargs['rangeurl']
            # get the range instance object using the rangeurl
            rangeinstance = Range.objects.get(rangeurl = rangeurl)
            # get the questionid
            questionid = Questions.objects.filter(questionid = self.kwargs['questionid']).values_list('questionid')[0][0]
            # call the checkanswer function from above
            check = self.form.checkAnswer(user, answergiven, questioninstance, rangeinstance, questionid)
            # return the post form
            return ListView.get(self, request, *args, **kwargs)
        
        else:
            return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        # get queryset is to pull from the database to get info for the listview
        # call the docker kill class
        DockerKill.get(self, self.request)
        # check if the question exists, otherwise raise 404
        self.questionid = get_object_or_404(Questions, questionid=self.kwargs['questionid'])
        # check if the range exists, otherwise raise 404
        self.rangeid = get_object_or_404(Range, rangeurl=self.kwargs['rangeurl'], rangeactive=1, isdisabled=0)
        # get the questions
        question = Questions.objects.filter(questionid = self.kwargs['questionid'])[0]
        return question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the questionid
        questionid = self.kwargs['questionid']
        # get the rangeid using the rangeurl
        rangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        # check if the question uses docker
        usedocker = Questions.objects.filter(questionid = questionid).values_list('usedocker')[0][0]
        if usedocker is True:
            # if it is true, call the dockercontainerstart function
            password, siab = DockerContainerStart.get(self)
            # set siab and password as context
            context['siab'] = siab
            context['password'] = password
        else:
            # otherwise, set both to false
            context['siab'] = False
            context['password'] = False

        # call the checkattemptlimit function to be set as context
        context['hitmaxattempts'] = self.checkattemptlimit()
        # call the latestanswer function to be set as contexxt
        context['latestanswer'] = self.latestanswer()

        # gotta check if it's mcq, and if it is, get options from database
        # first i gotta get the questionobject
        questiontype = Questions.objects.filter(questionid = questionid).values_list('questiontype')[0][0]
        
        # if it is mcq
        if questiontype == 'MCQ':
            # get the mcqoptions from the database
            options = MCQOptions.objects.filter(questionid = questionid)
            # set the options as context
            context['mcqoptions'] = options

        # get the question points for that question to be set as context
        context['questionpoints'] = Questions.objects.filter(rangeid = self.rangeid, questionid = questionid).values_list('points')[0][0]
        
        # check if the student activated the hint for this question before
        hintactivated = StudentHints.objects.filter(rangeid = self.rangeid, questionid = questionid, studentid = self.request.user).values_list('hintactivated')
        # check if the queryset has data
        if len(hintactivated) != 0:
            # if it does, get the hint
            hint = hintactivated[0][0]
        else:
            # otherwise set to none
            hint = None
        #set hint as the context
        context['hint'] = hint

        # check the database if the student has answer the question correctly before
        correctcheck = StudentQuestions.objects.filter(studentid = self.request.user, rangeid = rangeid, questionid = questionid, answercorrect = 1)
        # if the queryset has that entry
        if len(correctcheck) == 1:
            # set context as tTrue
            context['correct'] = True
        else:
            # otherwise set false
            context['correct'] = False

        # get the question topic of the question
        questiontopic = Questions.objects.filter(rangeid = self.rangeid, questionid = questionid).values_list('topicid')[0][0]
        # get the topic name from the database
        topicname = QuestionTopic.objects.filter(topicid = questiontopic).values_list('topicname')[0][0]
        # set the context as topicname
        context['topic'] = topicname

        # get the number of attempts for that question
        attempted = StudentQuestions.objects.filter(questionid = questionid, studentid = self.request.user, rangeid = rangeid).count()
        # check if it is attempted
        if attempted != 0:
            # get the latest points awarded
            latestpoints = StudentQuestions.objects.get(studentid = self.request.user, rangeid = rangeid, questionid = questionid, attempts = attempted)
            # set the latestpoints context
            context['latestpoints'] = latestpoints
            # check if the open ended question is marked
            if questiontype == 'OE':
                # check if it is repeated
                repeatedcheck = StudentQuestions.objects.filter(questionid = questionid, studentid = self.request.user, rangeid = rangeid).count()
                # check if it is marked
                checkoemarked = StudentQuestions.objects.get(studentid = self.request.user, rangeid = rangeid, questionid = questionid, attempts = repeatedcheck)
                marked = checkoemarked.ismarked
                # set the mark as context
                context['ismarked'] = marked

        # return context
        return context


@method_decorator(user_is_student, name='dispatch')
class AttemptMCQQuestionView(ListView, ModelFormMixin):
    template_name = 'ranges/attemptquestion.html'
    context_object_name = 'question'
    model = StudentQuestions
    form_class = AnswerMCQForm

    def checkattemptlimit(self):
        # this function is to determine if the user has reached his attempt limit
        # declare the attempted as false first
        attempted = False
        # get the current user
        user = self.request.user
        # get the question object of the current object
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        # get the rangeurl of the currenet range
        rangeurl = self.kwargs['rangeurl']
        # get the rangeid using the range url
        rangeid = Range.objects.filter(rangeurl=rangeurl).values_list('rangeid')[0][0]
        # check the number of attempts that the user has attempted this question before
        numberofattempts = len(StudentQuestions.objects.filter(studentid = user, rangeid = rangeid, questionid = questioninstance))
        # get the max number of attempts for this question
        maxattempts = Range.objects.filter(rangeid = rangeid).values_list('attempts')[0][0]
        # check if the user has reached his attempt limit 
        if maxattempts != 0 and numberofattempts == maxattempts:
            # if it is, return true
            attempted = True
        # otherwise, return false
        return attempted

    def latestanswer(self):
        # this function is to get the latest answer that the user has attempted
        # first, get the username
        user = self.request.user
        # then, get the question instnace
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        # get the rangeurl of the current range
        rangeurl = self.kwargs['rangeurl']
        # get the range instance object of the current range
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        # get the queryset of the studentquestions for the students attempts
        result = StudentQuestions.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance).values_list('answergiven')
        # check if the return is not 0
        if len(result) != 0:
            # get the latest given answer
            result = result[len(result) - 1][0]
        else:
            # set result as None
            result = None
        # return the result
        return result

    def get_form_kwargs(self):
        # get the keyword arguments for the form
        kwargs = super(AttemptMCQQuestionView, self).get_form_kwargs()
        # set list one to four
        list = ['one', 'two', 'three', 'four']
        newlist = []

        for x in list:
            # get the mcq options from the database
            options = MCQOptions.objects.filter(questionid = self.kwargs['questionid']).values_list('option'+str(x))[0][0]
            # set the choice syntax
            choice = (options, options)
            # append to the list
            newlist.append(choice)
        # set the keyword arguments as newlist
        kwargs['choices'] = newlist
        # return kwargs
        return kwargs
    
    def get(self, request, *args, **kwargs):
        # this get function is to display the get method form
        # declare self.object as none
        self.object = None
        # get the form using the form class stated at the start of this view
        self.form = self.get_form(self.form_class)
        # return the list view
        return ListView.get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # this post function is to display the post method form
        # declare self.object as none
        self.object = None
        # get the form using the form class stated at the start of this view
        self.form = self.get_form(self.form_class)

        # check if the form is valid
        if self.form.is_valid():
            # if the form is valid
            # get the user
            user = self.request.user
            # get the answer they gave
            answergiven = self.form.cleaned_data['answergiven']
            # get the question object of current question
            questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
            # get the current range url
            rangeurl = self.kwargs['rangeurl']
            # get the range instance object using the rangeurl
            rangeinstance = Range.objects.get(rangeurl = rangeurl)
            # get the questionid
            questionid = Questions.objects.filter(questionid = self.kwargs['questionid']).values_list('questionid')[0][0]
            # call the checkanswer function from above
            check = self.form.checkAnswer(user, answergiven, questioninstance, rangeinstance, questionid)
            # return the post form
            return ListView.get(self, request, *args, **kwargs)

    def get_queryset(self):
        # get queryset is to pull from the database to get info for the listview
        # call the docker kill class
        DockerKill.get(self, self.request)
        # check if the question exists, otherwise raise 404
        self.questionid = get_object_or_404(Questions, questionid=self.kwargs['questionid'])
        # check if the range exists, otherwise raise 404
        self.rangeid = get_object_or_404(Range, rangeurl=self.kwargs['rangeurl'], rangeactive=1, isdisabled=0)
        # get the questions
        question = Questions.objects.filter(questionid = self.kwargs['questionid'])[0]
        return question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the questionid
        questionid = self.kwargs['questionid']
        # get the rangeid using the rangeurl
        rangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        # check if the question uses docker
        usedocker = Questions.objects.filter(questionid = questionid).values_list('usedocker')[0][0]
        if usedocker is True:
            # if it is true, call the dockercontainerstart function
            password, siab = DockerContainerStart.get(self)
            # set siab and password as context
            context['siab'] = siab
            context['password'] = password
        else:
            # otherwise, set both to false
            context['siab'] = False
            context['password'] = False

        # call the checkattemptlimit function to be set as context
        context['hitmaxattempts'] = self.checkattemptlimit()
        # call the latestanswer function to be set as contexxt
        context['latestanswer'] = self.latestanswer()

        # gotta check if it's mcq, and if it is, get options from database
        # first i gotta get the questionobject
        questiontype = Questions.objects.filter(questionid = questionid).values_list('questiontype')[0][0]
        
        # if it is mcq
        if questiontype == 'MCQ':
            # get the mcqoptions from the database
            options = MCQOptions.objects.filter(questionid = questionid)
            # set the options as context
            context['mcqoptions'] = options

        # get the question points for that question to be set as context
        context['questionpoints'] = Questions.objects.filter(rangeid = self.rangeid, questionid = questionid).values_list('points')[0][0]
        
        # check if the student activated the hint for this question before
        hintactivated = StudentHints.objects.filter(rangeid = self.rangeid, questionid = questionid, studentid = self.request.user).values_list('hintactivated')
        # check if the queryset has data
        if len(hintactivated) != 0:
            # if it does, get the hint
            hint = hintactivated[0][0]
        else:
            # otherwise set to none
            hint = None
        #set hint as the context
        context['hint'] = hint

        # check the database if the student has answer the question correctly before
        correctcheck = StudentQuestions.objects.filter(studentid = self.request.user, rangeid = rangeid, questionid = questionid, answercorrect = 1)
        # if the queryset has that entry
        if len(correctcheck) == 1:
            # set context as tTrue
            context['correct'] = True
        else:
            # otherwise set false
            context['correct'] = False

        # get the question topic of the question
        questiontopic = Questions.objects.filter(rangeid = self.rangeid, questionid = questionid).values_list('topicid')[0][0]
        # get the topic name from the database
        topicname = QuestionTopic.objects.filter(topicid = questiontopic).values_list('topicname')[0][0]
        # set the context as topicname
        context['topic'] = topicname

        # return context
        return context

@method_decorator(user_is_student, name='dispatch')
class ActivateHint(View):
    # this class is to activate the hint as a student
    def get(self, request, questionid, rangeurl):
        # get the current user
        user = self.request.user
        # create a new hint object
        hintobj = StudentHints()
        # set the student id of the object
        hintobj.studentid = user
        # get the range instance object of current range
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        # set the rangeinstance as the rangeid of the object
        hintobj.rangeid = rangeinstance
        # get the question instance object
        questioninstance = Questions.objects.get(questionid = questionid)
        # set the questioninstance as questionid of the object
        hintobj.questionid = questioninstance
        # set the hintactivated as True
        hintobj.hintactivated = True
        # save the object
        hintobj.save()
        # redirect the user
        return redirect('./')


@method_decorator(user_is_student, name='dispatch')
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
        rangestudentobj.lastaccess = timezone.now()
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
        questionidsinrange = Questions.objects.filter(rangeid = currentrangeid, isarchived=False).values_list("questionid")

        # create empty list for topics
        topiclist = []

        if len(questionidsinrange) != 0:
            # get the queryset of the topicid of the first question
            topicidqueryset = Questions.objects.filter(questionid = (questionidsinrange[0][0]))

            # loop so that i can get all the topic ids of the questions in the range
            for x in range(0, len(questionidsinrange)):
                currenttopicidqueryset = Questions.objects.filter(questionid=(questionidsinrange[x][0]))
                currenttopicidforlistinteger = Questions.objects.filter(questionid=(questionidsinrange[x][0])).values_list("topicid")[0][0]


                # check if the topic id is repeated, if its not, add to the list and append to queryset to get the QUESTIONS QUERYSET
                if currenttopicidforlistinteger not in topiclist:
                    topiclist.append(currenttopicidforlistinteger)  
                    topicidqueryset = topicidqueryset | currenttopicidqueryset

                    # but i need the questiontopic queryset

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

        else:
            # probably won't be none but still
            questiontopicqueryset = None

        # return topics as a context YEBOI YAY ME
        context['topics'] = questiontopicqueryset

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
        adminemail = Range.objects.filter(rangeurl= rangeurl).values_list('createdby')[0][0]
        adminusername = User.objects.filter(email=adminemail).values_list('username')[0][0]
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
        self.rangeid = get_object_or_404(Range, rangeurl=self.kwargs['rangeurl'], rangeactive=1, isdisabled=0)
        DockerKill.get(self, self.request)
        currentrangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        questions = Questions.objects.filter(rangeid = currentrangeid)
        if len(questions) == 0:
            questions = None
        return questions

# HouseKeeping View
# This housekeeping is to 
# 1. activate ranges when the start date and time has passed
# 2. deactivate ranges when end date and time has passed
# 3. check if the teacher override the activation
@method_decorator(user_is_student, name='dispatch')
class Housekeeping(View):
    # get the currentranges from the previous view that called this view
    def get(self, currentranges):
        # forloop each range 
        for x in currentranges:
            # get the date end
            dateend = Range.objects.filter(rangeid = x[0]).values_list("dateend")[0][0]
            # get the time end
            timeend = Range.objects.filter(rangeid = x[0]).values_list("timeend")[0][0]
            # get the date start
            datestart = Range.objects.filter(rangeid = x[0]).values_list('datestart')[0][0]
            # get the time start
            timestart = Range.objects.filter(rangeid = x[0]).values_list('timestart')[0][0]
            # get the range object
            rangeobject = Range.objects.get(rangeid = x[0])

            # check if the datestart is not None
            if datestart != None:
                # check if the date is between the start and end
                datecheck = datetime.date.today() >= datestart and datetime.date.today() <= dateend
                if datecheck is True:
                    # activate range first
                    rangeobject.rangeactive = True
                    # check if it is the datestart day
                    startdatecheck = datetime.date.today() == datestart
                    if startdatecheck is True:
                        # check if the timestart has passed
                        starttimecheck = datetime.datetime.now().time() >= timestart
                        if starttimecheck is True:
                            rangeobject.rangeactive = True

                    # check if it is the dateend day
                    enddatecheck = datetime.date.today() == dateend
                    if enddatecheck is True:
                        # check if the timeend has passed
                        endtimecheck = datetime.datetime.now().time() >= timeend
                        if endtimecheck is True:
                            rangeobject.rangeactive = False

                    rangeobject.save()
                else:
                    rangeobject.rangeactive = False
                    rangeobject.save()
                
            # check if the teacher manually activated the range
            manualstart = Range.objects.filter(rangeid = x[0]).values_list('manualactive')[0][0]
            if manualstart is True:
                # if it is true, set the manualdeactive as 0
                rangeobject.manualdeactive = 0
                # set the rangeactive as 1
                rangeobject.rangeactive = 1
                # save the object
                rangeobject.save()

            # check if the teacher manually stopped the range
            manualstop = Range.objects.filter(rangeid = x[0]).values_list('manualdeactive')[0][0]
            if manualstop is True:
                # if it is true, set the manual active as 0
                rangeobject.manualactive = 0
                # set the rangeactive as 0
                rangeobject.rangeactive = 0
                #save the rangeobject
                rangeobject.save()

# RangesView
# get all the ranges and list out for students to scroll through
@method_decorator(user_is_student, name='dispatch')
class RangesView(ListView):
    template_name = 'ranges/viewranges.html'
    context_object_name = 'rangeobject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        inactiveranges = RangeStudents.objects.filter(studentID=user, rangeID__rangeactive=0, rangeID__isdisabled=0).order_by('-lastaccess', '-dateJoined', '-pk')
        context['inactive'] = inactiveranges
        return context

    def get_queryset(self):
        # call the dockerkill view
        DockerKill.get(self, self.request)
        # get the email address of current user
        user = self.request.user
        # get the rangeIDs that are assigned to current user (in a queryset)
        assignedranges = RangeStudents.objects.filter(studentID=user, rangeID__rangeactive=1, rangeID__isdisabled=0).order_by('-lastaccess', '-dateJoined', '-pk')
        # get the currentranges
        currentranges = RangeStudents.objects.filter(studentID = user).values_list('rangeID')
        # call the housekeeping view
        Housekeeping.get(self, currentranges)
        # return the queryset
        return assignedranges
