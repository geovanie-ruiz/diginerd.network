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
        STORY: 'Digifiction'
    }

class Series(models.Model):
    """ Serves as catogries for articles, and a means of classifying stories """
    name = models.CharField(max_length=255, unique=True)
    hero_img = models.ImageField(upload_to='art/hero/series/', null=True, blank=True)
    enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255, unique=True)
    logline = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    article_type = enum.EnumField(ArticleType, default=ArticleType.ARTICLE)
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, related_name='series_articles', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='network_articles', null=True, blank=True)
    hero_img = models.ImageField(upload_to='art/hero/articles', null=True, blank=True)
    content = models.TextField(blank=True)
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

class Shop(models.Model):
    """
        Needs hours, digimon tournament times
        Connect to googlemaps?
    """
    name = models.CharField(max_length=255, unique=True)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=2) #needs a state list
    zipcode = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name}, ({self.city}, {self.state})'
