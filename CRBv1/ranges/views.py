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
                elif database[x][0] >=9052:
                    dockerserver.append(database[x])
        
        else:
            #return first available port for docker server
            return 9052 

        #print('FIRST --->')
        #print(dockerserver, webserver)

        webserversize = len(webserver)
        dockerserversize = len(dockerserver)
        #print('SECOND --->')
        #print(webserversize, dockerserversize)
        
        if dockerserversize < 50:
            if int(dockerserver[dockerserversize - 1][0]) == 9100:
                for x in range(0, 48):
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
        previousport = UnavailablePorts.objects.filter(studentid = self.request.user).values_list('containername')
        if previousport:
            containername = previousport[0][0]
            endpoint = 'http://192.168.100.42:8051/containers/{conid}?force=True'
            url = endpoint.format(conid=containername)
            response = requests.delete(url)
            endpoint = 'http://192.168.100.43:8051/containers/{conid}?force=True'
            url = endpoint.format(conid=containername)
            response = requests.delete(url)
            # need to delete from db
            deleteportsdb = UnavailablePorts.objects.filter(studentid = self.request.user)
            deleteportsdb.delete()


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
        image = 'siab_server'
        payload = {
            'Image':image,
            'HostConfig': {
                "PortBindings": {
                "4200/tcp": [{
                    "HostIp": "",
                    "HostPort": port
                    }
                ]}
            }
        }
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
            finalsiaburl = serverip+':'+port
            #print(finalsiaburl)
            return finalsiaburl

        elif response.status_code == 400:
            return redirect('/error')
        elif response.status_code == 409:
            return redirect('/error')
        else:
            return redirect('/error')


    def checkattempted(self):
        attempted = False
        user = self.request.user
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        rangeurl = self.kwargs['rangeurl']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        if StudentQuestions.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance):
            #print("attempted")
            attempted = True
        # else:
            #print("not attempted")
        
        return attempted

    def result(self):
        user = self.request.user
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        rangeurl = self.kwargs['rangeurl']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        result = StudentQuestions.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance)
        
        if result is not None:
            return result
        else:
            return None

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
        self.questionid = get_object_or_404(Questions, questionid=self.kwargs['questionid'])
        self.rangeid = get_object_or_404(Range, rangeurl=self.kwargs['rangeurl'], rangeactive=1)
        #print("1 --> " + str(self.kwargs['questionid']))
        question = Questions.objects.filter(questionid = self.kwargs['questionid'])
        #print("2 --> "+ str(question))
        return question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        siab = self.dockerContainerStart()
        context['siab'] = siab
        context['attempted'] = self.checkattempted()
        context['result'] = self.result()
        #print('ATTEMPTED ----->>>>> ' + str(context['attempted']))
        #print('RESULT ----->>>>> ' + str(context['result']))

        #gotta check if it's mcq, and if it is, get options from database
        # first i gotta get the questionobject
        questiontype = Questions.objects.filter(questionid = self.kwargs['questionid']).values_list('questiontype')[0][0]
        #print("HI WADDUP --->" + str(questiontype))

        if questiontype == 'MCQ':
            #print("YAY")
            options = MCQOptions.objects.filter(questionid = self.kwargs['questionid'])
            #print("HERE ARE THE OPTIONS" + str(options))
            context['mcqoptions'] = options

        return context


