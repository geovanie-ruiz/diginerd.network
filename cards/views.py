import json
import random

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, F, Max, Q
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.views.generic import DetailView, ListView, TemplateView

from cards.models import Card, CardEffect

PAGE_LENGTH = 8


def get_random_card():
    max_id = Card.objects.all().count()-1
    while True:
        rand_id = random.randint(0, max_id)
        card = Card.objects.all()[rand_id]
        if card:
            return card.number


def lazy_load_cards(request):
    page = request.POST.get('page')
    cards = Card.objects.annotate(
        last_activity=Max('comments__created_date'),
        comment_count=Coalesce(Count('comments'), 0)
    ).order_by(F('last_activity').desc(nulls_last=True))
    paginator = Paginator(cards, PAGE_LENGTH)
    try:
        cards = paginator.page(page)
    except PageNotAnInteger:
        cards = paginator.page(2)
    except EmptyPage:
        cards = paginator.page(paginator.num_pages)
    cards_html = loader.render_to_string('card_art.html', {'cards': cards})
    output_data = {'contents_html': cards_html, 'has_next': cards.has_next()}
    return JsonResponse(output_data)


def card_autocomplete(request, **kwargs):
    term = request.GET.get('term')
    cards = [str(card) for card in Card.objects.filter(name__icontains=term)]
    return JsonResponse(cards, safe=False)


class CardsIndexView(TemplateView):
    template_name = 'card_search.html'

    def get_context_data(self, **kwargs):
        context = super(CardsIndexView, self).get_context_data(**kwargs)
        cards = Card.objects.annotate(
            last_activity=Max('comments__created_date'),
            comment_count=Coalesce(Count('comments'), 0)
        ).order_by(F('last_activity').desc(nulls_last=True))
        context['total'] = cards.count
        context['page_length'] = PAGE_LENGTH
        card_list = cards.all()[:PAGE_LENGTH]
        context['cards'] = card_list
        context['random'] = get_random_card()
        return context


class SetListView(ListView):
    template_name = 'sets.html'


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


class CardDetailView(DetailView):
    template_name = 'card.html'
