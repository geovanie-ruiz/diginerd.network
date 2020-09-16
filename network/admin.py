from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from .models import Article, ArticleType, Comment, Status


def make_published(ModelAdmin, request, queryset):
    queryset.update(status=Status.PUBLISHED)

def approve_comment(ModelAdmin, request, queryset):
    queryset.update(approved_comment=True)

make_published.short_description = 'Mark selected articles as published'
approve_comment.short_description = 'Mark selected comments as approved'

class ArticleTypeFilter(SimpleListFilter):
    title = 'By article type'
    parameter_name = 'article_type'

    def lookups(self, request, model_admin):
        types = set([a.article_type for a in model_admin.model.objects.exclude(article_type=ArticleType.CARD)])
        return [(a.value, a.label) for a in types]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(article_type=self.value())

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
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
