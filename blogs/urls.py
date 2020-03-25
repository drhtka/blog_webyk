# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from blogs.views import PostsListView, SubscribeListView, TapeListView, UnSubscribeListView, ReadPostTemplView#, SendPost
#from blogs.feeds import LatestPostFeed


#app_name = 'blog_posts'

urlpatterns = [
    url('^list/', PostsListView.as_view(), name='list'),#<str:slug>/
    url(r'^subscribe', SubscribeListView.as_view(), name='subscribe'),
    url(r'^tapelist', TapeListView.as_view(), name='subscribe'),
    url(r'^unsubscribe', UnSubscribeListView.as_view(), name='unsibscribe'),
    url(r'^readpost', ReadPostTemplView.as_view(), name='readpost'),
    #url(r'^sendpost', SendPost.as_view(), name='sendpost'),

]

