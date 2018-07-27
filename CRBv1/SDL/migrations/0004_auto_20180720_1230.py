# Generated by Django 2.0.7 on 2018-07-20 04:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('SDL', '0003_auto_20180717_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='SDLComment',
            fields=[
                ('commentid', models.AutoField(db_column='commentID', primary_key=True, serialize=False)),
                ('comment', models.CharField(db_column='comment', max_length=255, null=True)),
                ('dateposted', models.DateField(db_column='datePosted', null=True)),
                ('timeposted', models.TimeField(db_column='timePosted', null=True)),
                ('commenter', models.ForeignKey(db_column='commenter', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'SDLComment',
                'db_table': 'SDLComment',
            },
        ),
        migrations.RenameField(
            model_name='sdlpost',
            old_name='postID',
            new_name='postid',
        ),
        migrations.AddField(
            model_name='sdlcomment',
            name='postid',
            field=models.ForeignKey(db_column='postid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='SDL.SDLPost'),
        ),
    ]
