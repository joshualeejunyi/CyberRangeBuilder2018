from django.db import models
from teachers.choices import *
from tinymce import HTMLField
# Create your models here.

class Range(models.Model):
    rangeid = models.AutoField(db_column='rangeID', primary_key=True)
    rangename = models.CharField(db_column='rangeName', max_length=45)
    rangeactive = models.BooleanField(db_column='rangeActive', default=False)
    datecreated = models.DateField(db_column='dateCreated', blank=True, null=True)
    datestart = models.DateField(db_column='dateStart', blank=True, null=True)
    timestart = models.TimeField(db_column='timeStart', blank=True, null=True)
    dateend = models.DateField(db_column='dateEnd', blank=True, null=True)
    timeend = models.TimeField(db_column='timeEnd', blank=True, null=True)
    maxscore = models.PositiveIntegerField(db_column='maxScore', default=0, blank=True, null=True)
    lastmodifieddate = models.DateField(db_column='lastModifiedDate', blank=True, null=True)
    rangecode = models.IntegerField(db_column='rangeCode', blank=True, null=True, unique=True)
    lastmodifiedby = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, db_column='lastModifiedBy', blank=True, null=True, related_name='LMBR')
    createdby = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='createdby', related_name='CBR', default='super')
    rangeurl = models.CharField(db_column='rangeURL', max_length=50, null=True, unique=True)
    studentsinrange = models.PositiveIntegerField(db_column='studentsInRange', default=0,null=True)
    isdisabled = models.BooleanField(db_column='isDisabled', default=False)
    isopen = models.BooleanField(db_column='isOpen', default=False)
    rangeinfo = HTMLField(db_column='rangeInfo', default="")
    attempts = models.PositiveIntegerField(db_column='attempts', default=0)
    manualactive = models.BooleanField(db_column = 'manualactive', default=0)
    manualdeactive = models.BooleanField(db_column = 'manualdeactive', default=0)
    
    class Meta:
        db_table = 'Range'
        verbose_name_plural = 'Ranges'
        ordering = ['-rangeid']

class FakeRange(models.Model):
    rangeid = models.AutoField(db_column='rangeID', primary_key=True)
    rangename = models.CharField(db_column='rangeName', max_length=45)
    rangeactive = models.BooleanField(db_column='rangeActive', default=False)
    datecreated = models.DateField(db_column='dateCreated', blank=True, null=True)
    datestart = models.DateField(db_column='dateStart', blank=True, null=True)
    timestart = models.TimeField(db_column='timeStart', blank=True, null=True)
    dateend = models.DateField(db_column='dateEnd', blank=True, null=True)
    timeend = models.TimeField(db_column='timeEnd', blank=True, null=True)
    maxscore = models.PositiveIntegerField(db_column='maxScore', default=0, blank=True, null=True)
    lastmodifieddate = models.DateField(db_column='lastModifiedDate', blank=True, null=True)
    rangecode = models.IntegerField(db_column='rangeCode', blank=True, null=True, unique=True)
    lastmodifiedby = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, db_column='lastModifiedBy', blank=True, null=True, related_name='fLMBR')
    createdbyusername = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='createdby', related_name='fCBR', default='super')
    rangeurl = models.CharField(db_column='rangeURL', max_length=50, null=True, unique=True)
    studentsinrange = models.PositiveIntegerField(db_column='studentsInRange', default=0,null=True)
    isdisabled = models.BooleanField(db_column='isDisabled', default=False)
    isopen = models.BooleanField(db_column='isOpen', default=False)
    rangeinfo = HTMLField(db_column='rangeInfo', default="")
    attempts = models.PositiveIntegerField(db_column='attempts', default=0)
    manualactive = models.BooleanField(db_column = 'manualactive', default=0)
    manualdeactive = models.BooleanField(db_column = 'manualdeactive', default=0)

    class Meta:
        app_label = Range._meta.app_label
        db_table = Range._meta.db_table
        managed = False


class RangeStudents(models.Model):
    dateJoined = models.DateTimeField(db_column='dateJoined', max_length=45, blank=True, null=True)
    points = models.IntegerField(db_column='points', default=0)
    datecompleted = models.DateTimeField(db_column='datecompleted', null=True)
    rangeID = models.ForeignKey(Range, on_delete=models.CASCADE, db_column='rangeID',unique=False)
    studentID = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='email', unique=False)
    lastaccess = models.DateTimeField(db_column='lastaccess', null=True)
    groupid = models.ForeignKey('accounts.Group', on_delete=models.CASCADE, db_column="groupid", null=True, blank=True)

    REQUIRED_FIELDS = ['rangeID', 'studentID']

    class Meta:
        db_table = 'RangeStudents'
        verbose_name_plural = 'RangeStudents'

