import timeago
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView

from network.forms.forms import ShopForm
from network.models import Article, ArticleType, Comment, Series, Shop, Status


PAGE_LENGTH = 5


def format_article_summaries(articles):
    for article in articles:
        article.age = timeago.format(article.published_on, timezone.now())
        if len(article.content) > 180:
            article.summary = strip_tags(f'{article.content[:177]}...')
        else:
            article.summary = strip_tags(article.content)


def format_comment_age(comments):
    for comment in comments:
        comment.age = timeago.format(comment.created_date, timezone.now())


def store_comment(request):
    if request.method == 'POST':
        print(request.POST)
        post = Article.objects.get(slug=request.POST.get('slug'))
        c = Comment(
            text=request.POST.get('editordata'),
            author=request.user,
            post=post
        )
        c.save()
        url = reverse('article', args=(request.POST.get('slug'),))
        return HttpResponseRedirect('{}#commentSection'.format(url))


def lazy_load_articles(request):
    pk = request.POST.get('container')
    page = request.POST.get('page')

    article_list = Article.objects.filter(
        series__id=pk
    ).order_by('-published_on')

    paginator = Paginator(article_list, PAGE_LENGTH)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(2)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    format_article_summaries(articles)
    output_data = {
        'contents_html': loader.render_to_string(
            'articles.html', {'articles': articles}
        ),
        'has_next': articles.has_next()
    }
    return JsonResponse(output_data)


def lazy_load_comments(request):
    pk = request.POST.get('container')
    page = request.POST.get('page')

    article = Article.objects.get(pk=pk)
    comments = Comment.objects.filter(post=article)

    paginator = Paginator(comments, PAGE_LENGTH)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(2)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    format_comment_age(comments)
    output_data = {
        'contents_html': loader.render_to_string(
            'comments.html', {'comments': comments}
        ),
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
        articles = Article.objects.filter(
            series__id=self.object.pk).order_by('-published_on')
        context['page_length'] = PAGE_LENGTH
        article_list = articles.all()[:PAGE_LENGTH]
        format_article_summaries(article_list)
        context['articles'] = article_list
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_view.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(
            post=self.object).order_by('-created_date')
        context['total'] = comments.count
        context['page_length'] = PAGE_LENGTH
        comment_list = comments.all()[:PAGE_LENGTH]
        format_comment_age(comment_list)
        context['comments'] = comment_list
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
