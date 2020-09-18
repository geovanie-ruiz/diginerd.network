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
    NEWS = 0
    ARTICLE = 1
    CARD = 2
    STORY = 3

    __labels__ = {
        NEWS: 'News',
        ARTICLE: 'Article',
        CARD: 'Card',
        STORY: 'Story'
    }

class Series(models.Model):
    """ Serves as catogries for articles, and a means of classifying stories """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    article_type = enum.EnumField(ArticleType, default=ArticleType.ARTICLE)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, related_name='series_articles', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='network_articles', null=True, blank=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    published_on = models.DateTimeField(null=True, blank=True)
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
