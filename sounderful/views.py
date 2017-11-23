# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.decorators import api_view, detail_route
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,)
from rest_framework import viewsets
from rest_framework.views import APIView

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


# Post for get
class PostListSerializer(serializers.ModelSerializer):
    userName = AccountListSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


# Post for post, put, delete
class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


# API get detail, update, delete
class PostDetailUpdateAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()

    serializer_class = PostListSerializer
    lookup_field = 'id'


# API get list and create
class PostListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView,APIView):
    queryset = Post.objects.select_related().all()

    def get_serializer_class(self):
        if self.request.POST:
            return PostCreateSerializer
        return PostListSerializer


# Comment for get
class CommentListSerializer(serializers.ModelSerializer):
    userName = AccountListSerializer()
    postId = PostListSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


# Comment for post, put, delete
class CommentCreateSerializer(serializers.ModelSerializer):

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
    queryset = Comment.objects.all()

    def get_serializer_class(self):
        if self.request.POST:
            return CommentCreateSerializer
        return CommentListSerializer


# Like for get
class LikeListSerializer(serializers.ModelSerializer):
    # userName = AccountListSerializer()
    # postId = PostListSerializer()

    class Meta:
        model = Like
        fields = '__all__'


# Like for post, put, delete
class LikeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'


# API get detail, update, delete
class LikeDetailUpdateAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.values_list('userName', 'postId').all()
    serializer_class = LikeListSerializer
    lookup_field = 'postId'


# API get list and create
class LikeListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView):
    queryset = Like.objects.values_list('userName', 'postId').all()

    def get_serializer_class(self):
        if self.request.POST:
            return LikeCreateSerializer
        return LikeListSerializer


# Following
class FollowingListSerializer(serializers.ModelSerializer):
    userNameA = AccountListSerializer()
    userNameB = AccountListSerializer()

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
    userName = AccountListSerializer()
    postId = PostListSerializer()

    class Meta:
        model = Notification
        fields = '__all__'


# Notification
class NotificationCreateSerializer(serializers.ModelSerializer):

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

    def get_serializer_class(self):
        if self.request.POST:
            return NotificationCreateSerializer
        return NotificationListSerializer