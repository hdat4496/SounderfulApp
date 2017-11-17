# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,)
from rest_framework import viewsets
from sounderful.models import Account
# Create your views here.


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('userName', 'password')


# API get detail, update, delete
class AccountDetailUpdateAPIView(viewsets.GenericViewSet, RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer
    lookup_field = 'userName'


# API get list and create
class AccountListCreateAPIView(viewsets.GenericViewSet, ListCreateAPIView):
    serializer_class = AccountListSerializer
    queryset = Account.objects.all()