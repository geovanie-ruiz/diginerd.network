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
    # Data
    max_id = Card.objects.all().count()-1
    search = True

    # Session (reset breadcrumbs)
    request.session['breadcrumbs'] = {}
    request.session.modified = True

    # Logic
    while True and max_id > -1:
        rand_id = random.randint(0, max_id)
        card = Card.objects.all()[rand_id]
        if card:
            return redirect('card_view', card.number)
    
    # Failsafe
    return redirect('cards')


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
    return redirect('filtered_list', request.POST.get('term'))


def card_filter(request):
    return redirect('cards')


class CardsIndexView(TemplateView):
    template_name = 'card_index.html'

    def get_context_data(self, **kwargs):
        # Data
        cards = Card.objects.annotate(
            last_activity=Max('comments__created_date'),
            comment_count=Coalesce(Count('comments'), 0)
        ).order_by(F('last_activity').desc(nulls_last=True))
        card_list = cards.all()[:PAGE_LENGTH]

        # Session (reset breadcrumbs)
        self.request.session['breadcrumbs'] = {}
        self.request.session.modified = True

        # Context
        context = super(CardsIndexView, self).get_context_data(**kwargs)
        context.update(
            {
                'list_name': 'Cards',
                'total': cards.count,
                'page_length': PAGE_LENGTH,
                'cards': card_list,
                'breadcrumbs': self.request.session.get('breadcrumbs')
            }
        )
        return context


class FilteredListView(TemplateView):
    template_name = 'card_index.html'

    def get_context_data(self, **kwargs):
        # Data
        term = self.kwargs['term']
        cards = Card.objects.filter(name__icontains=term).all()

        # Session
        breadcrumbs = self.request.session.get('breadcrumbs', {})

        if 'card' in breadcrumbs.keys():
            del breadcrumbs['card']
        if 'sets' in breadcrumbs.keys():
            del breadcrumbs['sets']
        if 'set' in breadcrumbs.keys():
            del breadcrumbs['set']

        self.request.session['breadcrumbs']['search_result'] = {
            'name': 'Search Results',
            'view': 'filtered_list',
            'key': term,
            'card': None
        }
        self.request.session.modified = True

        # Context
        context = super(FilteredListView, self).get_context_data(**kwargs)
        context.update(
            {
                'list_name': f'"{term}"',
                'cards': cards,
                'breadcrumbs': self.request.session.get('breadcrumbs', [])
            }
        )
        return context


class SetListView(ListView):
    model = ReleaseSet
    template_name = 'card_sets.html'

    def get_context_data(self, **kwargs):
        # Data

        # Session
        breadcrumbs = self.request.session.get('breadcrumbs', {})

        if 'card' in breadcrumbs.keys():
            del breadcrumbs['card']
        if 'search_result' in breadcrumbs.keys():
            del breadcrumbs['search_result']
        if 'set' in breadcrumbs.keys():
            del breadcrumbs['set']

        self.request.session['breadcrumbs']['sets'] = {
            'name': 'Set List',
            'view': 'sets',
            'key': ''
        }
        self.request.session.modified = True

        # Context
        context = super(SetListView, self).get_context_data(**kwargs)
        context.update(
            {
                'breadcrumbs': self.request.session.get('breadcrumbs')
            }
        )
        return context


class FilteredSetView(TemplateView):
    template_name = 'card_index.html'

    def get_context_data(self, **kwargs):
        code = self.kwargs['code']
        set = ReleaseSet.objects.get(code=code)
        cards = Card.objects.filter(release_set=set).all()

        # Session
        breadcrumbs = self.request.session.get('breadcrumbs', {})

        if 'card' in breadcrumbs.keys():
            del breadcrumbs['card']
        if 'search_result' in breadcrumbs.keys():
            del breadcrumbs['sets']

        set_crumb = [{
            'name': str(set),
            'view': 'filtered_set',
            'key': code
        }]

        if 'sets' in breadcrumbs.keys():
            breadcrumbs['sets']['set'] = set_crumb.pop()
        
        if set_crumb:
            breadcrumbs['set'] = set_crumb.pop()

        self.request.session['breadcrumbs'] = breadcrumbs
        self.request.session.modified = True

        # Context
        context = super(FilteredSetView, self).get_context_data(**kwargs)
        context.update(
            {
                'list_name': f'{str(set)}',
                'cards': cards,
                'breadcrumbs': self.request.session.get('breadcrumbs')
            }
        )
        return context


class CardDetailView(DetailView):
    model = Card
    template_name = 'card_details.html'

    def get_object(self):
        return get_object_or_404(Card, number=self.kwargs['number'])

    def get_context_data(self, **kwargs):
        # Data
        # Comments

        # Session
        card_crumb = [{
            'name': str(self.object),
            'view': 'card_view',
            'key': self.object.number
        }]
        breadcrumbs = self.request.session.get('breadcrumbs', {})

        if 'search_result' in breadcrumbs.keys():
            breadcrumbs['search_result']['card'] = card_crumb.pop()
        elif 'sets' in breadcrumbs.keys():
            if 'set' in breadcrumbs['sets'].keys():
                breadcrumbs['sets']['set']['card'] = card_crumb.pop()
            else:
                del breadcrumbs['sets']
        elif 'set' in breadcrumbs.keys():
            breadcrumbs['set']['card'] = card_crumb.pop()

        if card_crumb:
            breadcrumbs['card'] = card_crumb.pop()

        self.request.session['breadcrumbs'] = breadcrumbs
        self.request.session.modified = True

        # Context
        context = super(CardDetailView, self).get_context_data(**kwargs)
        context.update(
            {
                'breadcrumbs': self.request.session.get('breadcrumbs', [])
            }
        )
        return context
