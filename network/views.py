import timeago
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView

from network.forms.forms import ShopForm
from network.models import Article, ArticleType, Comment, Series, Shop, Status


def format_article_summaries(articles):
    for article in articles:
        article.age = timeago.format(article.published_on, timezone.now())
        if len(article.content) > 180:
            article.summary = strip_tags(f'{article.content[:177]}...')
        else:
            article.summary = strip_tags(article.content)


def lazy_load_comments(request):
    page = request.POST.get('page')
    comments = Comment.objects.all()
    # use Django's pagination
    # https://docs.djangoproject.com/en/dev/topics/pagination/
    results_per_page = 5
    paginator = Paginator(comments, results_per_page)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(2)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    # build a html comments list with the paginated comments
    comments_html = loader.render_to_string(
        'comments.html',
        {'comments': comments}
    )
    # package output data and return it as a JSON object
    output_data = {
        'comments_html': comments_html,
        'has_next': comments.has_next()
    }
    return JsonResponse(output_data)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        latest_three_articles = Article.objects.order_by('-published_on').filter(
            article_type__in=[ArticleType.NEWS, ArticleType.ARTICLE], status=Status.PUBLISHED)[:3]

        format_article_summaries(latest_three_articles)
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
        format_article_summaries(top_ten_articles)
        context['articles'] = top_ten_articles
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_view.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        comment_total = Comment.objects.filter(post=self.object).count()
        context['comment_total'] = comment_total
        return context


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
