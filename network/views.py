from django.utils import timezone

import timeago
from django.db.models import Count, Q
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView

from network.forms.forms import ShopForm
from network.models import Article, ArticleType, Series, Shop, Status


def format_articles(articles):
    for article in articles:
        article.age = timeago.format(article.published_on, timezone.now())
        if len(article.content) > 180:
            article.summary = f'{article.content[:177]}...'
        else:
            article.summary = article.content


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        latest_three_articles = Article.objects.order_by('-published_on').filter(
            article_type__in=[ArticleType.NEWS, ArticleType.ARTICLE], status=Status.PUBLISHED)[:3]

        format_articles(latest_three_articles)
        context['big_article'] = latest_three_articles[0]
        context['small_articles'] = latest_three_articles[1:]

        return context


class ArticleCategoriesListView(ListView):
    model = Article
    template_name = 'article_category_list.html'

    def get_queryset(self, *args, **kwargs):
        qs = Article.objects.filter(
            article_type__in=[ArticleType.NEWS, ArticleType.ARTICLE],
            status=Status.PUBLISHED
        ).order_by('series').distinct('series')
        return qs


class ArticlesByArticlesCategoryView(DetailView):
    model = Series
    template_name = 'articles_by_article_category.html'

    def get_context_data(self, **kwargs):
        context = super(
            ArticlesByArticlesCategoryView,
            self
        ).get_context_data(**kwargs)
        top_ten_articles = Article.objects.order_by('-published_on').filter(
            series__id=self.object.pk)[:10]
        format_articles(top_ten_articles)
        context['articles'] = top_ten_articles
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_view.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class PrivacyView(TemplateView):
    template_name = 'privacy.html'


class TermsView(TemplateView):
    template_name = 'terms.html'


class RoadmapView(TemplateView):
    template_name = 'roadmap.html'


class GameplayView(TemplateView):
    template_name = 'gameplay.html'


class RulesView(TemplateView):
    template_name = 'rules.html'


class ColorsView(TemplateView):
    template_name = 'colors.html'


class DecksListView(ListView):
    """ Series 'decks' """
    template_name = 'decks.html'


class DeckView(DetailView):
    model = Article
    template_name = 'decks_view.html'


class TrialSetListView(ListView):
    """ Series 'trials' """
    template_name = 'trial_sets.html'


class TrialSetDetailView(DetailView):
    model = Article
    template_name = 'trial_set_view.html'


class BoosterSetListView(ListView):
    """ Series 'boosters' """
    template_name = 'booster_sets.html'


class BoosterSetDetailView(DetailView):
    model = Article
    template_name = 'booster_set_view.html'