class AttemptMCQQuestionView(ListView, ModelFormMixin):
    template_name = 'ranges/attemptquestion.html'
    context_object_name = 'question'
    model = StudentQuestions
    form_class = AnswerMCQForm

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

    def checkattempted(self):
        attempted = False
        user = self.request.user
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        rangeurl = self.kwargs['rangeurl']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        if StudentQuestions.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance):
            #print("attempted")
            attempted = True
        # else:
            #print("not attempted")
        
        return attempted

    def result(self):
        user = self.request.user
        questioninstance = Questions.objects.get(questionid = self.kwargs['questionid'])
        rangeurl = self.kwargs['rangeurl']
        rangeinstance = Range.objects.get(rangeurl = rangeurl)
        result = StudentQuestions.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance)
        
        if result is not None:
            return result
        else:
            return None

    def get_queryset(self):
        self.questionid = get_object_or_404(Questions, questionid=self.kwargs['questionid'])
        self.rangeid = get_object_or_404(Range, rangeurl=self.kwargs['rangeurl'], rangeactive=1)
        #print("1 --> " + str(self.kwargs['questionid']))
        question = Questions.objects.filter(questionid = self.kwargs['questionid'])
        #print("2 --> "+ str(question))
        return question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempted'] = self.checkattempted()
        context['result'] = self.result()
        #print('ATTEMPTED ----->>>>> ' + str(context['attempted']))
        #print('RESULT ----->>>>> ' + str(context['result']))

        #gotta check if it's mcq, and if it is, get options from database
        # first i gotta get the questionobject
        questiontype = Questions.objects.filter(questionid = self.kwargs['questionid']).values_list('questiontype')[0][0]
        #print("HI WADDUP --->" + str(questiontype))

        if questiontype == 'MCQ':
            #print("YAY")
            options = MCQOptions.objects.filter(questionid = self.kwargs['questionid'])
            #print("HERE ARE THE OPTIONS" + str(options))
            context['mcqoptions'] = options


        return context

