# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView
#from django.views.generic.base import View
from blogs.forms import BlogPostsForms
from blogs.models import BlogPosts
from django.contrib.auth.mixins import LoginRequiredMixin

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
        #tape users which subscribe
        ug = self.request.user.id
        test_like = BlogPosts.objects.filter(subscribe__contains=ug).values('author_id')# фильтруем подписанных авторизированных по полю автор айди
        test_list = []
        for test_likes in test_like:
            test_list.append(test_likes['author_id'])
        list_entr = BlogPosts.objects.filter(author_id__in=list(test_list)).values_list('title', 'text', 'created', 'author__first_name', 'id', 'read_posts')
        print(list_entr)

        return render(request, 'blogs/tapelist.html', {'list_entr': list_entr})

class SubscribeListView(LoginRequiredMixin, TemplateView):
    # подписка на блоги пользователей
    model = BlogPosts
    context_object_name = "subsc"
    template_name = 'blogs/subscribe.html'
    login_url = 'subscribe'

    def get(self, request):
        #print('hello')
        subscribe_idd = request.GET.get('idd')
        subscribe_id = int(request.GET.get('id'))

        test_all=BlogPosts.objects.filter(author_id=subscribe_id).values('subscribe')
        temp_subs = test_all[0]['subscribe']
        temp_subs = temp_subs + ',' + subscribe_idd
        BlogPosts.objects.select_related().filter(author_id=subscribe_id).update(subscribe=temp_subs)
        return render(request, 'blogs/subscribe.html')

class UnSubscribeListView(LoginRequiredMixin, TemplateView):
    # отписка на блоги пользователей
    model = BlogPosts
    login_url = 'unsubscribe'
    def get(self, request):
        unsubscribe_idh = request.GET.get('iddu')# авториз юзер
        unsubscribe_id = request.GET.get('idu') # автор поста
        unsub_users = BlogPosts.objects.filter(author_id=unsubscribe_id).values('subscribe')

        for unsub_user in unsub_users:
            del_sub_for = unsub_user['subscribe']
            print(del_sub_for)
            print(unsub_user)
            print('subscribe')
            del_sub_for2 = del_sub_for.split(',')
            result = ''
            for del_sub_fors in del_sub_for2:
                if del_sub_fors != unsubscribe_idh:
                    result = result + ',' + del_sub_fors
            print('result')
            print(result)
            BlogPosts.objects.select_related().filter(author_id=unsubscribe_id).update(subscribe=result)

        return render(request, 'blogs/unsubscribe.html')

class ReadPostTemplView(LoginRequiredMixin, TemplateView):
    model = BlogPosts
    login_url = 'readpost'

    def get(self, request):
        id_request_user = request.GET.get('id')# авториз юзер
        id_request_post = request.GET.get('post')  # номер поста который помечаем

        read_post = BlogPosts.objects.filter(id=id_request_post).values('read_posts')
        print('11111')
        result2 = ''
        #for unsub_user in unsub_users:
        #    del_sub_for = unsub_user['read_posts']
        print(read_post)
        #update_read_posts = read_post[0]['read_posts'].split(',')
        #print(update_read_posts)
        result2 = read_post[0]['read_posts'] + ',' + id_request_user
        #BlogPosts.objects.select_related().filter(id=id_request_post).update(read_posts=result2)
        print_read=BlogPosts.objects.select_related().filter(id=id_request_post).update(read_posts=result2)
        print(print_read)
        return redirect('/tapelist')

"""class SendPost(CreateView):
    model = BlogPosts
    form_class = BlogPostsForms
    template_name = 'blogs/details.html'

    def form_valid(self, form):
        #post =
        form.save()  # проверка на валидность
        return redirect('/sendpost/')

    def succes_url(self):
        return redirect('/sendpost/')  # куда редиректить когда мы сделам что либо на наш url


     print('uns_test_uns')   
        print('uns_test')
        print(unsubscribe_idd)
        print(request.GET)


print('req')
        subs = BlogPosts.objects.filter(author=True)
        print(subs)
        for object in subs:
            object.author = False
            print(object)
            object.save() 
        #context={"subs":subs}
        return redirect(request, 'blogs/subscribe.html')"""
