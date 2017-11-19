# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,)
from rest_framework import viewsets
from sounderful.models import Account, Post, Comment, Like, Following, Notification


# Create your views here.

# Account
class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


# API get detail, update, delete
class AccountDetailUpdateAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer
    lookup_field = 'userName'


# API get list and create
class AccountListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView):
    serializer_class = AccountListSerializer
    queryset = Account.objects.all()


# Post
class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


# API get detail, update, delete
class PostDetailUpdateAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    lookup_field = 'id'


# API get list and create
class PostListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView):
    serializer_class = PostListSerializer
    queryset = Post.objects.all()


# Comment
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


# API get detail, update, delete
class CommentDetailUpdateAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    lookup_field = 'id'


# API get list and create
class CommentListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView):
    serializer_class = CommentListSerializer
    queryset = Comment.objects.all()


# Like
class LikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


# API get detail, update, delete
class LikeDetailUpdateAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeListSerializer
    lookup_field = 'id'


# API get list and create
class LikeListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView):
    serializer_class = LikeListSerializer
    queryset = Like.objects.all()


# Following
class FollowingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = '__all__'


# API get detail, update, delete
class FollowingDetailUpdateAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = FollowingListSerializer
    lookup_field = 'id'


# API get list and create
class FollowingListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView):
    serializer_class = FollowingListSerializer
    queryset = Following.objects.all()


# Notification
class NotificationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


# API get detail, update, delete
class NotificationDetailUpdateAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationListSerializer
    lookup_field = 'id'


# API get list and create
class NotificationListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView):
    serializer_class = NotificationListSerializer
    queryset = Notification.objects.all()