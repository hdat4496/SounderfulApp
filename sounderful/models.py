# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Account(models.Model):
    userName = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=32)
    biography = models.TextField(null=True, blank=True)
    urlAvatar = models.CharField(max_length=255, null=True, blank=True)
    urlBackgroundImage = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.userName

    class Meta:
        app_label = 'sounderful'
        db_table = 'account'


class Post(models.Model):
    userName = models.ForeignKey(Account, db_constraint=False)
    title = models.CharField(max_length=32)
    urlTrack = models.CharField(max_length=255)
    urlImage = models.CharField(max_length=255, null=True, blank=True)
    postTime = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    listenNumber = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        app_label = 'sounderful'
        db_table = 'post'


class Comment(models.Model):
    userName = models.ForeignKey(Account, db_constraint=False)
    postId = models.ForeignKey(Post, db_constraint=False)
    context = models.TextField()
    commentTime = models.DateTimeField()

    class Meta:
        app_label = 'sounderful'
        db_table = 'comment'


class Like(models.Model):
    userName = models.ForeignKey(Account, db_constraint=False)
    postId = models.ForeignKey(Post, db_constraint=False)

    class Meta:
        app_label = 'sounderful'
        db_table = 'like'


class Following(models.Model):
    userNameA = models.ForeignKey(Account, db_constraint=False, related_name='following_fk_1')
    userNameB = models.ForeignKey(Account, db_constraint=False, related_name='following_fk_2')

    class Meta:
        app_label = 'sounderful'
        db_table = 'following'


class Notification(models.Model):
    userName = models.ForeignKey(Account, db_constraint=False)
    action = models.TextField()
    postId = models.ForeignKey(Post, db_constraint=False)
    notificationTime = models.DateTimeField()

    class Meta:
        app_label = 'sounderful'
        db_table = 'notification'
