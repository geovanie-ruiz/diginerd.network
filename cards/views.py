import random

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, F, Max, Q
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.views.generic import DetailView, ListView, TemplateView
from network.models import Comment
from network.views import PAGE_LENGTH, format_comment_age

from cards.models import (MAX_LEVEL, Card, CardColor, CardEffect, CardKeyword,
                          CardRarity, CardType, DigimonStage, EffectType,
                          ReleaseSet)

LIST_LENGTH = 8
AUTOCOMPLETE_LIMIT = 10
FILTER_TERM = 'filtered-list'


def filter_data():
    filters = {
        'colors': [{'color': color.label, 'tag': color.label.lower()} for color in CardColor],
        'card_types': [{'type': type.label, 'tag': type.label.lower()} for type in CardType],
        'rarities': [{'rarity': rarity.label, 'tag': rarity.label.lower()} for rarity in CardRarity],
        'keywords': [{'id': keyword.id, 'keyword': keyword.name} for keyword in CardKeyword.objects.all()],
        'effect_types': [{'type': type.label, 'tag': type.label.lower()} for type in EffectType],
        'levels': [level for level in range(2, MAX_LEVEL + 1)],
        'stages': [{'stage': stage.label, 'tag': stage.label.lower()} for stage in DigimonStage],
        'digimon_types': [card.flavor_type for card in Card.objects.order_by('flavor_type').distinct('flavor_type')],
        'attributes': [card.flavor_attribute for card in Card.objects.order_by('flavor_attribute').distinct('flavor_attribute')]
    }
    return filters


def get_filtered_cards(session):
    filters = session.get('apply_filters', {})
    cards = Card.objects.all()

    # Handle Color filtering
    colors = [color for color in CardColor if filters['colors'][color.value]]
    if colors:
        if filters['multicolor']:
            cards = cards.filter(
                Q(color__in=colors) | Q(evo__color__in=colors)
            ).order_by('number').distinct('number')
        else:
            cards = cards.filter(color__in=colors)

    # Handle Card Type filtering
    card_types = [
        type for type in CardType if filters['card_types'][type.value]]
    if card_types:
        cards = cards.filter(card_type__in=card_types)

    # Handle Card Rarity filtering
    if filters['rarities']:
        rarities = [CardRarity(int(rarity_id))
                    for rarity_id in filters['rarities']]
        if rarities:
            cards = cards.filter(rarity__in=rarities)

    # Handle Card Rarity filtering
    if filters['keywords']:
        keywords = [int(keyword_id) for keyword_id in filters['keywords']]
        if keywords:
            cards = cards.filter(effect__card_keyword__id__in=keywords).order_by(
                'number').distinct('number')

    # Handle Play Cost Range
    if filters['playcost']:
        playFrom = - \
            1 if filters['playcost'][0] == '' else int(filters['playcost'][0])
        playTo = - \
            1 if filters['playcost'][1] == '' else int(filters['playcost'][1])
        if playFrom < 0 and playTo < 0:
            # neither set
            pass
        elif (playFrom >= 0 and playTo < 0) or (playFrom > playTo):
            # starting from
            cards = cards.filter(play_cost__gte=playFrom)
        elif playFrom < 0 and playTo >= 0:
            # going to
            cards = cards.filter(play_cost__lte=playTo)
        elif playFrom < playTo:
            # good range
            cards = cards.filter(play_cost__gte=playFrom,
                                 play_cost__lte=playTo)
        elif playFrom == playTo:
            # specific number
            cards = cards.filter(play_cost=playFrom)

    # Handle Effect Types filter
    if filters['effect_types']:
        effect_types = [EffectType(int(type_id))
                        for type_id in filters['effect_types']]
        if effect_types:
            cards = cards.filter(effect__effect_type__in=effect_types).order_by(
                'number').distinct('number')

    # Handle Effect scan
    if filters['effect_scan']:
        print(filters['effect_scan'])
        cards = cards.filter(
            effect__effect_text__icontains=filters['effect_scan'])

    # Handle Digimon Power Range
    if filters['digimon_power']:
        dpFrom = - \
            1 if filters['digimon_power'][0] == '' else int(
                filters['digimon_power'][0])
        dpTo = - \
            1 if filters['digimon_power'][1] == '' else int(
                filters['digimon_power'][1])
        if dpFrom < 0 and dpTo < 0:
            # neither set
            pass
        elif (dpFrom >= 0 and dpTo < 0) or (dpFrom > dpTo):
            # starting from
            cards = cards.filter(digimon_power__gte=dpFrom)
        elif dpFrom < 0 and dpTo >= 0:
            # going to
            cards = cards.filter(digimon_power__lte=dpTo)
        elif dpFrom < dpTo:
            # good range
            cards = cards.filter(digimon_power__gte=dpFrom,
                                 digimon_power__lte=dpTo)
        elif dpFrom == dpTo:
            # specific number
            cards = cards.filter(digimon_power=dpFrom)

    # Handle Levels filter
    if filters['levels']:
        levels = [int(level) + 2 for level in filters['levels']]
        if levels:
            cards = cards.filter(level__in=levels)

    # Handle Stages filter
    if filters['stages']:
        stages = [DigimonStage(int(stage_id))
                  for stage_id in filters['stages']]
        if stages:
            cards = cards.filter(stage__in=stages)

    # Handle Flavor Types
    if filters['digimon_types']:
        types = [type for type in filters['digimon_types']]
        if types:
            cards = cards.filter(flavor_type__in=types).order_by(
                'number').distinct('number')

    # Handle Flavor Attributes
    if filters['attributes']:
        attributes = [attribute for attribute in filters['attributes']]
        if attributes:
            cards = cards.filter(flavor_attribute__in=attributes).order_by(
                'number').distinct('number')

    return cards


