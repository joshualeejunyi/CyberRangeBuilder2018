from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from ranges.models import Range
# Create your models here.

class UserClass(models.Model):
    userclass = models.CharField(db_column='class', max_length=45)

    class Meta:
        db_table = 'UserClass'
        verbose_name_plural = 'UserClass'


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_column='email', primary_key = True)
    username = models.CharField(db_column='username', max_length=45, unique=True)
    password = models.CharField(db_column='password', max_length=100,)
    name = models.CharField(db_column='name', max_length=100)
    userclass = models.ForeignKey('accounts.UserClass', on_delete=models.DO_NOTHING, db_column='UserClass', blank=True, null=True, related_name='UC')
    datejoined = models.DateField(db_column='dateJoined', blank=True, null=True)
    lastmodifieddate = models.DateField(db_column='lastModifiedDate', blank=True, null=True)
    lastmodifiedtime = models.TimeField(db_column='lastModifiedTime', null=True)
    lastmodifiedby = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, db_column='lastModifiedBy', blank=True, null=True, related_name="LMB")
    acceptedby = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, db_column='acceptedBy', related_name="AB", null=True) 
    last_login = models.DateTimeField(db_column='lastlogin', blank=True, null=True)
    is_superuser = models.BooleanField(db_column='admin', default=False)
    is_staff = models.BooleanField(db_column='teacher', default=False)
    isdisabled = models.BooleanField(db_column='isdisabled', default=False)
    isaccepted = models.BooleanField(db_column='isaccepted', default=False)
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-lastmodifieddate', '-lastmodifiedtime']

class FakeUser(models.Model):
    email = models.EmailField(db_column='email', primary_key = True)
    username = models.CharField(db_column='username', max_length=45, unique=True)
    password = models.CharField(db_column='password', max_length=100,)
    name = models.CharField(db_column='name', max_length=100)
    userclass = models.ForeignKey('accounts.UserClass', on_delete=models.DO_NOTHING, db_column='UserClass', blank=True, null=True, related_name='fUC')
    datejoined = models.DateField(db_column='dateJoined', blank=True, null=True)
    lastmodifieddate = models.DateField(db_column='lastModifiedDate', blank=True, null=True)
    lastmodifiedtime = models.TimeField(db_column='lastModifiedTime', null=True)
    lastmodifiedby = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, db_column='lastModifiedBy', blank=True, null=True, related_name="fLMB")
    acceptedby = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, db_column='acceptedBy', related_name="fAB", null=True) 
    last_login = models.DateTimeField(db_column='lastlogin', blank=True, null=True)
    is_superuser = models.BooleanField(db_column='admin', default=False)
    is_staff = models.BooleanField(db_column='teacher', default=False)
    isdisabled = models.BooleanField(db_column='isdisabled', default=False)
    isaccepted = models.BooleanField(db_column='isaccepted', default=False)
    
    class Meta:
        app_label = User._meta.app_label
        db_table = User._meta.db_table
        managed = False

class Group(models.Model):
    groupid = models.AutoField(db_column='groupID', primary_key=True)
    groupname = models.CharField(db_column='groupName', max_length=45, unique=True)
    groupleader = models.ForeignKey("User", on_delete=models.DO_NOTHING, db_column='groupLeader', null=True, related_name="groupleader")
    datecreated = models.DateField(db_column='dateCreated', null=True)
    timecreated = models.TimeField(db_column='timeCreated', null=True)
    grouppoints = models.IntegerField(db_column='groupPoints', null=True, default=0)
    createdby = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, db_column='createdBy', related_name="groupcreatedby", null=True)
    lastmodifieddate = models.DateField(db_column='lastModifiedDate', blank=True, null=True)
    lastmodifiedtime = models.TimeField(db_column='lastModifiedTime', null=True)
    lastmodifiedby = models.ForeignKey('accounts.User', on_delete=models.DO_NOTHING, db_column='lastModifiedBy', blank=True, null=True, related_name="GLMB")
    
    class Meta:
        db_table = 'Group'
        verbose_name_plural = 'Groups'

class StudentGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    studentid = models.ForeignKey("User", on_delete=models.CASCADE, db_column='studentID')
    groupid = models.ForeignKey("Group", on_delete=models.DO_NOTHING, db_column='groupID')

    class Meta:
        db_table = 'StudentGroup'
        verbose_name_plural = 'StudentGroups'

class FakeStudentGroup(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    studentid = models.ForeignKey("User", models.DO_NOTHING, db_column='studentID')
    groupid = models.ForeignKey("Group", models.DO_NOTHING, db_column='groupID')

    class Meta:
        app_label = StudentGroup._meta.app_label
        db_table = StudentGroup._meta.db_table
        managed = False

class GroupRange(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    groupid = models.ForeignKey("Group", models.DO_NOTHING, db_column='groupID')
    rangeid = models.ForeignKey("ranges.Range", models.DO_NOTHING, db_column='rangeID')
    datecreated = models.DateField(db_column='dateCreated', null=True)
    timecreated = models.TimeField(db_column='timeCreated', null=True)
    grouprangepoints = models.IntegerField(db_column='groupRangePoints', null=True, default=0)
    addedby = models.ForeignKey('accounts.User', models.DO_NOTHING, db_column='addedBy', null=True)

    class Meta:
        db_table = 'GroupRange'
        verbose_name_plural = 'GroupRanges'