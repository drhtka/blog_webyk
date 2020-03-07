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

    def get_queryset(self):#здесь покaвазывает посты закрепленные за пользователем
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(author=u)

class TapeListView(LoginRequiredMixin, ListView):

    def get(self, request):
        #print(self.request.user)
        #tape users which subscribe
        print('lenta_test')
        ug = self.request.user.id
        print(ug)
        test_like = BlogPosts.objects.filter(subscribe__contains=ug).values('author_id')# фильтруем подписанных авторизированных по полю автор айди
        print(test_like)
        test_list = []
        for test_likes in test_like:
            print(test_likes['author_id'])
            test_list.append(test_likes['author_id'])
        print(test_list)
        list_entr = BlogPosts.objects.filter(author_id__in=list(test_list)).values_list('title', 'text', 'created', 'status' )#.values('title')
        print(list_entr)
        return render(request, 'blogs/tapelist.html', {'list_entr': list_entr})


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

        #subs_posts = BlogPosts.objects.values('subscribe')
        all_posts = BlogPosts.objects.only('subscribe', 'author_id').get(author_id=subscribe_idd)
        #print(subs_posts[0]['subscribe'])
        print(all_posts)
        test_all=BlogPosts.objects.filter(author_id=subscribe_id).values('subscribe')#.update(field2='cool')
        print(test_all[0]['subscribe'])
        temp_subs = test_all[0]['subscribe']
        temp_subs = temp_subs + ',' + subscribe_idd
        print(temp_subs)
        BlogPosts.objects.select_related().filter(author_id=subscribe_id).update(subscribe=temp_subs)

        #testt_like = BlogPosts.objects.filter(subscribe__='2')
        #print(testt_like)
        return render(request, 'blogs/subscribe.html')


        #print(subs_posts)
        #all_posts = BlogPosts.objects.only('subscribe').get(id=1)
"""        print('req')
        subs = BlogPosts.objects.filter(author=True)
        print(subs)
        for object in subs:
            object.author = False
            print(object)
            object.save() 
        #context={"subs":subs}
        return redirect(request, 'blogs/subscribe.html')"""