def get_searched_cards(term):
    return Card.objects.filter(name__icontains=term).all()


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
    print(request.POST)
    page = request.POST.get('page')
    term = request.POST.get('term')
    filtered = request.POST.get('filtered') == 'true'

    if term:
        cards = get_searched_cards(term)
    elif filtered:
        cards = get_filtered_cards(request.session)
    else:
        cards = Card.objects.annotate(
            last_activity=Max('comments__created_date'),
            comment_count=Coalesce(Count('comments'), 0)
        ).order_by(F('last_activity').desc(nulls_last=True))

    paginator = Paginator(cards, LIST_LENGTH)
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
    # Data
    filters = {
        'colors': [
            bool(request.POST.getlist(f'colors[{i}]', []))
            for i in range(len(CardColor))
        ],
        'multicolor': bool(request.POST.get('includeSource', False)),
        'card_types': [
            bool(request.POST.getlist(f'ctype[{i}]', []))
            for i in range(len(CardType))
        ],
        'rarities': request.POST.getlist('raritySelect', []),
        'keywords': request.POST.getlist('keywordSelect', []),
        'playcost': [
            request.POST.get('playCostFrom', 0),
            request.POST.get('playCostTo', 0)
        ],
        'effect_types': request.POST.getlist('effectTypeSelect', []),
        'effect_scan': request.POST.get('effectScan', ''),
        'digimon_power': [
            request.POST.get('dpFrom', 0),
            request.POST.get('dpTo', 0)
        ],
        'levels': request.POST.getlist('levelSelect', []),
        'stages': request.POST.getlist('stageSelect', []),
        'digimon_types': request.POST.getlist('digimonTypeSelect', []),
        'attributes': request.POST.getlist('attributeSelect', []),

    }

    # Session (store filter)
    request.session['apply_filters'] = filters
    request.session.modified = True

    return redirect('filtered_list', FILTER_TERM)


