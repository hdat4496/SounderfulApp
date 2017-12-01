# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from rest_framework import request


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
    userName = models.ForeignKey(Account, db_constraint=False, to_field="userName", db_column="userName")
    title = models.CharField(max_length=255)
    urlTrack = models.CharField(max_length=255, blank=True, default="")
    urlImage = models.CharField(max_length=255, null=True, blank=True)
    postTime = models.DateTimeField(auto_now_add=True, blank=True)
    description = models.TextField(null=True, blank=True)
    listenNumber = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.pk

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'sounderful'
        db_table = 'post'


class Comment(models.Model):
    userName = models.ForeignKey(Account, db_constraint=False, to_field="userName", db_column="userName")
    postId = models.ForeignKey(Post, db_constraint=False, to_field="id", db_column="postId")
    context = models.TextField()
    commentTime = models.DateTimeField()

    class Meta:
        app_label = 'sounderful'
        db_table = 'comment'


class Like(models.Model):
    userName = models.ForeignKey(Account, db_constraint=False, to_field="userName", db_column="userName")
    postId = models.ForeignKey(Post, db_constraint=False, to_field="id", db_column="postId")

    class Meta:
        app_label = 'sounderful'
        db_table = 'like'
        unique_together = ("userName", "postId")


class Following(models.Model):
    userNameA = models.ForeignKey(Account, db_constraint=False, to_field="userName", db_column="userNameA", related_name='following_fk_1')
    userNameB = models.ForeignKey(Account, db_constraint=False, to_field="userName", db_column="userNameB", related_name='following_fk_2')

    class Meta:
        app_label = 'sounderful'
        db_table = 'following'
        unique_together = ("userNameA", "userNameB")


class Notification(models.Model):
    userName = models.ForeignKey(Account, db_constraint=False, to_field="userName", db_column="userName")
    action = models.TextField()
    postId = models.ForeignKey(Post, db_constraint=False, to_field="id", db_column="postId")
    notificationTime = models.DateTimeField()

    class Meta:
        app_label = 'sounderful'
        db_table = 'notification'
