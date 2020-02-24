# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from blogs.views import PostsListView
#from blogs.feeds import LatestPostFeed


app_name = 'blog_posts'

urlpatterns = [
    url('^list/', PostsListView.as_view(), name='list'),#<str:slug>/

#    url('^create/$', PostCreateView.as_view(), name='create'),
#    url(r'^feed/$', LatestPostFeed(), name='post_feed'),
#    url(r'^detail/(?P<pk>\d+)/(?P<slug>[-\w]+)/$', LatestPostFeed(), name='detail'),

]

