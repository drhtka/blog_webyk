# -*- coding: utf-8 -*-
from django import forms
from blogs.models import BlogPosts

class BlogPostsForms(forms.ModelForm):
    class Meta:
        model = BlogPosts
        fields = ('title', 'text')
