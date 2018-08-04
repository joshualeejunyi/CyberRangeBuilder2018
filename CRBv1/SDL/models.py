from django.db import models

from tinymce import HTMLField
# Create your models here.

class SDLPost(models.Model):
    postid = models.AutoField(db_column='postID', primary_key=True)
    title = models.CharField(db_column='posttitle', max_length=255, null=True)
    text = HTMLField(db_column='posttext', default="")
    createdby = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, db_column='createdby', related_name="SDLcreatedby", null=True)
    datecreated = models.DateField(db_column='dateCreated', null=True)
    timecreated = models.TimeField(db_column='timeCreated', null=True)
    dateposted = models.DateField(db_column='datePosted', null=True)
    timeposted = models.TimeField(db_column='timePosted', null=True)
    lastmodifieddate = models.DateField(db_column='LastModifiedDate', null=True)
    lastmodifiedtime = models.TimeField(db_column='LastModifiedTime', null=True)
    postactive = models.BooleanField(db_column='postActive', default=False)

    class Meta:
        db_table = 'SDLPost'
        verbose_name_plural = 'SDLPosts'

class SDLComment(models.Model):
    commentid = models.AutoField(db_column='commentID', primary_key=True)
    comment = models.CharField(db_column='comment', max_length=255, null=True)
    postid = models.ForeignKey('SDL.SDLPost', on_delete=models.CASCADE, db_column='postid', null=True)
    commenter = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, db_column='commenter', null=True)
    dateposted = models.DateField(db_column='datePosted', null=True)
    timeposted = models.TimeField(db_column='timePosted', null=True)

    class Meta:
        db_table = 'SDLComment'
        verbose_name_plural = 'SDLComments'