class QuestionsView(ListView):
    template_name = 'ranges/questions.html'
    context_object_name = 'questionobject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # i need to find all the topics in a single range.
        # how do i do it?
        # first i need to get the range id.
        rangeurl = self.kwargs['rangeurl'] # get the rangename from the kwargs (url)
        
        # get the current range id using rangename we got above
        currentrangeid = Range.objects.filter(rangeurl = rangeurl).values_list('rangeid')[0][0]
        #print("rangeid ----->>>" + str(currentrangeid))

        # now that i got the range id
        # what do i need?
        # i need to get the categories that appear in the range
        # how do i get that?
        # i need to get the questionids in the range (rangequestions)
        # then i need to get the categoryids of the questions (question)
        # do i need the categoryname?

        # get the questionids of the questions in the range in a queryset
        questionidsinrange = RangeQuestions.objects.filter(rangeid = currentrangeid).values_list("questionid")
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
        # get the queryset of attempted questions
        context['attemptedquestions'] = StudentQuestions.objects.filter(studentid = user, rangeid = currentrangeid)

        # should i get the queryset of questions that are not attempted? probably easier for the template. fricking template so damn dumb

        # create empty list for attempted questions
        attemptedlist = []
        unattemptedlist = []
        #print(attemptedlist)

        # i'll just give the attempted questions an easier name for variable
        attemptedquestionsqueryset = StudentQuestions.objects.filter(studentid = user, rangeid = currentrangeid).values_list("questionid")
        #print(attemptedquestionsqueryset)

        if len(attemptedquestionsqueryset) != 0:
            # probably won't be 0 lah but still (update: fml this screwed me over)
            # wait i test print first
            for x in range(0, len(attemptedquestionsqueryset)):
                # get all the questionids that have already been attempted
                attemptedlist.append(attemptedquestionsqueryset[x][0])
            #print("TESTPRINT ------>>>>>> " + str(attemptedlist))

            # okay now that i got all the questionids that have already been attempted
            # how do i get the queryset of all the questionids that have not been attempted?
            # can i get all the questionids in the range and remove those that have already been attempted?
            # print("QUESTIONIDS --->>>>> " + str(questionidsinrange))
            # nice

        # get unattempted list???
        for x in range(0, len(questionidsinrange)):
            if questionidsinrange[x][0] not in attemptedlist:
                unattemptedlist.append(questionidsinrange[x][0])
                #print(unattemptedlist)

        #print("ORHOR DIDN'T DO ----->>>>>" + str(unattemptedlist[0]))

        if len(unattemptedlist) != 0:
            # get the first entry
            #print("rangeinstance" + str(currentrangeid))
            unattemptedquestionsqueryset = RangeQuestions.objects.filter(questionid = unattemptedlist[0], rangeid = currentrangeid)
            #print("HELP" + str(unattemptedquestionsqueryset))
            for q in unattemptedlist:
                if q != unattemptedlist[0]:
                    uqs = RangeQuestions.objects.filter(questionid = q, rangeid = currentrangeid)
                    unattemptedquestionsqueryset = unattemptedquestionsqueryset | uqs
                
                #print("fml " + str(unattemptedquestionsqueryset))

            #print(unattemptedquestionsqueryset)
            context['unattemptedquestions'] = unattemptedquestionsqueryset
        else:
            context['unattemptedquestions'] = None

        context['rangename'] = Range.objects.filter(rangeurl = rangeurl).values_list('rangename')[0][0]
        return context

    def get_queryset(self):
        self.rangeurl = get_object_or_404(Range, rangeurl=self.kwargs['rangeurl'], rangeactive=1)

        previousport = UnavailablePorts.objects.filter(studentid = self.request.user).values_list('containername')
        if previousport:
            containername = previousport[0][0]
            endpoint = 'http://192.168.100.42:8051/containers/{conid}?force=True'
            url = endpoint.format(conid=containername)
            response = requests.delete(url)
            endpoint = 'http://192.168.100.43:8051/containers/{conid}?force=True'
            url = endpoint.format(conid=containername)
            response = requests.delete(url)
            # need to delete from db
            deleteportsdb = UnavailablePorts.objects.filter(studentid = self.request.user)
            deleteportsdb.delete()

        # timeout for ports
        allentriesinportsdb = UnavailablePorts.objects.all()
        if allentriesinportsdb != 0:
            for entry in allentriesinportsdb:
                timediff = timezone.now() - entry.datetimecreated 
                print(timediff)
                if timediff > datetime.timedelta(hours = 3):
                    print("more than 2 minutes")
                    containername = entry.containername
                    endpoint = 'http://192.168.100.42:8051/containers/{conid}?force=True'
                    url = endpoint.format(conid=containername)
                    response = requests.delete(url)

                    endpoint = 'http://192.168.100.43:8051/containers/{conid}?force=True'
                    url = endpoint.format(conid=containername)
                    response = requests.delete(url)
                    # need to delete from db
                    deleteportsdb = UnavailablePorts.objects.filter(studentid = self.request.user)
                    deleteportsdb.delete()
        #print('RANGE -->' + str(self.kwargs['rangeurl']))

        # get the range id
        currentrangeid = Range.objects.filter(rangeurl = self.kwargs['rangeurl']).values_list('rangeid')[0][0]
        #print(currentrangeid)

        # use range id to get the questionids in the current range
        questions = RangeQuestions.objects.filter(rangeid = currentrangeid).values_list('questionid')
        #print("1 --> ORDER" + str(questions))
        if len(questions) != 0:
            # get the first object of assigned range (because need to declare var before our little concat trick later)
            result = Questions.objects.filter(questionid=(questions[0][0]))
            #print('2 --> ' + str(result))
            for x in range(1, len(questions)):
                #this for loop will concat all the assigned ranges together for our template to call
                currentquestion= Questions.objects.filter(questionid=(questions[x][0]))
                result = result | currentquestion # if i didn't get the first object just now python will scold me
                # print('3 --> ' + str(result))
        else:
            # if there are no questions return None if not rip cause it shouldn't be none
            result = None
        #print("FMLLLLLLLL " +str(result))
        #final = result.order_by('rangequestions__questionorder')[1:]
        return result

