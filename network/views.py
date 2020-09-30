from django.db.models import Count, Q
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView

from network.forms.forms import ShopForm
from network.models import Article, ArticleType, Series, Shop, Status


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

class ShopListView(ListView):
    model = Shop
    template_name = 'lgs.html'

class ShopDetailView(DetailView):
    model = Shop
    template_name = 'lgs_view.html'

class ShopAddView(FormView):
    form_class = ShopForm
    template_name = 'lgs_add.html'
    success_url = '/lgs/'

    def form_valid(self, form):
        form.add_lgs()
        return super().form_valid(form)

class ContactView(TemplateView):
    template_name = 'contact.html'

class PrivacyView(TemplateView):
    template_name = 'privacy.html'

class TermsView(TemplateView):
    template_name = 'terms.html'

class GameplayView(TemplateView):
    template_name = 'gameplay.html'

class RulesView(TemplateView):
    template_name = 'rules.html'

class ColorsView(TemplateView):
    """ Article 'colors' """
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

class RulingsListView(ListView):
    """ Series 'rulings' """
    template_name = 'rulings.html'

class RulingsDetailView(DetailView):
    model = Article
    template_name = 'rulings_view.html'

class ErrataListView(ListView):
    """ Series 'errata' """
    template_name = 'errata.html'

class ErrataDetailView(DetailView):
    model = Article
    template_name = 'errata_view.html'
