import json
import random

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, F, Max, Q
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.views.generic import DetailView, ListView, TemplateView

from cards.models import Card, CardEffect, ReleaseSet

PAGE_LENGTH = 8
AUTOCOMPLETE_LIMIT = 10


def get_random_card(request):
    max_id = Card.objects.all().count()-1
    search = True
    while search:
        rand_id = random.randint(0, max_id)
        card = Card.objects.all()[rand_id]
        search = False if card else True
    return redirect('card_view', card.number)


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
    cards = [card.name for card in Card.objects.filter(
        name__icontains=term).order_by('name').distinct('name')]
    return JsonResponse(cards[:AUTOCOMPLETE_LIMIT], safe=False)


def card_search(request):
    term = request.POST.get('term')
    return redirect('filtered_list', term)


class CardsIndexView(TemplateView):
    template_name = 'card_index.html'

    def get_context_data(self, **kwargs):
        context = super(CardsIndexView, self).get_context_data(**kwargs)
        cards = Card.objects.annotate(
            last_activity=Max('comments__created_date'),
            comment_count=Coalesce(Count('comments'), 0)
        ).order_by(F('last_activity').desc(nulls_last=True))
        context['list_name'] = 'Cards'
        context['total'] = cards.count
        context['page_length'] = PAGE_LENGTH
        card_list = cards.all()[:PAGE_LENGTH]
        context['cards'] = card_list
        return context


class FilteredListView(TemplateView):
    template_name = 'card_index.html'

    def get_context_data(self, **kwargs):
        term = self.kwargs['term']
        context = super(FilteredListView, self).get_context_data(**kwargs)
        cards = Card.objects.filter(name__icontains=term).all()
        context['list_name'] = f'"{term}"'
        context['cards'] = cards
        context['breadcrumbs'] = [
            {
                'name': 'Search Results',
                'view': 'filtered_list',
                'url': None
            }
        ]
        return context


class SetListView(ListView):
    model = ReleaseSet
    template_name = 'card_sets.html'


class CardDetailView(DetailView):
    model = Card
    template_name = 'card_details.html'

    def get_object(self):
        return get_object_or_404(Card, number=self.kwargs['number'])
