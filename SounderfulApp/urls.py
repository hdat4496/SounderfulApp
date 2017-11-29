"""SounderfulApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from sounderful import views
from sounderful.views import AccountListCreateAPIView, AccountDetailUpdateAPIView, PostListCreateAPIView, \
    PostDetailUpdateAPIView, CommentListCreateAPIView, CommentDetailUpdateAPIView, LikeListCreateAPIView, \
    LikeDetailUpdateAPIView, FollowingListCreateAPIView, FollowingDetailUpdateAPIView, NotificationListCreateAPIView, \
    NotificationDetailUpdateAPIView

router = routers.SimpleRouter()
router.register(r'accounts', AccountListCreateAPIView, base_name="accounts")
router.register(r'accounts', AccountDetailUpdateAPIView, base_name="accounts")

router.register(r'posts', PostListCreateAPIView, base_name="posts")
router.register(r'posts', PostDetailUpdateAPIView, base_name="posts")

router.register(r'comments', CommentListCreateAPIView, base_name="comments")
router.register(r'comments', CommentDetailUpdateAPIView, base_name="comments")

router.register(r'likes', LikeListCreateAPIView, base_name="likes")
router.register(r'likes', LikeDetailUpdateAPIView, base_name="likes")

router.register(r'followings', FollowingListCreateAPIView, base_name="followings")
router.register(r'followings', FollowingDetailUpdateAPIView, base_name="followings")

router.register(r'notifications', NotificationListCreateAPIView, base_name="notifications")
router.register(r'notifications', NotificationDetailUpdateAPIView, base_name="notifications")

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^api/', include(router.urls)),
    url(r'^posts/(?P<username>.*)/follow/$', views.get_post_follow),
    url(r'^posts/(?P<username>.*)/like/$', views.get_post_like),
    url(r'^accounts/search/(?P<username>.*)/$', views.search_account_by_username),
    url(r'^posts/search/(?P<title>.*)/$', views.search_post_by_title),
    url(r'^notifications/filter/(?P<username>.*)/$', views.filter_notification_by_username),
    url(r'^posts/(?P<userNameParameter>.*)/$', views.get_post_of_user),
    url(r'^accounts/check/(?P<username>.*)/$', views.check_username),
    url(r'^accounts/checkfollow/(?P<usernameA>.*)/follow/(?P<usernameB>.*)/$', views.check_follow),
    url(r'^accounts/checklogin/$', views.check_login),
]