class RangesView(ListView):
    template_name = 'ranges/viewranges.html'
    context_object_name = 'rangeobject'

    def checkrangeexpiry(self, ranges):
        #print(ranges)

        for x in ranges:
            dateend = Range.objects.filter(rangeid = x[0]).values_list("dateend")[0][0]
            timeend = Range.objects.filter(rangeid = x[0]).values_list("timeend")[0][0]
            if dateend != None:
                #print('test')
                #print(datetime.date.today())
                #print(dateend)
                datecheck = datetime.date.today() > dateend
                if datecheck:
                    timecheck = datetime.time.now() > timeend
                    if timecheck:
                        checkifalreadyinactive = Range.objects.filter(rangeid = x[0]).values_list("rangeactive")[0][0]
                        if checkifalreadyinactive == 1:
                            rangeobject = Range.objects.get(rangeid = x[0])
                            rangeobject.rangeactive = 0
                            rangeobject.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['userrange'] = RangeStudents.objects.filter(studentID = user)
        #print('HIHIHIHI -->' + str(context['userrange']))

        currentranges = RangeStudents.objects.filter(studentID = user).values_list('rangeID')
        #print('1 --> ' + str(currentranges))
        # check if there are no assigned ranges
        if len(currentranges) != 0:
            # get the first object of assigned range (because need to declare var before our little concat trick later)
            inactiveranges = Range.objects.filter(rangeid=(currentranges[0][0]), rangeactive = 0)
            #print('2 --> ' + str(result))
            for x in range(1, len(currentranges)):
                #this for loop will concat all the assigned ranges together for our template to call
                inactiveassignedranges= Range.objects.filter(rangeid=(currentranges[x][0]), rangeactive = 0)
                inactiveranges = inactiveranges | inactiveassignedranges # if i didn't get the first object just now python will scold me
            #print('3 -->' + str(inactiveranges))
        
        else:
            inactiveranges = None

        context['inactive'] = inactiveranges
        return context

    def get_queryset(self):
        # delete old port if existing
        previousport = UnavailablePorts.objects.filter(studentid = self.request.user).values_list('containername')
        if previousport:
            containername = previousport[0][0]
            endpoint = 'http://192.168.100.42:8051/containers/{conid}?force=True'
            url = endpoint.format(conid=containername)
            response = requests.delete(url)
            endpoint = 'http://192.168.100.42:8051/containers/{conid}?force=True'
            url = endpoint.format(conid=containername)
            response = requests.delete(url)
            # need to delete from db
            deleteportsdb = UnavailablePorts.objects.filter(studentid = self.request.user)
            deleteportsdb.delete()

        # timeout for ports
        allentriesinportsdb = UnavailablePorts.objects.all()
        if allentriesinportsdb != 0:
            for entry in allentriesinportsdb:
                timediff = timezone.now() - entry.datetimecreated 
                print(timediff)
                if timediff > datetime.timedelta(hours = 3):
                    print("more than 2 minutes")
                    containername = entry.containername
                    endpoint = 'http://192.168.100.42:8051/containers/{conid}?force=True'
                    url = endpoint.format(conid=containername)
                    response = requests.delete(url)
                    endpoint = 'http://192.168.100.43:8051/containers/{conid}?force=True'
                    url = endpoint.format(conid=containername)
                    response = requests.delete(url)
                    # need to delete from db
                    deleteportsdb = UnavailablePorts.objects.filter(studentid = self.request.user)
                    deleteportsdb.delete()

        

        # get the email address of current user
        user = self.request.user
        # get the rangeIDs that are assigned to current user (in a queryset)
        currentranges = RangeStudents.objects.filter(studentID = user).values_list('rangeID')

        self.checkrangeexpiry(currentranges)
        #print('1 --> ' + str(currentranges))
        # check if there are no assigned ranges
        if len(currentranges) != 0:
            # get the first object of assigned range (because need to declare var before our little concat trick later)
            activeranges = Range.objects.filter(rangeid=(currentranges[0][0]), rangeactive = 1)
            #print('2 --> ' + str(result))
            for x in range(1, len(currentranges)):
                #this for loop will concat all the assigned ranges together for our template to call
                activeassignedranges= Range.objects.filter(rangeid=(currentranges[x][0]), rangeactive = 1)
                activeranges = activeranges | activeassignedranges # if i didn't get the first object just now python will scold me
                #print('3 -->' + str(result))
        else:
            # if there are no assigned ranges return None if not rip
            return None

        # return the whole damn thing
        #print(result[0])
        return activeranges

class ErrorMessage(generic.TemplateView):
    template_name = 'ranges/error.html'
