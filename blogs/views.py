# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView
#from django.views.generic.base import View
from blogs.forms import BlogPostsForms
from blogs.models import BlogPosts
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

class IndexTemplateView(LoginRequiredMixin, TemplateView):
    #  стартовая траница со всами постами всех пользователей
    def get(self, request):
        template_name = 'blogs/index.html'
        all_posts = BlogPosts.objects.all()
        #u = self.request.user
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

class AddPostView(LoginRequiredMixin, TemplateView):
    template_name = 'blogs/addpost.html'
    form_class = BlogPostsForms
    #login_url = 'addpost'

    def get(self, request):
        #form = BlogPostsForms
        #send_ids = request.GET.get('ids')
        title_send = request.GET.get('title')
        text_send = request.GET.get('text')
        author_send = self.request.user.id #request.GET.get('id')
        print(title_send, text_send, author_send)
        print('print')
        send_test = BlogPosts(title=title_send, text=text_send, author_id=author_send)
        #print(send_test)
        send_test.save()
        form = BlogPostsForms
        return render(request, 'blogs/addpost.html', {'form': form})


class TapeListView(LoginRequiredMixin, ListView):

    def get(self, request):
        #tape users which subscribe
        ug = self.request.user.id
        test_like = BlogPosts.objects.filter(subscribe__contains=ug).values('author_id')# фильтруем подписанных авторизированных по полю автор айди
        test_list = []
        for test_likes in test_like:
            test_list.append(test_likes['author_id'])
        list_entr = BlogPosts.objects.filter(author_id__in=list(test_list)).values_list('title', 'text', 'created', 'author__first_name', 'id', 'read_posts')
        #print(list_entr)
        tmp_array = []
        for list_entrs in list_entr:
            print(list_entrs[5].find(str(ug)))
            if list_entrs[5].find(str(ug)) == -1:
                #print('ne prochitano')
                tmp_two = list_entrs
                tmp_three = [tmp_two, 'не прочитано']
                tmp_array.append(tmp_three)
            else:
                tmp_two = list_entrs
                tmp_three = [tmp_two, 'прочитано']
                tmp_array.append(tmp_three)

        return render(request, 'blogs/tapelist.html', {'list_entr': list_entr, 'list_entr2': tmp_array})

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
    # отписка от блогов пользователей
    model = BlogPosts
    login_url = 'unsubscribe'
    def get(self, request):
        unsubscribe_idh = request.GET.get('iddu')# авториз юзер
        unsubscribe_id = request.GET.get('idu') # автор поста
        unsub_users = BlogPosts.objects.filter(author_id=unsubscribe_id).values('subscribe')
        for unsub_user in unsub_users:
            del_sub_for = unsub_user['subscribe']
            del_sub_for2 = del_sub_for.split(',')
            result = ''
            for del_sub_fors in del_sub_for2:
                if del_sub_fors != unsubscribe_idh:
                    result = result + ',' + del_sub_fors
            BlogPosts.objects.select_related().filter(author_id=unsubscribe_id).update(subscribe=result)

        unsub_users2 = BlogPosts.objects.filter(author_id=unsubscribe_id).values('read_posts')
        for unsub_user in unsub_users2:
            del_sub_for = unsub_user['read_posts']
            del_sub_for3 = del_sub_for.split(',')
            result = ''
            for del_sub_fors in del_sub_for3:
                if del_sub_fors != unsubscribe_idh:
                    result = result + ',' + del_sub_fors
            BlogPosts.objects.select_related().filter(author_id=unsubscribe_id).update(read_posts=result)

        return render(request, 'blogs/unsubscribe.html')

class ReadPostTemplView(LoginRequiredMixin, TemplateView):
    # пометка о прочитанности
    model = BlogPosts
    login_url = 'readpost'
    def get(self, request):
        print('id_request_user')
        id_request_user = request.GET.get('id')# авториз юзер
        print('id_request_user')
        print(id_request_user)
        id_request_post = request.GET.get('post')  # номер поста который помечаем

        read_post = BlogPosts.objects.filter(id=id_request_post).values('read_posts')
        result2 = ''
        result2 = read_post[0]['read_posts'] + ',' + id_request_user
        print_read=BlogPosts.objects.select_related().filter(id=id_request_post).update(read_posts=result2)
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



print('req')
        subs = BlogPosts.objects.filter(author=True)
        print(subs)
        for object in subs:
            object.author = False
            print(object)
            object.save()
            pass
            
            
            
            #if request.method == "POST":
            form = BlogPostsForms(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect("/")
        else:
            
            """
        #context={"subs":subs}
        #return redirect(request, 'blogs/subscribe.html')
