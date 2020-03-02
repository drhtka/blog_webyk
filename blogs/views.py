# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View
#from django.views.generic.base import View

from blogs.models import BlogPosts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    #  стартовая траница со всами постами всех пользователей
    def get(self, request):
        template_name = 'blogs/index.html'
        all_posts = BlogPosts.objects.all()
        u = self.request.user
        print(u)
        print(all_posts)
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
        print('hello')
        subscribe_idd = request.GET.get('idd')
        subscribe_id = int(request.GET.get('id'))
        #all_posts = BlogPosts.objects.only('subscribe').get(id=1)
        all_posts = BlogPosts.objects.values('subscribe')
        print(all_posts)

       # BlogPosts.objects.select_related().filter(author_id=subscribe_id).update(subscribe=subscribe_idd)
        return render(request, 'blogs/subscribe.html')


"""        print('req')
        subs = BlogPosts.objects.filter(author=True)
        print(subs)
        for object in subs:
            object.author = False
            print(object)
            object.save()
        #context={"subs":subs}
        return redirect(request, 'blogs/subscribe.html')"""
