from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django_enumfield import enum


class Status(enum.Enum):
    DRAFT = 0
    PUBLISHED = 1

    __labels__ = {
        DRAFT: 'Draft',
        PUBLISHED: 'Published'
    }

class ArticleType(enum.Enum):
    ARTICLE = 0
    CARD = 1
    STORY = 2

    __labels__ = {
        ARTICLE: 'Article',
        CARD: 'Card',
        STORY: 'Story'
    }

class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    article_type = enum.EnumField(ArticleType, default=ArticleType.ARTICLE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='network_articles', null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = enum.EnumField(Status, default=Status.DRAFT)
    open_for_comment = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.text

    def approve(self):
        self.approved_comment = True
        self.save()    
