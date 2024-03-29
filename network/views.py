from time import time

import requests
import timeago
from cards.models import Card
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, F, Max
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.generic import DetailView, ListView, TemplateView

from network.models import (Article, ArticleType, Comment, ContactRequest,
                            Series, Status)

PAGE_LENGTH = 5
COMMENT_THROTTLE_SECONDS = 10


def format_article_summaries(articles, length=''):
    char_count = 540 if length == 'long' else 180
    for article in articles:
        article.age = timeago.format(article.published_on, timezone.now())
        if len(article.content) > char_count:
            article.summary = strip_tags(f'{article.content[:char_count]}...')
        else:
            article.summary = strip_tags(article.content)


def format_comment_age(comments):
    for comment in comments:
        comment.age = timeago.format(comment.created_date, timezone.now())


def format_card_discussions(discussions):
    char_count = 162
    for discussion in discussions:
        discussion.age = timeago.format(
            discussion.comments.first().created_date, timezone.now())
        if len(discussion.comments.first().text) > char_count:
            discussion.summary = strip_tags(
                f'{discussion.comments.first().text[:char_count]}...')
        else:
            discussion.summary = strip_tags(discussion.comments.first().text)


def store_comment(request):
    if request.method == 'POST':
        # Data
        url = request.POST.get('url')
        slug = request.POST.get('slug')
        comment_edit = request.POST.get('commentId')
        comment_text = request.POST.get('editordata')
        post = Article.objects.get(slug=slug)

        if url == 'card_view':
            card = Card.objects.get(slug=slug)
            url = reverse(url, args=(card.number,))
        else:
            url = reverse(url, args=(slug,))

        # Session
        last_comment = request.session.get('last_comment', None)
        if last_comment:
            seconds_ago = time() - last_comment
            if seconds_ago < COMMENT_THROTTLE_SECONDS:
                return HttpResponseRedirect('{}#commentSection'.format(url))

        request.session['last_comment'] = time()
        request.session.modified = True

        # Update
        if comment_edit:
            c = Comment.objects.filter(
                pk=comment_edit).update(text=comment_text)
        else:
            c = Comment(text=comment_text, author=request.user, post=post)
            c.save()

        return HttpResponseRedirect('{}#commentSection'.format(url))


def send_message(request):
    if request.method == 'POST':
        # Begin reCAPTCHA validation #
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        ask_google = requests.post(url, data=data)
        result = ask_google.json()
        # End reCAPTCHA validation #

        if result['success']:
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('editordata')

            cr = ContactRequest(
                name=name,
                contact=email,
                subject=subject,
                message=message
            )
            cr.save()

            context = {'title': 'Success',
                       'message': 'Communication sent successfully!'}
            return render(request, 'flatpages/contact_success.html', context)

    return HttpResponseRedirect(reverse('index'))


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
    url = request.POST.get('redirect_url')

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
            'comments.html', {
                'comments': comments,
                'user': request.user,
                'object': article,
                'redirect_url': url
            }
        ),
        'has_next': comments.has_next()
    }
    return JsonResponse(output_data)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        # Data
        latest_three_articles = Article.objects.order_by('-published_on').filter(
            article_type__in=[ArticleType.NEWS, ArticleType.ARTICLE], status=Status.PUBLISHED)[:3]
        format_article_summaries(latest_three_articles)

        latest_five_discussions = Card.objects.annotate(
            last_activity=Max('comments__created_date'),
            comment_count=Count('comments')
        ).filter(comment_count__gt=0).order_by('-last_activity')[:5]
        format_card_discussions(latest_five_discussions)

        cotd = Card.objects.order_by(
            F('card_of_the_day').desc(nulls_last=True))[:1]

        # Context
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update(
            {
                'big_article': latest_three_articles[0] if latest_three_articles else None,
                'small_articles': latest_three_articles[1:] if latest_three_articles else None,
                'cotd': cotd.get() if cotd else None,
                'discussions': latest_five_discussions if latest_five_discussions else None
            }
        )
        return context


class ArticleCategoriesListView(ListView):
    model = Series
    template_name = 'article_category_list.html'


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
        context['total'] = articles.count
        context['page_length'] = PAGE_LENGTH
        article_list = articles.all()[:PAGE_LENGTH]
        format_article_summaries(article_list, 'long')
        context['articles'] = article_list
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_view.html'

    def get_context_data(self, **kwargs):
        # Data
        comments = Comment.objects.filter(
            post=self.object).order_by('-created_date')
        comment_list = comments.all()[:PAGE_LENGTH]
        format_comment_age(comment_list)

        # Session

        # Context
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context.update(
            {
                'total': comments.count,
                'page_length': PAGE_LENGTH,
                'comments': comment_list,
                'redirect_url': 'article'
            }
        )
        return context


class DecksListView(ListView):
    """ Series 'decks' """
    template_name = 'decks.html'


class DeckView(DetailView):
    model = Article
    template_name = 'decks_view.html'
