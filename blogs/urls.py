# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from blogs.views import PostsListView, SubscribeListView, \
    TapeListView, UnSubscribeListView, ReadPostTemplView, \
    AddPostView, AddTestView, DetailPostView#, SendPost
#from blogs.feeds import LatestPostFeed


#app_name = 'blog_posts'

urlpatterns = [
    url('^list', PostsListView.as_view(), name='list'),#<str:slug>/
    url(r'^subscribe', SubscribeListView.as_view(), name='subscribe'),
    url(r'^tapelist', TapeListView.as_view(), name='tapelist'),
    url(r'^unsubscribe', UnSubscribeListView.as_view(), name='unsibscribe'),
    url(r'^readpost', ReadPostTemplView.as_view(), name='readpost'),
    url(r'^addpost', AddPostView.as_view(), name='addpost'),
    url(r'^addtest', AddTestView.as_view(), name='addtest'),
    url(r'^detailpost', DetailPostView.as_view(), name='detailpost'),
    #url(r'^sendpost', SendPost.as_view(), name='sendpost'),

]

