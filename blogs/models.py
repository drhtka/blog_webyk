# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

DEFAULT_SAMMICH = 0

class BlogPosts(models.Model):
    """Посты блога
    """
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
    )

    author = models.ForeignKey(
        User,
        related_name='blog_posts',
        on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=100,)
    text = models.TextField('Текст статьи',)
    created = models.DateField('Дата создания', auto_now_add=True,)
    status = models.CharField('Состояние', max_length=10, choices=STATUS_CHOICES, default='draft')
    subscribe = models.CharField('Подписан', max_length=30, null=True, blank=None, default=DEFAULT_SAMMICH)
    read_posts = models.CharField(max_length=30, null=True, blank=None)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        db_table = 'blogs'
        ordering = ('-created',)

    def __str__(self):
        #return "Посты блога %s" % self.title
        return self.title

#class ReadPosts(models.Model):
