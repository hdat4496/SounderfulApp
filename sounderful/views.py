# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import urllib
import urllib2

import os
from MySQLdb import connections
from django.core.files.storage import default_storage
from django.db.models import Count
from django.db.models.signals import post_delete, pre_delete, post_save
from django.dispatch import receiver
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.utils.encoding import uri_to_iri
from rest_framework import serializers, status
from rest_framework.decorators import api_view, detail_route
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView, )
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from SounderfulApp.settings import BASE_DIR
from sounderful.models import Account, Post, Comment, Like, Following, Notification


# Create your views here.

# Account
class AccountListSerializer(serializers.ModelSerializer):
    num_of_post = serializers.SerializerMethodField()
    num_of_follow = serializers.SerializerMethodField()
    num_of_follower = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = '__all__'

    def get_num_of_post(self, obj):
        return Post.objects.filter(userName=obj).count()

    def get_num_of_follow(self, obj):
        return Following.objects.filter(userNameA=obj).count()

    def get_num_of_follower(self, obj):
        return Following.objects.filter(userNameB=obj).count()


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
def get_post_follow(request, username):
    if request.method == 'GET':
        posts = Post.objects.filter(Q(userName__following_fk_2__userNameA=username) | Q(userName=username)).order_by(
            "-postTime").distinct()
        serializer = PostListSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def search_account_by_username(request, username):
    if request.method == 'GET':
        accounts = Account.objects.filter(userName__icontains=username)
        serializer = AccountListSerializer(accounts, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
def search_post_by_title(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        posts = Post.objects.filter(title__icontains=title)
        serializer = PostListSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def filter_notification_by_username(request, username):
    if request.method == 'GET':
        notifications = Notification.objects.filter(userName=username)
        serializer = NotificationListSerializer(notifications, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def get_post_of_user(request, userNameParameter):
    if request.method == 'GET':
        posts = Post.objects.filter(userName=userNameParameter).order_by("-postTime")
        serializer = PostListSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def check_username(request, username):
    if request.method == 'GET':
        account = Account.objects.filter(userName=username)
        if account:
            check = {
                'exists': 1
            }
            return JsonResponse(check, safe=False)
        check = {
            'exists': 0
        }
        return JsonResponse(check, safe=False)


@api_view(['POST'])
def check_login(request):
    if request.method == 'POST':
        username = request.POST.get('userName')
        password = request.POST.get('password')
        account = Account.objects.filter(Q(userName=username) & Q(password=password))
        print account.query
        print account
        if account:
            check = {
                'exists': 1
            }
            return JsonResponse(check, safe=False)
        check = {
            'exists': 0
        }
        return JsonResponse(check, safe=False)


@api_view(['GET'])
def check_follow(request, usernameA, usernameB):
    if request.method == 'GET':
        follow = Following.objects.filter(Q(userNameA=usernameA) & Q(userNameB=usernameB))
        print follow.query
        if follow:
            check = {
                'exists': 1
            }
            return JsonResponse(check, safe=False)
        check = {
            'exists': 0
        }
        return JsonResponse(check, safe=False)


@api_view(['GET'])
def get_post_like(request, username):
    if request.method == 'GET':
        post = Post.objects.filter(like__userName=username)
        serializer = PostListSerializer(post, many=True)
        return JsonResponse(serializer.data, safe=False)


class ImageUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request, format='jpg'):
        up_file = request.FILES['file']
        path = os.path.join(os.path.dirname(BASE_DIR),"SounderfulApp","Image")
        destination = open(path+'/'+up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        return Response(up_file.name, status.HTTP_201_CREATED)


class AudioUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request, format='mp3'):
        up_file = request.FILES['file']
        path = os.path.join(os.path.dirname(BASE_DIR),"SounderfulApp","Track")
        destination = open(path+'/'+up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        return Response(up_file.name, status.HTTP_201_CREATED)


@api_view(['GET'])
def download_image(request, fileName):
        path = os.path.join(os.path.dirname(BASE_DIR), "SounderfulApp", "Image",fileName)
        if os.path.exists(path):
            with open(path,'rb') as fh:
                respone = HttpResponse(fh.read(), content_type="image/*")
                respone['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
                return  respone
            raise Http404
        return Response({'test': path},status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def download_audio(request, fileName):
        path = os.path.join(os.path.dirname(BASE_DIR), "SounderfulApp", "Track",fileName)
        if os.path.exists(path):
            with open(path,'rb') as fh:
                respone = HttpResponse(fh.read(), content_type="audio/*")
                respone['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
                return  respone
            raise Http404
        return Response({'test': path},status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def delete_like(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        postid = request.POST.get('postid')
        like = Like.objects.filter(Q(userName=username) & Q(postId=postid))
        if not like: return HttpResponseNotFound()
        like.delete()
        return HttpResponse(status=status.HTTP_200_OK)

@receiver(pre_delete, sender=Post)
def file_post_delete_handler(sender, instance, **kwargs):
    post = instance
    imagepath = os.path.join(os.path.dirname(BASE_DIR), "SounderfulApp", "Image", post.urlImage)
    if os.path.exists(imagepath):
        default_storage.delete(imagepath)
    audiopath = os.path.join(os.path.dirname(BASE_DIR), "SounderfulApp", "Track", post.urlTrack)
    if os.path.exists(audiopath):
        default_storage.delete(audiopath)

@api_view(['POST'])
def delete_follow(request):
    if request.method == 'POST':
        usernameA = request.POST.get('usernameA')
        usernameB = request.POST.get('usernameB')
        follow = Following.objects.filter(Q(userNameA=usernameA) & Q(userNameB=usernameB))
        if not follow: return HttpResponseNotFound()
        follow.delete()
        return HttpResponse(status=status.HTTP_200_OK)

@api_view(['GET'])
def get_comments_of_post(request, postid):
    if request.method == 'GET':
        comments = Comment.objects.filter(postId=postid).order_by("-commentTime")
        serializer = CommentListSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)

class ImageModifyView(APIView):
    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request, format=None):
        up_file = request.FILES['file']
        post_id = request.data.get('postid')
        post = Post.objects.get(id=post_id)
        if post.urlImage is not None:
            image_path = os.path.join(os.path.dirname(BASE_DIR), "SounderfulApp", "Image", post.urlImage)
            default_storage.delete(image_path)
        path = os.path.join(os.path.dirname(BASE_DIR),"SounderfulApp","Image")
        destination = open(path+'/'+up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        post.urlImage = up_file.name
        post.save()
        return Response(up_file.name, status.HTTP_201_CREATED)


@api_view(['POST'])
def modify_post(request):
    if request.method == 'POST':
        postid = request.POST.get('id')
        title = request.POST.get('title')
        description = request.POST.get('description')
        post = Post.objects.get(id=postid)
        if not post: return HttpResponseNotFound()
        post.title = title
        post.description = description
        post.save()
        return HttpResponse(status=status.HTTP_200_OK)


class ImageUserModifyView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser, )

    def post(self, request, format=None):
        up_file = request.FILES['file']
        username = request.data.get('username').replace("\"","")
        accountFilter = Account.objects.filter(userName=username)
        if not accountFilter:
            return HttpResponseNotFound()
        account = accountFilter.get()
        if account.urlAvatar is not None:
            image_path = os.path.join(os.path.dirname(BASE_DIR), "SounderfulApp", "Image", account.urlAvatar)
            default_storage.delete(image_path)
        path = os.path.join(os.path.dirname(BASE_DIR),"SounderfulApp","Image")
        destination = open(path+'/'+up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        account.urlAvatar = up_file.name
        account.save()
        return Response(up_file.name, status.HTTP_201_CREATED)

class BackgroundUserModifyView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser, )

    def post(self, request, format=None):
        up_file = request.FILES['file']
        username = request.data.get('username').replace("\"","")
        accountFilter = Account.objects.filter(userName=username)
        if not accountFilter:
            return HttpResponseNotFound()
        account = accountFilter.get()
        if account.urlBackgroundImage is not None:
            image_path = os.path.join(os.path.dirname(BASE_DIR), "SounderfulApp", "Image", account.urlBackgroundImage)
            default_storage.delete(image_path)
        path = os.path.join(os.path.dirname(BASE_DIR),"SounderfulApp","Image")
        destination = open(path+'/'+up_file.name, 'wb+')
        for chunk in up_file.chunks():
            destination.write(chunk)
        account.urlBackgroundImage = up_file.name
        account.save()
        return Response(up_file.name, status.HTTP_201_CREATED)

@receiver(post_save, sender=Like)
def like_post_save_handler(sender, instance, **kwargs):
    like = instance
    username = like.userName
    postId = like.postId
    action = 'like'
    post_username = Post.objects.filter(id=postId.id).get().userName
    print post_username
    if username != post_username:
        notification = Notification.objects.create(userName=username, postId=postId, action=action)
        notification.save()


@receiver(post_save, sender=Comment)
def comment_post_save_handler(sender, instance, **kwargs):
    comment = instance
    username = comment.userName
    postId = comment.postId
    action = 'comment'
    post_username = Post.objects.filter(id=postId.id).get().userName
    print post_username
    if username != post_username:
        notification = Notification.objects.create(userName=username, postId=postId, action=action)
        notification.save()

@api_view(['GET'])
def get_notification_of_user(request, username):
    if request.method == 'GET':
        notification = Notification.objects.filter(postId__userName=username).order_by("-notificationTime")
        serializer = NotificationListSerializer(notification, many=True)
        return JsonResponse(serializer.data, safe=False)