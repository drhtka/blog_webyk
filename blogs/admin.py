# -*- coding: utf-8 -*-
from django.contrib import admin

from blogs.models import BlogPosts

class BlogPostsAdmin(admin.ModelAdmin):

    list_display = ('author', 'title', 'created', 'status')
    list_filter = ('author', 'status')
    raw_id_fields = ('author',)
    ordering = ('created',)

admin.site.register(BlogPosts, BlogPostsAdmin,)