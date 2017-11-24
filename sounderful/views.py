# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from MySQLdb import connections
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.decorators import api_view, detail_route
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,)
from rest_framework import viewsets
from rest_framework.views import APIView
from django.db import connection
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


# Post for get, put, delete
class PostListSerializer(serializers.ModelSerializer):
    userName = AccountListSerializer(read_only=True)
    num_of_like = serializers.SerializerMethodField()
    num_of_comment = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_num_of_like(self, obj):
        return Like.objects.filter(postId=obj).count()

    def get_num_of_comment(self, obj):
        return Comment.objects.filter(postId=obj).count()


# Post for post
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
class PostListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView, APIView):
    queryset = Post.objects.select_related().all()

    def get_serializer_class(self):
        if self.request.POST:
            return PostCreateSerializer
        return PostListSerializer


# Comment for get, put, delete
class CommentListSerializer(serializers.ModelSerializer):
    userName = AccountListSerializer()
    postId = PostListSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


# Comment for post
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


# Like for get, put, delete
class LikeListSerializer(serializers.ModelSerializer):
    userName = AccountListSerializer()
    postId = PostListSerializer()

    class Meta:
        model = Like
        fields = '__all__'


# Like for post
class LikeCreateSerializer(serializers.ModelSerializer):

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
    queryset = Like.objects.all()

    def get_serializer_class(self):
        if self.request.POST:
            return LikeCreateSerializer
        return LikeListSerializer


# Following for get, put, delete
class FollowingListSerializer(serializers.ModelSerializer):
    userNameA = AccountListSerializer()
    userNameB = AccountListSerializer()

    class Meta:
        model = Following
        fields = '__all__'


# Following for post
class FollowingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Following
        fields = '__all__'


# API get detail, update, delete
class FollowingDetailUpdateAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView):
    queryset = Following.objects.all()
    serializer_class = FollowingListSerializer
    lookup_field = 'id'


# API get list and create
class FollowingListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView):
    queryset = Following.objects.all()

    def get_serializer_class(self):
        if self.request.POST:
            return FollowingCreateSerializer
        return FollowingListSerializer


# Notification for get, put, delete
class NotificationListSerializer(serializers.ModelSerializer):
    userName = AccountListSerializer()
    postId = PostListSerializer()

    class Meta:
        model = Notification
        fields = '__all__'


# Notification for post
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
    queryset = Notification.objects.all()

    def get_serializer_class(self):
        if self.request.POST:
            return NotificationCreateSerializer
        return NotificationListSerializer


@api_view(['GET'])
def get_post_follow(request, userName):
    if request.method == 'GET':
        posts = Post.objects.filter(userName__following_fk_2__userNameA=userName)
        serializer = PostListSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)