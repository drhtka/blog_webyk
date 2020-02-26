# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View
#from django.views.generic.base import View

from blogs.models import BlogPosts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class IndexTemplateView(TemplateView):
    #  стартовая траница со всами постами всех пользователей
    def get(self, request):
        template_name = 'blogs/index.html'
        all_posts = BlogPosts.objects.all()
        context = {'all_posts': all_posts}
        return render(request, template_name, context)



class PostsListView(LoginRequiredMixin, ListView):
    #  страница блога зарегестрированного пользователя
    model = BlogPosts
    context_object_name = "posts"
    template_name = 'blogs/details.html'
    login_url = 'login'

    def get_queryset(self):#здесь поквазывает посты закрепленные за пользователем
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(author=u)

class SubscribeListView(LoginRequiredMixin, TemplateView):
    print('hhhh')
    # подписка отписка на блоги пользователей
    model = BlogPosts
    context_object_name = "subsc"
    template_name = 'blogs/subscribe.html'
    login_url = 'subscribe'
    print('subsc')
    def get(self, request):
        subs = BlogPosts.objects.get(author=request.user)
        subs.save()
        return redirect(request, 'blogs/subscribe.html')
