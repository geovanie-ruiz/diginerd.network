from datetime import datetime

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django_summernote.admin import SummernoteModelAdmin

from .models import (Article, ArticleType, Comment, ContactRequest, Series,
                     Shop, Status)

admin.site.register(Series)
admin.site.register(Shop)


def make_published(ModelAdmin, request, queryset):
    queryset.update(status=Status.PUBLISHED, published_on=datetime.now())


def approve_comment(ModelAdmin, request, queryset):
    queryset.update(approved_comment=True)


def reply(ModelAdmin, request, queryset):
    queryset.update(replied=True)


make_published.short_description = 'Mark selected articles as published'
approve_comment.short_description = 'Mark selected comments as approved'
reply.short_description = 'Mark selected contact requests as replied to'


class ArticleTypeFilter(SimpleListFilter):
    title = 'By article type'
    parameter_name = 'article_type'

    def lookups(self, request, model_admin):
        types = set([a.article_type for a in model_admin.model.objects.exclude(
            article_type=ArticleType.CARD)])
        return [(a.value, a.label) for a in types]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(article_type=self.value())


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'
    list_display = ('title', 'slug', 'status', 'created_on')
    list_filter = ('status', ArticleTypeFilter,)
    search_fields = ['title', 'content']
    actions = [make_published]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(article_type=ArticleType.CARD)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'created_date', 'approved_comment', 'text')
    list_filter = ('author', 'approved_comment')
    search_fields = ['content']
    actions = [approve_comment]


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'subject', 'replied')
    actions = [reply]
