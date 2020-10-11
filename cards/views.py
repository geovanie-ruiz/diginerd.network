from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView


def lazy_load_cards(request):
    """
    slug = request.POST.get('article')
    article = Article.objects.get(slug=slug)
    page = request.POST.get('page')
    comments = Comment.objects.filter(post=article)
    # use Django's pagination
    # https://docs.djangoproject.com/en/dev/topics/pagination/
    results_per_page = PAGE_LENGTH
    paginator = Paginator(comments, results_per_page)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(2)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    # build a html comments list with the paginated comments
    format_comment_age(comments)
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
    """
    pass


class IndexView(TemplateView):
    template_name = 'card_search.html'


class TrialSetListView(ListView):
    """ Series 'trials' """
    template_name = 'trial_sets.html'


class TrialSetDetailView(DetailView):
    template_name = 'trial_set_view.html'


class BoosterSetListView(ListView):
    """ Series 'boosters' """
    template_name = 'booster_sets.html'


class BoosterSetDetailView(DetailView):
    template_name = 'booster_set_view.html'