class CardsIndexView(TemplateView):
    template_name = 'card_index.html'

    def get_context_data(self, **kwargs):
        # Data
        cards = Card.objects.annotate(
            last_activity=Max('comments__created_date'),
            comment_count=Coalesce(Count('comments'), 0)
        ).order_by(F('last_activity').desc(nulls_last=True))
        card_list = cards.all()[:LIST_LENGTH]

        # Session (reset breadcrumbs)
        filters = self.request.session.get('filters', {})
        if not filters:
            self.request.session['filters'] = filter_data()
        self.request.session['breadcrumbs'] = {}
        self.request.session.modified = True

        # Context
        context = super(CardsIndexView, self).get_context_data(**kwargs)
        context.update(
            {
                'list_name': 'Cards',
                'total': cards.count,
                'page_length': LIST_LENGTH,
                'cards': card_list,
                'breadcrumbs': self.request.session.get('breadcrumbs'),
                'filters': self.request.session.get('filters')
            }
        )
        return context


class FilteredListView(TemplateView):
    template_name = 'card_index.html'

    def get_context_data(self, **kwargs):
        # Data
        term = self.kwargs['term']
        if term == FILTER_TERM:
            name = 'Filtered List'
            breadcrumb = 'Filter Result'
            cards = get_filtered_cards(self.request.session)
        else:
            name = f'"{term}"'
            breadcrumb = 'Search Result'
            cards = get_searched_cards(term)

        card_list = cards.all()[:LIST_LENGTH]

        # Session
        filters = self.request.session.get('filters', {})
        if not filters:
            self.request.session['filters'] = filter_data()
        breadcrumbs = self.request.session.get('breadcrumbs', {})

        if 'card' in breadcrumbs.keys():
            del breadcrumbs['card']
        if 'sets' in breadcrumbs.keys():
            del breadcrumbs['sets']
        if 'set' in breadcrumbs.keys():
            del breadcrumbs['set']

        self.request.session['breadcrumbs']['search_result'] = {
            'name': breadcrumb,
            'view': 'filtered_list',
            'key': term,
            'card': None
        }
        self.request.session.modified = True

        # Context
        context = super(FilteredListView, self).get_context_data(**kwargs)
        context.update(
            {
                'list_name': name,
                'total': cards.count,
                'page_length': LIST_LENGTH,
                'cards': card_list,
                'breadcrumbs': self.request.session.get('breadcrumbs'),
                'filters': self.request.session.get('filters'),
                'term': '' if term == FILTER_TERM else term,
                'filtered': True if term == FILTER_TERM else None
            }
        )
        return context


class SetListView(ListView):
    model = ReleaseSet
    template_name = 'card_sets.html'

    def get_context_data(self, **kwargs):
        # Data

        # Session
        filters = self.request.session.get('filters', {})
        if not filters:
            self.request.session['filters'] = filter_data()
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
                'breadcrumbs': self.request.session.get('breadcrumbs'),
                'filters': self.request.session.get('filters')
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
        filters = self.request.session.get('filters', {})
        if not filters:
            self.request.session['filters'] = filter_data()
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
                'breadcrumbs': self.request.session.get('breadcrumbs'),
                'filters': self.request.session.get('filters')
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
        idx = 0
        effects = [
            {
                'label': EffectType.MAIN.label,
                'effects': []
            },
            {
                'label': EffectType.SOURCE.label,
                'effects': []
            },
            {
                'label': EffectType.SECURITY.label,
                'effects': []
            }
        ]
        for idx, effect in enumerate(CardEffect.objects.filter(card=self.object)):
            if effect.effect_text:
                text = effect.effect_text
            else:
                keyword = effect.card_keyword
                text = f'{keyword.name} ({keyword.reminder_text})'
            effects[effect.effect_type.value]['effects'].append(text)
        else:
            if idx == 0:
                effects = []
        comments = Comment.objects.filter(
            post=self.object).order_by('-created_date')
        comment_list = comments.all()[:PAGE_LENGTH]
        format_comment_age(comment_list)

        # Session
        filters = self.request.session.get('filters', {})
        if not filters:
            self.request.session['filters'] = filter_data()
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
                'breadcrumbs': self.request.session.get('breadcrumbs'),
                'filters': self.request.session.get('filters'),
                'card_effects': effects,
                'total': comments.count,
                'page_length': PAGE_LENGTH,
                'comments': comment_list,
                'redirect_url': 'card_view'
            }
        )
        return context
