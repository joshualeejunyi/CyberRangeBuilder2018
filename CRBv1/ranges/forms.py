from django import forms
from .models import *
from django.utils import timezone

class AnswerForm(forms.ModelForm):
    answergiven = forms.CharField(label='Answer', max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))

    def checkAnswer(self, user, answergiven, questioninstance, rangeinstance, questionid):
        points = Questions.objects.filter(questionid = questionid).values_list('points')[0][0]
        hintactivated = StudentHints.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance).values_list('hintactivated')
        if len(hintactivated) != 0:
            points = points - int(Questions.objects.filter(questionid = questionid).values_list('hintpenalty')[0][0])
            print('deducted')
            print(points)

        correctanswer = Questions.objects.filter(questionid = questionid).values_list('answer')[0][0]
        isthisashortanswer = Questions.objects.filter(questionid = questionid).values_list('questiontype')[0][0]
        repeatedcheck = StudentQuestions.objects.filter(questionid = questionid, studentid = user, rangeid = rangeinstance)
        numberofrangequestions = Questions.objects.filter(rangeid=rangeinstance).count()
        progress = RangeStudents.objects.filter(rangeID=rangeinstance, studentID=user).values_list('progress')[0][0]
        if progress is None:
            progress = 0
        else:
            progress = int(progress)

        if len(repeatedcheck) == 0:
            print('repeatedcheck')
            check = False
            if isthisashortanswer == 'SA':
                saanswer = correctanswer.lower().split()
                givenanswer = answergiven.lower().split()
                print(saanswer)
                keywords = len(saanswer)
                keycheck = 0
                for x in saanswer:
                    for y in givenanswer:
                        if y in x:
                            keycheck += 1
                            if keycheck == keywords:
                                check = True
            elif isthisashortanswer == 'OE':
                check = False
            else:
                if answergiven.lower() == correctanswer.lower():
                    check = True

            print(check)
            studentobject = StudentQuestions()
            studentobject.studentid = user
            studentobject.rangeid = rangeinstance
            studentobject.questionid = questioninstance
            studentobject.answergiven = answergiven
            studentobject.answercorrect = check

            pointsobject = RangeStudents.objects.get(rangeID=rangeinstance, studentID=user)
            progress = progress + 1
            pointsobject.progress = progress
            pointsobject.lastaccess = timezone.now()
            pointsobject.save()

            if progress == numberofrangequestions:
                pointsobject = RangeStudents.objects.get(rangeID=rangeinstance, studentID=user)
                pointsobject.datecompleted = timezone.now()
                pointsobject.save()

            if check is True:
                print("here")
                pointsobject = RangeStudents.objects.get(rangeID = rangeinstance, studentID = user)
                pointsobject.points += points
                pointsobject.save()

                studentobject.marksawarded = points
                studentobject.save()
            
                return True
            else:
                studentobject.marksawarded = 0
                studentobject.save()

        else:
            return False

    class Meta:
        model = StudentQuestions
        fields = ('answergiven',)

class AnswerMCQForm(forms.ModelForm):
    answergiven = forms.ChoiceField(label='Answer', widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        self.choices = kwargs.pop('choices', None)
        #print(self.questionid)
        super(AnswerMCQForm, self).__init__(*args, **kwargs)
        self.fields['answergiven'].choices = self.choices

    def checkAnswer(self, user, answergiven, questioninstance, rangeinstance, questionid):
        points = Questions.objects.filter(questionid = questionid).values_list('points')[0][0]
        hintactivated = StudentHints.objects.filter(studentid = user, rangeid = rangeinstance, questionid = questioninstance).values_list('hintactivated')
        if len(hintactivated) != 0:
            points = points - int(Questions.objects.filter(questionid = questionid).values_list('hintpenalty')[0][0])
        correctanswer = Questions.objects.filter(questionid = questionid).values_list('answer')[0][0]

        repeatedcheck = StudentQuestions.objects.filter(questionid = questionid, studentid = user, rangeid = rangeinstance)
        
        numberofrangequestions = Questions.objects.filter(rangeid=rangeinstance).count()
        progress = RangeStudents.objects.filter(rangeID=rangeinstance, studentID=user).values_list('progress')[0][0]
        if progress is None:
            progress = 0
        else:
            progress = int(progress)

        if len(repeatedcheck) == 0:
            check = False
            if answergiven.lower() == correctanswer.lower():
                check = True

            studentobject = StudentQuestions()
            studentobject.studentid = user
            studentobject.rangeid = rangeinstance
            studentobject.questionid = questioninstance
            studentobject.answergiven = answergiven
            studentobject.answercorrect = check

            pointsobject = RangeStudents.objects.get(rangeID=rangeinstance, studentID=user)
            progress = progress + 1
            pointsobject.progress = progress
            pointsobject.lastaccess = timezone.now()
            pointsobject.save()

            if progress == numberofrangequestions:
                pointsobject = RangeStudents.objects.get(rangeID=rangeinstance, studentID=user)
                pointsobject.datecompleted = timezone.now()
                pointsobject.save()

            if check is True:
                studentobject.marksawarded = points
                pointsobject = RangeStudents.objects.get(rangeID = rangeinstance, studentID = user)
                pointsobject.points += points
                pointsobject.save()
                studentobject.save()
                return True
            else:
                studentobject.save()

        else:
            return False


    class Meta:
        model = StudentQuestions
        fields = ('answergiven',)