from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(db_column='email', primary_key = True)
    username = models.CharField(db_column='username', max_length=45, unique=True)
    password = models.CharField(db_column='password', max_length=100,)
    name = models.CharField(db_column='name', max_length=100)
    datejoined = models.DateField(db_column='dateJoined', blank=True, null=True)  # Field name made lowercase.
    lastmodifieddate = models.DateField(db_column='lastModifiedDate', blank=True, null=True)  # Field name made lowercase.
    lastmodifedby = models.ForeignKey("User", models.DO_NOTHING, db_column='lastModifedBy', blank=True, null=True, related_name="LMB")  # Field name made lowercase.
    acceptedby = models.ForeignKey("User", models.DO_NOTHING, db_column='acceptedBy', related_name="AB", null=True)  # Field name made lowercase.
    last_login = models.DateTimeField(db_column='lastlogin', blank=True, null=True)
    is_superuser = models.BooleanField(db_column='admin', default=False)
    is_staff = models.BooleanField(db_column='teacher', default=False)
    #userclass = models.CharField(db)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'User'
        verbose_name_plural = 'Users'