class QuestionTopic(models.Model):
    topicid = models.AutoField(db_column='topicid', primary_key=True)
    topicname = models.CharField(db_column='topicname', max_length=100, null=True)

    class Meta:
        db_table = 'QuestionTopic'
        verbose_name_plural = 'QuestionTopics'

class Questions(models.Model):
    questionid = models.AutoField(db_column='questionID', primary_key=True)
    questiontype = models.CharField(db_column='questiontype', choices = QUESTION_TYPE_CHOICES, default='FL', max_length=100)
    title = models.CharField(db_column='questiontitle', max_length=255, null=True)
    text = HTMLField(db_column='questiontext', default="")
    hint = models.TextField(db_column='hint')
    hintpenalty = models.PositiveIntegerField(db_column='hintpenalty', default=0)
    topicid = models.ForeignKey(QuestionTopic, on_delete=models.SET_NULL, db_column='topicid', unique=False, related_name='catid', null=True)
    createdby = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, db_column='createdby', related_name="questioncreatedby", null=True)
    datecreated = models.DateTimeField(db_column='dateCreated', blank=True, null=True)
    points = models.PositiveIntegerField(db_column='points', default=0)
    answer = models.TextField(db_column='answer', null=True)
    rangeid = models.ForeignKey(Range, db_column = 'rangeid', on_delete=models.CASCADE, null=True)
    usedocker = models.BooleanField(db_column='usedocker', default=False)
    registryid = models.CharField(db_column='registryID', max_length=255, null=True)
    isarchived = models.BooleanField(db_column='isArchived', default=False)
    remarks = models.CharField(db_column='remarks', max_length=255, null=True)

    class Meta:
        db_table = 'Questions'
        verbose_name_plural = 'Questions'
        ordering = ['-questionid']

class MCQOptions(models.Model):
    questionid = models.OneToOneField(Questions, models.CASCADE, db_column='questionid', unique=True)
    optionone = models.CharField(db_column='OptionOne', max_length=100)
    optiontwo = models.CharField(db_column='OptionTwo', max_length=100)
    optionthree = models.CharField(db_column='OptionThree', max_length=100)
    optionfour = models.CharField(db_column='OptionFour', max_length=100)
    
    class Meta:
        db_table = 'MCQOptions'
        verbose_name_plural = 'MCQOptions'

class StudentQuestions(models.Model):
    studentid = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='email', unique=False)
    rangeid = models.ForeignKey(Range, on_delete=models.CASCADE, db_column='rangeID',unique=False)
    questionid = models.ForeignKey(Questions, on_delete=models.CASCADE, db_column='questionid', unique=False)
    answergiven = models.TextField(db_column='answergiven', null=True)
    answercorrect = models.BooleanField(db_column='right/wrong', default=False)
    marksawarded = models.PositiveIntegerField(db_column='marksawarded', default=0)
    attempts = models.PositiveIntegerField(db_column='attempts', default=1)
    ismarked = models.BooleanField(db_column='ismarked', default=False)

    class Meta:
        db_table = 'StudentQuestions'
        verbose_name_plural = 'StudentQuestions'


class StudentHints(models.Model):
    studentid = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='studentid', unique=False)
    rangeid = models.ForeignKey(Range, on_delete=models.CASCADE, db_column='rangeid', unique=False)
    questionid = models.ForeignKey(Questions, on_delete=models.CASCADE, db_column='questionid', unique=False)
    hintactivated = models.BooleanField(db_column='hintactivated', default=False)

    class Meta:
        db_table = 'StudentHints'
        verbose_name_plural = 'StudentHints'

class UnavailablePorts(models.Model):
    portnumber = models.PositiveIntegerField(db_column='portNumber', primary_key=True)
    studentid = models.ForeignKey('accounts.User', on_delete=models.CASCADE, db_column='studentid')
    containername = models.TextField(db_column='containerName', null=True)
    datetimecreated = models.DateTimeField(db_column='dateTimeCreated', null=True)

    class Meta:
        db_table = 'UnavailablePorts'
        verbose_name_plural = 'UnavailablePorts'
        ordering = ['-portnumber']