from django.db.models import Count, Q
from django.views.generic import DetailView, ListView, TemplateView

from network.models import Article, ArticleType, Series, Status


class IndexView(TemplateView):
    template_name = 'index.html'

    """
        TODO: #1 get relevant data
    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_articles'] = Article.objects.all()[:5]
        return context

class StoryListView(ListView):
    model = Article
    template_name = 'story_list.html'

    def get_queryset(self, *args, **kwargs):
        qs = Article.objects.filter(article_type=ArticleType.STORY, status=Status.PUBLISHED)
        return qs.order_by('-published_on')

class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

    def get_queryset(self, *args, **kwargs):
        qs = Article.objects.filter(article_type__in=[ArticleType.NEWS, ArticleType.ARTICLE], status=Status.PUBLISHED)
        return qs.order_by('-published_on')

class SeriesListView(ListView):
    model = Series
    template_name = 'series_list.html'

    def get_queryset(self, *args, **kwargs):
        """
            TODO: #2 fix series list query
        """
        qs = Series.objects.annotate(
            article_count=Count(
                'series_articles',
                filter=Q(series_articles__status=Status.PUBLISHED)
            )).filter(article_count__gt=0)
        return qs.order_by('-article_count')

class StoryDetailView(DetailView):
    model = Article
    template_name = 'story_view.html'

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_view.html'

class SeriesDetailView(DetailView):
    model = Series
    template_name = 'series_view.html'
